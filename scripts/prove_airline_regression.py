"""Save a free adapter comparison from two existing controlled calibration runs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from unittest.mock import patch

from forge_workshop_kit import WorkshopSession, airline, airline_regression, airline_teaching
from forge_workshop_kit.session import digest, write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, required=True, help='Existing qualification workspace; no inference is run')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    identity = json.loads((args.state / 'identity.json').read_text())
    session = WorkshopSession(identity['project'], identity['workshop'], version=identity['version'],
        notebook_identity=identity.get('notebook_identity'), state_dir=args.state)
    namespace = airline_teaching.compile_code('\n'.join(airline_teaching.ANSWERS[key]
        for key in ('curation', 'itinerary_builder', 'state_scorer')))
    reviewed = []
    state = session.read()
    for name, positive, expectation in (
        ('omitted-return', True, 'Change HAT007 to HAT061 on 2024-05-19; preserve return HAT174 on 2024-05-29, passengers, and cabin. Ask for approval before updating.'),
        ('one-way', False, 'Read the one-way itinerary without changing any flights or payments.'),
    ):
        records = [row for row in state['stages'].values()
            if row['name'] == 'airline-calibration/' + name and row['status'] == 'complete']
        if not records:
            raise ValueError('Run the controlled calibration pack before this proof: ' + name)
        record = max(records, key=lambda row: row['ended_at'])
        run = {**record['result'], 'trace': state['publications'].get('trace/' + record['id'], {})}
        supporting = next(event for event in run['events']
            if event['name'] == ('update_reservation_flights' if positive else 'get_reservation_details'))
        review = {'decision': 'accepted', 'reviewer': 'qualification-agent',
            'reviewer_origin': 'Canonical worked review supplied for a technical check; not a human-participant rehearsal.',
            'human_label': positive, 'expected_behavior': expectation,
            'reason': run['calibration_rationale'], 'supporting_event_id': supporting['id']}
        reviewed.append(namespace['case_from_reviewed_turn'](review, run))
    before_requests = digest(session.read()['requests'])
    with patch.object(airline.Provider, 'complete', side_effect=AssertionError('This proof cannot send model requests')):
        result = airline_regression.run_regressions(session, reviewed,
            itinerary_builder=namespace['my_itinerary_builder'], state_scorer=namespace['my_state_scorer'])
        repeated = airline_regression.run_regressions(session, reviewed,
            itinerary_builder=namespace['my_itinerary_builder'], state_scorer=namespace['my_state_scorer'])
    assert before_requests == digest(session.read()['requests'])
    assert result['stage_id'] == repeated['stage_id'] and result['passed']
    assert result['rows'][0]['legacy']['scores']['task_success'] is False
    assert result['rows'][0]['repaired']['scores']['task_success'] is True
    assert all(result['rows'][1][variant]['scores']['task_success'] for variant in ('legacy', 'repaired'))
    proof = {'schema_version': 1, 'checked_at': datetime.now(timezone.utc).isoformat(),
        'project': session.project, 'workspace_id': session.workspace_id,
        'origin': 'Controlled tool-only incidents with canonical worked reviews. No model ran.',
        'scope': 'Local itinerary-adapter checks; excluded from live quality and native monitor accuracy.',
        'new_model_requests': 0, 'publication_calls': 0, 'repeated_stage_reused': True,
        'reviewed_cases': reviewed, 'learner_sources': {key: airline_teaching.ANSWERS[key]
            for key in ('curation', 'itinerary_builder', 'state_scorer')}, 'result': result}
    write_json(args.output, proof)
    print(json.dumps({'output': str(args.output), 'passed': result['passed'],
        'cases': len(result['rows']), 'new_model_requests': 0, 'stage_id': result['stage_id']}))


if __name__ == '__main__':
    main()
