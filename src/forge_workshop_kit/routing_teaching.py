"""Free checks, restoration, and downloads for the routing notebook."""
import tarfile
import tempfile
from pathlib import Path

import httpx

from . import routing
from .manifest import get_workshop

STEPS = tuple(tuple(step) for step in get_workshop("banking-routing")["steps"])
DATA_URL = "https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.5.0"
OPENING_REQUEST = {
    "case_id": "official-train/00021", "text": "What is the status of my card's delivery?",
    "label": "card_arrival", "split": "review",
    "source": "https://github.com/PolyAI-LDN/task-specific-datasets",
}

CLASSIFIER_STARTER = '''def make_classifier():
    from sklearn.linear_model import LogisticRegression
    # Fit only the linear classifier. The sentence encoder stays frozen.
    raise NotImplementedError("Return LogisticRegression(C=10, max_iter=1000, random_state=17).")
'''
CLASSIFIER_SOLUTION = CLASSIFIER_STARTER.replace('raise NotImplementedError("Return LogisticRegression(C=10, max_iter=1000, random_state=17).")', 'return LogisticRegression(C=10, max_iter=1000, random_state=17)')
POLICY_STARTER = '''def needs_review(confidence, threshold):
    # A low score sends the request to a person instead of routing automatically.
    raise NotImplementedError("Return a boolean using the threshold.")
'''
POLICY_SOLUTION = '''def needs_review(confidence, threshold):
    return confidence < threshold
'''
VALIDATOR_STARTER = '''def validate_judge(value):
    # Reject missing fields and strings such as "false" masquerading as booleans.
    raise NotImplementedError("Require exactly failed (bool) and reason (nonempty str).")
'''
VALIDATOR_SOLUTION = '''def validate_judge(value):
    if not isinstance(value, dict) or set(value) != {"failed", "reason"}:
        raise ValueError("Return failed and reason.")
    if type(value["failed"]) is not bool or not isinstance(value["reason"], str) or not value["reason"].strip():
        raise ValueError("Use a boolean and a reason.")
    return value
'''
JUDGE_RUBRIC = "A routing failure means that the proposed intent would send this request to the wrong support workflow. Use only the request and intent meanings. A request sent for human review is unresolved, not a proven routing failure. Return JSON with failed (boolean) and reason (short string)."


def functions(source):
    scope = {}
    exec(compile(source, "<routing-exercise>", "exec"), scope)
    return scope


def check_classifier(source):
    import numpy as np
    model = functions(source)["make_classifier"]()
    model.fit(np.array([[0,0],[0,.1],[1,1],[1,.9]]), ["a","a","b","b"])
    assert list(model.predict([[0,0],[1,1]])) == ["a","b"], "The classifier should separate the public practice points."
    assert hasattr(model, "predict_proba"), "The review exercise needs predicted probabilities."
    return {"status":"complete", "predictions":["a","b"]}


def check_policy(source):
    fn=functions(source)["needs_review"]
    assert fn(.2,.5) is True and fn(.9,.5) is False and fn(.5,.5) is False
    return {"status":"complete", "examples":"0.2 goes to review; 0.9 routes; 0.5 routes at a 0.5 threshold."}


def check_validator(source):
    fn=functions(source)["validate_judge"]
    assert fn({"failed":False,"reason":"The intent matches."})["failed"] is False
    for invalid in ({"failed":"false","reason":"No."},{"failed":False},{"failed":True,"reason":""}):
        try: fn(invalid)
        except (ValueError,TypeError,KeyError): continue
        raise AssertionError(f"This malformed result should fail validation: {invalid}")
    return {"status":"complete", "examples":"A boolean false passes; the string false and missing reasons fail."}


def saved(session, name):
    rows=[r for r in session.read()["stages"].values() if r["name"]==name and r["status"]=="complete"]
    return max(rows,key=lambda r:r["ended_at"]) if rows else None


def judge_summary(session):
    """An attempted comparison counts even when the provider returned no judgments."""
    if not session:
        return None
    record = saved(session, "routing/judge/summary")
    if not record or not record["result"].get("human_reviews"):
        return None
    return record


def freeze_prerequisite(session):
    if not baselines_complete(session):
        return "Train the two baseline classifiers first."
    first = saved(session, "routing/baseline/tfidf")
    second = saved(session, "routing/baseline/embedding")
    if first.get("sources", {}).get("classifier.py") != second.get("sources", {}).get("classifier.py"):
        return "The two representations used different classifier code. Restore the matched comparison before freezing."
    if not judge_summary(session):
        return "In Check the automated reviewer, run Compare the judge with up to eight of my reviews. Unavailable judgments are saved and will not block you afterward."
    return None


def baselines_complete(session):
    return bool(session and all(saved(session, "routing/baseline/" + kind) for kind in ("tfidf", "embedding")))


def check_matched_classifier(session, source):
    """Splitting the buttons must not turn a representation test into a settings test."""
    for kind in ("tfidf", "embedding"):
        record = saved(session, "routing/baseline/" + kind)
        if record and record.get("sources", {}).get("classifier.py") != source:
            raise ValueError("Restore the classifier code used for the saved " + kind +
                             " run. Both representations must use the same classifier settings; use a new workspace for another recipe.")


def validation_examples(session, kind="tfidf"):
    record = saved(session, "routing/baseline/" + kind) if session else None
    rows = (record or {}).get("result", {}).get("validation", [])
    return sorted(rows, key=lambda row: (row["prediction"] == row["target"], row["case_id"]))


def prompted_examples(session):
    """The fixed eight-request sample from the saved embedding validation run."""
    record = saved(session, "routing/baseline/embedding") if session else None
    rows = (record or {}).get("result", {}).get("validation", [])
    return sorted(rows, key=lambda row: row["case_id"])[:8]


def prompted_complete(session):
    rows = prompted_examples(session)
    if len(rows) != 8:
        return False
    for row in rows:
        record = saved(session, "routing/judge/prompted/" + row["case_id"])
        if not record or record.get("result", {}).get("case_id") != row["case_id"]:
            return False
    return True


def completed_steps(session):
    if not session: return ()
    names={r["name"] for r in session.read()["stages"].values() if r["status"]=="complete"}
    decision = saved(session, "routing/release/decision")
    rollback = saved(session, "routing/release/rollback")
    release = decision["result"]["release"] if decision else {}
    release_complete = (release.get("decision") == "reject" or bool(
        release.get("decision") == "release" and rollback
        and rollback["result"].get("release", {}).get("previous") == release.get("artifact")
        and rollback["result"].get("checks", {}).get("prediction_parity") is True))
    return [step for step in ("setup","data","baseline","alternative","review","prompted","judge","improve","final","release","report")
            if (bool(judge_summary(session)) if step == "judge" else release_complete if step == "release"
                else baselines_complete(session) if step == "baseline"
                else "routing/baseline/embedding" in names if step == "alternative"
                else prompted_complete(session) if step == "prompted"
                else any(name.startswith("routing/"+step) for name in names))]


def metrics_table(versions):
    labels = {"tfidf": "Word TF–IDF", "embedding": "Frozen MiniLM features", "selected": "Selected version"}
    output = []
    for name, rows in versions.items():
        values = routing.score(rows)
        output.append({"Version": labels.get(name, name), "Macro-F1": round(values["macro_f1"], 4) if values["macro_f1"] is not None else None,
            "Accuracy": round(values["accuracy"], 4) if values["accuracy"] is not None else None,
            "Automatically routed": f"{values['coverage']:.1%}",
            "Accuracy when routed": f"{values['selective_accuracy']:.1%}" if values["selective_accuracy"] is not None else None,
            "Requests": values["count"], "CPU prediction time (s)": round(values.get("latency_seconds", 0), 4)})
    return output


def publication_rows(rows):
    return [{"case_id":r["case_id"],"input":{"request":r["text"]},
             "prediction":{"intent":r["prediction"],"confidence":r["confidence"],"needs_review":r["abstained"]},
             "target":{"intent":r["target"]},"error":float(r["prediction"]!=r["target"]),
             "scores":{"correct":r["prediction"]==r["target"],"abstained":r["abstained"],
                       "latency_seconds":r["latency_seconds"]},"evidence":{}} for r in rows]


def download(destination, *, base_url=DATA_URL):
    destination=Path(destination)
    if (destination/'manifest.json').exists():
        routing.verify_data(destination)
        return destination
    with tempfile.TemporaryDirectory() as directory:
        temporary=Path(directory).resolve()
        expected=httpx.get(base_url+'/banking77-v1.sha256',follow_redirects=True,timeout=30)
        expected.raise_for_status()
        archive=temporary/'banking77-v1.tar.gz'
        with httpx.stream('GET',base_url+'/banking77-v1.tar.gz',follow_redirects=True,timeout=120) as response:
            response.raise_for_status()
            with archive.open('wb') as output:
                for chunk in response.iter_bytes():output.write(chunk)
        if routing.checksum(archive)!=expected.text.split()[0]:
            raise ValueError('Banking77 download checksum mismatch.')
        with tarfile.open(archive) as bundle:
            for entry in bundle.getmembers():
                if not (temporary/entry.name).resolve().is_relative_to(temporary) or entry.issym() or entry.islnk():
                    raise ValueError('Unsafe archive entry.')
            bundle.extractall(temporary,filter='data')
        routing.verify_data(temporary/'banking77-v1')
        import shutil
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(temporary/'banking77-v1',destination)
    return destination
