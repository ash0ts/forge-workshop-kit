"""Prepare PCB1 photos and a reproducible CPU feature cache from the authors' archive."""
import argparse
import csv
import hashlib
import json
import shutil
import tarfile
import time
from pathlib import Path
import httpx
import numpy as np
from PIL import Image
from forge_workshop_kit.inspection_encoder import encode, ENCODER_ID, TRANSFORM, WEIGHTS_URL

REVISION = '2a692ab575001cbde74d402d897a7286086c6199'
SOURCE = 'https://amazon-visual-anomaly.s3.us-west-2.amazonaws.com/VisA_20220922.tar'
RAW = f'https://raw.githubusercontent.com/amazon-science/spot-diff/{REVISION}/'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def fetch(url, path):
    path = Path(path)
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream('GET', url, follow_redirects=True, timeout=120) as response:
        response.raise_for_status()
        with path.with_suffix(path.suffix + '.partial').open('wb') as out:
            for chunk in response.iter_bytes():
                out.write(chunk)
    path.with_suffix(path.suffix + '.partial').replace(path)
    return path


def acquire(source):
    if (source / 'pcb1/image_anno.csv').exists():
        return
    archive = fetch(SOURCE, source / 'VisA_20220922.tar')
    with tarfile.open(archive) as bundle:
        for item in bundle:
            name = item.name.removeprefix('./')
            if name.startswith('pcb1/') and item.isfile():
                path = source / name
                if not path.resolve().is_relative_to(source.resolve()):
                    raise ValueError('Unsafe archive path')
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(bundle.extractfile(item).read())


def prepare(source, destination):
    source, destination = Path(source), Path(destination)
    acquire(source)
    destination.mkdir(parents=True, exist_ok=True)
    split_path = fetch(RAW + 'split_csv/2cls_highshot.csv', source / '2cls_highshot.csv')
    rows = [row for row in csv.DictReader(split_path.read_text().splitlines()) if row['object'] == 'pcb1']
    rows.sort(key=lambda row: row['image'])
    rng = np.random.default_rng(2718)
    membership = {}
    for label in ['normal', 'anomaly']:
        pool = sorted(row['image'] for row in rows if row['split'] == 'train' and row['label'] == label)
        rng.shuffle(pool)
        a, b = round(.6 * len(pool)), round(.8 * len(pool))
        for part, names in [('fit', pool[:a]), ('review', pool[a:b]), ('validation', pool[b:])]:
            membership.update({name: part for name in names})
    records = []
    for row in rows:
        original = source / row['image']
        if not original.is_file():
            raise FileNotFoundError(original)
        case = 'pcb1-' + row['label'] + '-' + Path(row['image']).stem
        picture = destination / 'images' / (case + '.jpg')
        picture.parent.mkdir(exist_ok=True)
        with Image.open(original) as im:
            im.convert('RGB').resize((224, 224), Image.Resampling.BILINEAR).save(picture, quality=94)
        mask_name = None
        if row['mask']:
            original_mask = source / row['mask']
            mask = destination / 'masks' / (case + '.png')
            mask.parent.mkdir(exist_ok=True)
            with Image.open(original_mask) as im:
                im.resize((224, 224), Image.Resampling.NEAREST).save(mask)
            mask_name = mask.relative_to(destination).as_posix()
        records.append({'case_id': case, 'label': int(row['label'] == 'anomaly'),
                        'partition': 'test' if row['split'] == 'test' else membership[row['image']],
                        'source_image': row['image'], 'source_sha256': sha(original),
                        'image': picture.relative_to(destination).as_posix(), 'image_sha256': sha(picture),
                        'mask': mask_name, 'mask_sha256': sha(destination / mask_name) if mask_name else None})
    (destination / 'records.json').write_text(json.dumps(records, indent=2) + '\n')
    weights = fetch(WEIGHTS_URL, source / 'resnet18-f37072fd.pth')
    start = time.monotonic()
    # Encode originals, not lossy display JPEGs. Recompute uses retained resized PNG originals below.
    originals = []
    for row in rows:
        path = destination / 'encoder-inputs' / (Path(row['image']).parent.name + '-' + Path(row['image']).stem + '.png')
        path.parent.mkdir(exist_ok=True)
        with Image.open(source / row['image']) as im:
            im.convert('RGB').resize((224, 224), Image.Resampling.BILINEAR).save(path)
        originals.append(path)
    whole, patches = encode(originals, weights, progress=lambda n, total: print(f'Encoded {n}/{total}', flush=True))
    np.savez_compressed(destination / 'features.npz', whole=whole, patches=patches)
    retained = [i for i, row in enumerate(records) if row['partition'] == 'fit'][:4]
    for i, path in enumerate(originals):
        if i not in retained:
            path.unlink()
    (destination / 'encoder-inputs.json').write_text(json.dumps({str(i): originals[i].relative_to(destination).as_posix() for i in retained}))
    license_path = fetch(RAW + 'LICENSE-DATASET', source / 'LICENSE-DATASET')
    shutil.copy2(license_path, destination / 'LICENSE-DATASET')
    files = {p.relative_to(destination).as_posix(): sha(p) for p in destination.rglob('*') if p.is_file() and p.name != 'manifest.json'}
    manifest = {'dataset': 'VisA PCB1', 'version': 'inspection-v1', 'license': 'CC BY 4.0',
                'attribution': 'Zou, Jeong, Pemula, Zhang, and Dabeer. SPot-the-Difference (ECCV 2022).',
                'source': SOURCE, 'source_revision': REVISION, 'official_split': '2cls_highshot.csv',
                'split_sha256': sha(split_path), 'split_seed': 2718, 'encoder': ENCODER_ID,
                'weights_url': WEIGHTS_URL, 'weights_sha256': sha(weights), 'transform': TRANSFORM,
                'feature_seconds': time.monotonic() - start, 'examples': len(records),
                'partition_counts': {p: sum(r['partition'] == p for r in records) for p in ['fit','review','validation','test']},
                'files': files}
    (destination / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default='data/inspection-source')
    parser.add_argument('--output', default='data/inspection-v1')
    args = parser.parse_args()
    manifest = prepare(args.source, args.output)
    print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}, indent=2))
