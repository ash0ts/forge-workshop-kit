"""Acquire pinned Banking77 and cache frozen MiniLM vectors; no provider calls."""
import argparse
import csv
import hashlib
import io
import json
import time
import urllib.request
from pathlib import Path

import numpy as np
from forge_workshop_kit import routing


def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def encode(texts, model_path, batch_size=64):
    import torch
    from transformers import AutoModel, AutoTokenizer
    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModel.from_pretrained(model_path, local_files_only=True).eval().cpu()
    vectors = []
    for start in range(0, len(texts), batch_size):
        batch = tokenizer(texts[start:start+batch_size], return_tensors="pt", padding=True,
                          truncation=True, max_length=256)
        with torch.no_grad():
            result = model(**batch).last_hidden_state
            mask = batch["attention_mask"].unsqueeze(-1)
            pooled = (result*mask).sum(1)/mask.sum(1).clamp(min=1)
            vectors.append(torch.nn.functional.normalize(pooled, p=2, dim=1).numpy())
        if start % (batch_size*20) == 0:
            print(f"Encoded {min(start+batch_size,len(texts))}/{len(texts)}", flush=True)
    return np.concatenate(vectors).astype(np.float32)


def prepare(output, model_path):
    output.mkdir(parents=True, exist_ok=True)
    model_path.mkdir(parents=True, exist_ok=True)
    base = f"https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/{routing.DATA_REVISION}/"
    sources = {}
    rows = []
    for name in ("train.csv", "test.csv"):
        content = fetch(base+"banking_data/"+name)
        (output/name).write_bytes(content)
        sources[name] = {"url": base+"banking_data/"+name, "sha256": hashlib.sha256(content).hexdigest()}
        split = name.split(".")[0]
        part = [{"id": f"official-{split}/{index:05d}", "text": row["text"], "label": row["category"]}
                for index,row in enumerate(csv.DictReader(io.StringIO(content.decode()))) ]
        rows += routing.assign_split(part) if split == "train" else [{**r,"split":"test"} for r in part]
    (output/"LICENSE-Banking77.txt").write_bytes(fetch(base+"LICENSE"))
    encoder_files = ("config.json", "tokenizer_config.json", "tokenizer.json", "vocab.txt", "special_tokens_map.json", "model.safetensors")
    encoder_checksums = {}
    encoder_lock = json.loads((Path(__file__).resolve().parents[1]/"examples/routing/encoder-files.json").read_text())
    for name in encoder_files:
        path = model_path/name
        if not path.exists():
            path.write_bytes(fetch(f"https://huggingface.co/{routing.ENCODER}/resolve/{routing.ENCODER_REVISION}/{name}"))
        encoder_checksums[name] = routing.checksum(path)
        if encoder_checksums[name] != encoder_lock[name]:
            raise ValueError(f"Pinned encoder checksum differs: {name}")
    (output/"cases.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n")
    started = time.perf_counter()
    np.save(output/"embeddings.npy", encode([r["text"] for r in rows],model_path))
    manifest = {"dataset":"Banking77", "dataset_revision":routing.DATA_REVISION,
                "license":"CC-BY-4.0", "source":base, "sources":sources,
                "citation":"Casanueva et al. (2020), Efficient Intent Detection with Dual Sentence Encoders.",
                "encoder":routing.ENCODER,"encoder_revision":routing.ENCODER_REVISION,"encoder_license":"Apache-2.0",
                "encoder_files":encoder_checksums,"pooling":"attention-masked mean, L2 normalized",
                "max_length":256,"dimensions":384,"split_seed":routing.SPLIT_SEED,
                "counts":{split:sum(r["split"]==split for r in rows) for split in ("train","validation","review","test")},
                "encoder_cpu_seconds":time.perf_counter()-started,
                "files":{name:routing.checksum(output/name) for name in ("train.csv","test.csv","LICENSE-Banking77.txt","cases.json","embeddings.npy")}}
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    routing.verify_data(output)
    print(json.dumps({"output":str(output),"counts":manifest["counts"],"encoder_cpu_seconds":manifest["encoder_cpu_seconds"]}))


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("data/banking77-v1"))
    parser.add_argument("--model-cache",type=Path,default=Path(".cache/banking77-minilm"))
    args=parser.parse_args()
    prepare(args.output,args.model_cache)
