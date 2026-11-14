"""Banking77 classification and reviewed labels, without changing its final partition."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import numpy as np

DATA_REVISION = "57ec275d8078af65b7731c2a98be812d844a6d6b"
ENCODER = "sentence-transformers/all-MiniLM-L6-v2"
ENCODER_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
SPLIT_SEED = 20261114


def checksum(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assign_split(rows, seed=SPLIT_SEED, validation_per_intent=10, review_per_intent=10):
    """Order official training examples within each class before any model runs."""
    assignments = {}
    for label in sorted({row["label"] for row in rows}):
        group = sorted((r for r in rows if r["label"] == label), key=lambda r:
                       hashlib.sha256(f"{seed}/{r['id']}".encode()).hexdigest())
        if len(group) <= validation_per_intent + review_per_intent:
            raise ValueError("Not enough training cases for the declared split.")
        for index, row in enumerate(group):
            assignments[row["id"]] = ("validation" if index < validation_per_intent else
                "review" if index < validation_per_intent + review_per_intent else "train")
    return [{**row, "split": assignments[row["id"]]} for row in rows]


def verify_data(root):
    root = Path(root)
    manifest = json.loads((root / "manifest.json").read_text())
    for name, expected in manifest["files"].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()) or checksum(path) != expected:
            raise ValueError(f"Dataset checksum mismatch: {name}")
    rows = json.loads((root / "cases.json").read_text())
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Case identities are not unique.")
    if any(r["split"] != "test" for r in rows if r["id"].startswith("official-test/")):
        raise ValueError("Official test assignments changed.")
    if manifest.get("dataset_revision") != DATA_REVISION:
        raise ValueError("The Banking77 source revision differs from the workshop.")
    if manifest["encoder_revision"] != ENCODER_REVISION:
        raise ValueError("Cached features use another encoder revision.")
    return manifest


def load_data(root):
    root = Path(root)
    manifest = verify_data(root)
    rows = json.loads((root / "cases.json").read_text())
    features = np.load(root / "embeddings.npy", allow_pickle=False)
    if features.shape != (len(rows), 384) or not np.isfinite(features).all():
        raise ValueError("Cached features do not align with the dataset.")
    return {"rows": rows, "features": features, "manifest": manifest, "root": root}


def partition(data, split):
    indices = [i for i, row in enumerate(data["rows"]) if row["split"] == split]
    return [data["rows"][i] for i in indices], data["features"][indices]


def fit_classifier(data, kind, *, seed=17, C=10.0, reviewed=(), factory=None):
    """Training sees the training partition and accepted review records only."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from threadpoolctl import threadpool_limits

    rows, features = partition(data, "train")
    if reviewed:
        by_id = {r["id"]: (i, r) for i, r in enumerate(data["rows"])}
        additions, vectors, seen = [], [], set()
        for review in reviewed:
            case_id = review["case_id"]
            if case_id in seen:
                raise ValueError("A reviewed case was included more than once.")
            seen.add(case_id)
            index, row = by_id[case_id]
            if row["split"] != "review":
                raise ValueError("Only review-pool cases may extend the training dataset.")
            if not review.get("verified") or review.get("label_source") != "human_review":
                raise ValueError("Training requires an accepted human label.")
            if review["accepted_label"] not in {r["label"] for r in rows}:
                raise ValueError("The reviewed label is outside the taxonomy.")
            additions.append({**row, "label": review["accepted_label"]})
            vectors.append(data["features"][index])
        rows += additions
        features = np.concatenate([features, np.asarray(vectors)])
    head = (factory or (lambda: LogisticRegression(C=C, max_iter=1000, random_state=seed)))()
    start = time.perf_counter()
    if kind == "tfidf":
        model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True), head)
        with threadpool_limits(limits=2):
            model.fit([r["text"] for r in rows], [r["label"] for r in rows])
    elif kind == "embedding":
        with threadpool_limits(limits=2):
            model = head.fit(features, [r["label"] for r in rows])
    else:
        raise ValueError("Choose tfidf or embedding.")
    return {"model": model, "kind": kind, "seed": head.get_params().get("random_state"),
            "C": head.get_params().get("C"), "head_parameters": head.get_params(),
            "training_ids": [r["id"] for r in rows], "training_seconds": time.perf_counter()-start}


def predict(fitted, data, split, *, threshold=0.5):
    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between zero and one.")
    rows, features = partition(data, split)
    start = time.perf_counter()
    scores = fitted["model"].predict_proba([r["text"] for r in rows] if fitted["kind"] == "tfidf" else features)
    latency = time.perf_counter()-start
    order = np.argsort(scores, axis=1)
    classes = fitted["model"].classes_
    return [{"case_id": row["id"], "text": row["text"], "target": row["label"],
             "prediction": str(classes[idx[-1]]), "confidence": float(prob[idx[-1]]),
             "runner_up": str(classes[idx[-2]]), "margin": float(prob[idx[-1]]-prob[idx[-2]]),
             "abstained": bool(prob[idx[-1]] < threshold), "split": split,
             "latency_seconds": latency / max(1, len(rows)), "inference_cost_usd": 0.0,
             "cost_note": "Local classifier inference; notebook compute billed separately."}
            for row, prob, idx in zip(rows, scores, order)]


def score(rows):
    from sklearn.metrics import accuracy_score, f1_score
    if not rows:
        return {"macro_f1": None, "accuracy": None, "coverage": 0., "selective_accuracy": None, "count": 0}
    labels = sorted({r["target"] for r in rows})
    accepted = [r for r in rows if not r["abstained"]]
    return {"macro_f1": float(f1_score([r["target"] for r in rows], [r["prediction"] for r in rows],
                                      labels=labels, average="macro", zero_division=0)),
            "accuracy": float(accuracy_score([r["target"] for r in rows], [r["prediction"] for r in rows])),
            "coverage": len(accepted)/len(rows),
            "selective_accuracy": sum(r["prediction"] == r["target"] for r in accepted)/len(accepted) if accepted else None,
            "count": len(rows), "latency_seconds": sum(r["latency_seconds"] for r in rows)}


def per_intent(rows):
    return [{"intent": label, "cases": len(part), "mistakes": sum(r["prediction"] != r["target"] for r in part),
             "reviewed": sum(r["abstained"] for r in part)}
            for label in sorted({r["target"] for r in rows})
            if (part := [r for r in rows if r["target"] == label])]


def select_review(rows, budget=50):
    if any(r["split"] != "review" for r in rows):
        raise ValueError("Review selection requires the training-derived review pool.")
    return sorted(rows, key=lambda r: (r["margin"], r["case_id"]))[:budget]


def validate_route(value, intents):
    if not isinstance(value, dict) or set(value) != {"intent", "needs_review", "reason"}:
        raise ValueError("Return exactly intent, needs_review, and reason.")
    if value["intent"] not in intents or type(value["needs_review"]) is not bool:
        raise ValueError("Use one known intent and a boolean needs_review.")
    if not isinstance(value["reason"], str) or not value["reason"].strip() or len(value["reason"]) > 1000:
        raise ValueError("Give a short explanation of the routing choice.")
    return value


def route_messages(text, intents):
    return [{"role": "system", "content": "Route a banking support request. Return JSON with intent (one allowed intent), needs_review (boolean), and reason (short string). Do not answer or act on the customer's request. Allowed intents: " + ", ".join(intents)},
            {"role": "user", "content": text}]


def prompted_route(session, stage_id, row, intents):
    from .provider import validated_json
    if row["split"] not in {"validation", "review"}:
        raise ValueError("Prompting exercise uses development cases only.")
    return validated_json(session, stage_id + "/" + row["case_id"],
                          route_messages(row["text"], intents), lambda x: validate_route(x, intents), max_tokens=512)


def validate_judgment(value):
    if not isinstance(value, dict) or set(value) != {"failed", "reason"}:
        raise ValueError("Return exactly failed and reason.")
    if type(value["failed"]) is not bool or not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("Judgment needs a boolean and a reason.")
    return value


def judge_alignment(human, judged):
    """Missing predictions stay unavailable; agreement is separate from task quality."""
    available = [(r, judged[r["case_id"]]) for r in human if judged.get(r["case_id"]) is not None]
    tp = sum(r["failed"] and j["failed"] for r,j in available)
    fp = sum(not r["failed"] and j["failed"] for r,j in available)
    fn = sum(r["failed"] and not j["failed"] for r,j in available)
    return {"reviewed": len(human), "available": len(available), "unavailable": len(human)-len(available),
            "agreement": sum(r["failed"] == j["failed"] for r,j in available)/len(available) if available else None,
            "precision": tp/(tp+fp) if tp+fp else None, "recall": tp/(tp+fn) if tp+fn else None,
            "false_alarms": fp, "missed_failures": fn}
