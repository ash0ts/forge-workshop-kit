"""Human review records. A model suggestion is not an accepted training label."""

import time

from .session import digest


def save_review(session, *, case_id, proposed_label, accepted_label, reviewer,
                dataset_version, split='review', evidence=None, verified=True):
    if split not in ('train', 'review', 'development'):
        raise ValueError('Review training or development examples. Keep final-test labels out.')
    if not all(isinstance(v, str) and v.strip() for v in (case_id, reviewer, dataset_version)):
        raise ValueError('Record the case, reviewer and exact dataset version.')
    if verified and accepted_label is None:
        raise ValueError('Choose a label before marking a review verified.')
    record = dict(case_id=case_id, proposed_label=proposed_label, accepted_label=accepted_label,
                  reviewer=reviewer, dataset_version=dataset_version, split=split,
                  evidence=evidence or {}, verified=bool(verified),
                  label_source='human_review' if verified else 'unverified_suggestion')
    signature = digest(record)
    with session.transaction() as state:
        reviews = state.setdefault('reviews', {})
        history = [r for r in reviews.values() if r['case_id'] == case_id
                   and r['dataset_version'] == dataset_version]
        previous = max(history, key=lambda r: r['created_at']) if history else None
        if previous and previous.get('decision_fingerprint') == signature:
            return previous
        record['previous'] = previous['id'] if previous else None
        record['decision_fingerprint'] = signature
        record['id'] = digest([signature, record['previous']])[:32]
        record['created_at'] = time.time()
        reviews[record['id']] = record
    return record


def reviewed_dataset(session, dataset_version):
    """Return the latest decision per case, including later withdrawals of a label."""
    latest = {}
    for row in sorted(session.read().get('reviews', {}).values(), key=lambda r: r['created_at']):
        if row['dataset_version'] == dataset_version:
            latest[row['case_id']] = row
    rows = [r for r in latest.values() if r['verified'] and r['accepted_label'] is not None]
    return {'version': digest(rows), 'source_dataset': dataset_version, 'rows': rows}


def judge_agreement(reviews, predictions):
    """Score a judge on reviewed cases; missing or malformed judgments stay missing."""
    paired = []
    for review in reviews:
        if review.get('verified') and review['case_id'] in predictions:
            prediction = predictions[review['case_id']]
            if prediction is not None:
                paired.append((review['accepted_label'], prediction))
    labels = sorted({str(v) for pair in paired for v in pair})
    confusion = {label: {other: 0 for other in labels} for label in labels}
    for human, judge in paired:
        confusion[str(human)][str(judge)] += 1
    planned = sum(bool(r.get('verified')) for r in reviews)
    return {'reviewed': planned, 'available': len(paired), 'unavailable': planned-len(paired),
            'agreement': sum(a == b for a, b in paired)/len(paired) if paired else None,
            'confusion': confusion}
