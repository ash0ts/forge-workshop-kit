from copy import deepcopy
from types import SimpleNamespace

import pytest

from forge_workshop_kit.eval_workspace import comparison_columns, native_panel, publish_workspace
from forge_workshop_kit.session import digest

COLUMNS = {
    'input_columns': ['case_id', 'input.image'],
    'output_columns': ['prediction.image', 'target.image', 'evidence.conversation.conversation_id'],
    'score_columns': ['masked_mae'],
    'image_columns': ['input.image', 'prediction.image', 'target.image'],
}


def test_native_panel_hides_evidence_using_real_legacy_grid_fields():
    panel = native_panel('images', ['global-a', 'global-b'], COLUMNS, ['call-a', 'call-b'])
    assert panel['referenceRunId'] == 'global-a'
    assert panel['comparedEvals'] == [{'runId': 'global-b'}]
    visibility = panel['columnVisibility']
    group = 'output.output.evidence.conversation.conversation_id'
    assert visibility == {group: False, group + '.call-a': False, group + '.call-b': False}
    # Prediction, target, score, and shared input columns stay visible.
    assert not any('prediction' in key or 'target' in key for key in visibility)
    assert panel['columnWidths']['inputs.case_id'] == 180
    assert panel['columnWidths']['inputs.input.image'] == 240
    assert panel['columnWidths']['output.output.prediction.image.call-a'] == 240
    assert panel['columnWidths']['output.output.target.image'] == 240
    assert panel['rowSize'] == 'large'
    assert panel['evalTableType'] == 'eval-table'


def test_saved_column_roles_do_not_need_remote_calls(monkeypatch):
    import weave

    monkeypatch.setattr(weave, 'init', lambda project: pytest.fail('Saved roles need no readback'))
    result = comparison_columns(SimpleNamespace(project='student/workshop'), [
        {'native_transport': {'column_roles': COLUMNS}},
        {'native_transport': {'column_roles': {
            'input_columns': ['case_id'], 'output_columns': ['prediction.status'],
            'score_columns': ['completed'], 'image_columns': [],
        }}},
    ])
    assert result['input_columns'] == ['case_id', 'input.image']
    assert set(result['output_columns']) == set(COLUMNS['output_columns']) | {'prediction.status'}
    assert result['score_columns'] == ['completed', 'masked_mae']


def test_older_receipt_gets_column_names_from_actual_evaluation(monkeypatch):
    import weave

    seen = []

    def read(kwargs):
        seen.append(kwargs)
        return [SimpleNamespace(
            op_name='weave:///student/workshop/op/Evaluation.predict_and_score:version',
            inputs={'example': {'case_id': 'a', 'input.question': 'Help'}},
            output={'output': {'prediction.intent': 'support', 'evidence.span': 'id'},
                    'scores': {'correct': True}})]

    monkeypatch.setattr(weave, 'init', lambda project: SimpleNamespace(
        project_id=project, server=SimpleNamespace(calls_query_stream=read)))
    result = comparison_columns(SimpleNamespace(project='student/workshop'), [
        {'native': {'evaluate_call_id': 'original-evaluation'}},
    ])
    assert seen[0]['filter'] == {'parent_ids': ['original-evaluation']}
    assert result['output_columns'] == ['evidence.span', 'prediction.intent']
    assert result['input_columns'] == ['case_id', 'input.question']


def test_workspace_requires_verified_publication_and_reuses_matching_view():
    session = SimpleNamespace(project='student/workshop', workspace_id='workspace')
    record = {'run_id': 'run-a', 'native': {'evaluate_call_id': 'call-a'},
              'native_transport': {'column_roles': COLUMNS}, 'native_verified': True,
              'native_status': 'unavailable'}
    assert publish_workspace(session, 'images', {'manual': record})['status'] == 'pending'
    record['native_status'] = 'published'
    columns = {key: sorted(values) for key, values in COLUMNS.items()}
    signature = digest({'versions': [['run-a', 'call-a']], 'columns': columns, 'layout_version': 3})
    saved = {'status': 'published', 'signature': signature, 'url': 'https://example.test/view'}
    assert publish_workspace(session, 'images', {'manual': deepcopy(record)}, previous=saved) is saved
