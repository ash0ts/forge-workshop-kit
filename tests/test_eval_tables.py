from copy import deepcopy
from types import SimpleNamespace

import pytest

from forge_workshop_kit.eval_tables import (
    EvalTableNeedsReview,
    eval_table_data,
    publish_eval_table,
    verify_eval_table,
    verify_run_history,
)

ROWS = [
    {'case_id': 'case-a', 'input': {'request': 'A card has not arrived'},
     'prediction': {'intent': 'card_arrival'}, 'target': 'card_arrival',
     'scores': {'correct': True}, 'error': None},
    {'case_id': 'case-b', 'input': {'request': 'An unavailable prediction'},
     'prediction': None, 'target': 'card_arrival',
     'scores': {'correct': None}, 'error': None},
]
MARKER = {'_type': 'eval-table', 'nrows': 2, 'ncols': 7,
          'evaluate_call_id': 'stored-evaluation', 'log_mode': 'IMMUTABLE'}


class Run:
    entity = 'participant'
    project = 'workshop'
    id = 'version-a'

    def __init__(self):
        self.logged = []

    def log(self, data):
        self.logged.append(data)


class Client:
    project_id = 'participant/workshop'

    def __init__(self):
        self.finished = True
        self.examples = []
        self.queries = []
        self.server = SimpleNamespace(calls_query_stream=self.query)
        for row in ROWS:
            self.examples.append(SimpleNamespace(
                op_name='weave:///participant/workshop/op/Evaluation.predict_and_score:version',
                ended_at='now', exception=None,
                inputs={'example': {'case_id': row['case_id'], 'input.request': row['input']['request']}},
                output={'scores': {'error': row['error'], **row['scores']},
                        'output': {'prediction': None,
                                   'prediction.intent': row['prediction']['intent'] if row['prediction'] else None,
                                   'target': row['target'], 'evidence': None}}))
        self.examples.append(SimpleNamespace(op_name='Evaluation.summarize:version'))

    def flush(self):
        pass

    def get_call(self, call_id):
        assert call_id == MARKER['evaluate_call_id']
        return SimpleNamespace(ended_at='now' if self.finished else None, exception=None)

    def get_calls(self, **kwargs):
        pytest.fail('High-level call deserialization would download image files')

    def query(self, kwargs):
        self.queries.append(kwargs)
        if 'call_ids' in kwargs['filter']:
            return [SimpleNamespace(ended_at='now' if self.finished else None, exception=None)]
        return self.examples


@pytest.fixture
def sdk(monkeypatch):
    import wandb
    calls = []

    class Table:
        def __init__(self, **kwargs):
            calls.append(kwargs)

        def to_json(self, run):
            assert len(run.logged) == 1
            return dict(MARKER)

    monkeypatch.setattr(wandb, 'EvalTable', Table)
    return calls


def test_flat_columns_preserve_missing_scores_and_matching_inputs():
    built = eval_table_data(ROWS)
    assert built['input_columns'] == ['case_id', 'input.request']
    assert built['score_columns'] == ['correct', 'error']
    assert 'prediction.intent' in built['output_columns']
    assert 'target' in built['output_columns']
    values = [dict(zip(built['columns'], row)) for row in built['data']]
    assert values[0]['correct'] is True
    assert values[1]['correct'] is None
    changed = deepcopy(ROWS)
    changed[0]['prediction'] = {'intent': 'another-intent'}
    revised = eval_table_data(changed)
    for before, after in zip(built['data'], revised['data']):
        assert before[:len(built['input_columns'])] == after[:len(revised['input_columns'])]


def test_native_image_columns_contain_images_not_file_paths(tmp_path):
    from PIL import Image

    import wandb
    from forge_workshop_kit.media import image_value
    path = tmp_path / 'board.png'
    Image.new('RGB', (3, 3), 'orange').save(path)
    rows = deepcopy(ROWS)
    rows[0]['input']['board'] = image_value(path, 'Example board')
    built = eval_table_data(rows)
    index = built['columns'].index('input.board')
    assert isinstance(built['data'][0][index], wandb.Image)
    assert built['data'][1][index] is None


def test_image_readback_checks_metadata_without_materializing_custom_objects(tmp_path):
    from PIL import Image

    from forge_workshop_kit.media import image_value
    path = tmp_path / 'board.png'
    Image.new('RGB', (3, 3), 'orange').save(path)
    rows, client = deepcopy(ROWS), Client()
    rows[0]['input']['board'] = image_value(path, 'Example board')
    client.examples[0].inputs['example']['input.board'] = {
        '_type': 'CustomWeaveType', 'weave_type': {'type': 'PIL.Image.Image'},
        'files': {'image.png': 'server-content-digest'},
    }
    client.examples[1].inputs['example']['input.board'] = None
    result = verify_eval_table(client, MARKER, rows)
    assert result['verified'] and not result['image_content_verified']
    assert all(query['return_expanded_column_values'] is False for query in client.queries)


@pytest.mark.parametrize('stored_image', [
    None,
    '/tmp/board.png',
    {'_type': 'CustomWeaveType', 'weave_type': {'type': 'PIL.Image.Image'}, 'files': {}},
    {'_type': 'CustomWeaveType', 'weave_type': {'type': 'wave.Wave_read'},
     'files': {'image.png': 'server-content-digest'}},
])
def test_image_readback_rejects_missing_or_invalid_media(tmp_path, stored_image):
    from PIL import Image

    from forge_workshop_kit.media import image_value
    path = tmp_path / 'board.png'
    Image.new('RGB', (3, 3), 'orange').save(path)
    rows, client = deepcopy(ROWS), Client()
    rows[0]['input']['board'] = image_value(path, 'Example board')
    client.examples[0].inputs['example']['input.board'] = stored_image
    client.examples[1].inputs['example']['input.board'] = None
    with pytest.raises(ValueError, match='inputs differ'):
        verify_eval_table(client, MARKER, rows)


def test_duplicate_cases_and_column_collisions_fail_before_publication():
    with pytest.raises(ValueError, match='one saved row'):
        eval_table_data([ROWS[0], ROWS[0]])
    rows = deepcopy(ROWS)
    rows[0]['input'] = {'a.b': 1, 'a': {'b': 2}}
    with pytest.raises(ValueError, match='columns collide'):
        eval_table_data(rows)
    rows = deepcopy(ROWS)
    rows[0]['scores']['nested'] = {'mean': 1}
    with pytest.raises(ValueError, match='scalar or missing'):
        eval_table_data(rows)


def test_sdk_export_saves_marker_before_readback_and_is_reused(sdk):
    run, client, saved = Run(), Client(), []
    receipt = publish_eval_table(run, ROWS, 'routing', save=lambda value: saved.append(deepcopy(value)),
                                 client=client)
    assert [value['status'] for value in saved] == ['writing', 'exported', 'published']
    assert saved[1]['marker'] == MARKER
    assert receipt['verified'] and receipt['row_count'] == 2
    assert sdk[0]['backend'] == 'weave'
    assert sdk[0]['unsupported_media_mode'] == 'raise'
    assert list(run.logged[0]) == ['routing']
    publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=lambda value: None, client=client)
    assert len(sdk) == len(run.logged) == 1
    assert client.queries[1]['filter'] == {'parent_ids': ['stored-evaluation']}
    assert client.queries[1]['return_expanded_column_values'] is False
    assert client.queries[1]['project_id'] == 'participant/workshop'


def test_interrupted_readback_retries_without_export(sdk):
    run, client, receipt = Run(), Client(), {}
    client.finished = False
    with pytest.raises(RuntimeError, match='unfinished'):
        publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=lambda value: None, client=client)
    assert receipt['status'] == 'readback_pending'
    assert receipt['marker'] == MARKER
    client.finished = True
    assert publish_eval_table(run, ROWS, 'routing', receipt=receipt,
                              save=lambda value: None, client=client)['verified']
    assert len(sdk) == len(run.logged) == 1


def test_ambiguous_export_is_not_automatically_repeated(sdk):
    run, client, receipt = Run(), Client(), {}

    def interrupted(data):
        run.logged.append(data)
        raise TimeoutError('Export timed out')

    run.log = interrupted
    with pytest.raises(TimeoutError):
        publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=lambda value: None, client=client)
    assert receipt['status'] == 'uncertain'
    with pytest.raises(EvalTableNeedsReview, match='uncertain outcome'):
        publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=lambda value: None, client=client)
    assert len(sdk) == len(run.logged) == 1


def test_changed_request_cannot_reuse_published_receipt(sdk):
    run, client = Run(), Client()
    receipt = publish_eval_table(run, ROWS, 'routing', save=lambda value: None, client=client)
    revised = deepcopy(ROWS)
    revised[0]['prediction']['intent'] = 'different'
    with pytest.raises(ValueError, match='request changed'):
        publish_eval_table(run, revised, 'routing', receipt=receipt, save=lambda value: None, client=client)
    assert len(sdk) == 1


@pytest.mark.parametrize('change, message', [
    ('missing', 'rows are incomplete'), ('duplicate', 'case identities'), ('score', 'scores differ'),
    ('input', 'inputs differ'), ('output', 'outputs differ'),
])
def test_readback_rejects_missing_duplicate_or_changed_rows(change, message):
    client = Client()
    if change == 'missing':
        client.examples.pop(0)
    elif change == 'duplicate':
        client.examples[1].inputs['example']['case_id'] = 'case-a'
    elif change == 'score':
        client.examples[0].output['scores']['correct'] = False
    elif change == 'input':
        client.examples[0].inputs['example']['input.request'] = 'Changed question'
    else:
        client.examples[0].output['output']['prediction.intent'] = 'Changed prediction'
    with pytest.raises((ValueError, RuntimeError), match=message):
        verify_eval_table(client, MARKER, ROWS)


def test_saved_marker_survives_local_save_error_without_second_export(sdk):
    run, client, receipt = Run(), Client(), {}

    def interrupted(value):
        if value['status'] == 'exported':
            raise OSError('disk is full')

    with pytest.raises(OSError):
        publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=interrupted, client=client)
    assert receipt['marker'] == MARKER
    publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=lambda value: None, client=client)
    assert len(sdk) == len(run.logged) == 1


def test_readback_only_retry_initializes_the_requested_project(sdk, monkeypatch):
    import weave
    run, client = Run(), Client()
    receipt = publish_eval_table(run, ROWS, 'routing', save=lambda value: None, client=client)
    projects = []

    def init(project):
        projects.append(project)
        return client

    monkeypatch.setattr(weave, 'init', init)
    publish_eval_table(run, ROWS, 'routing', receipt=receipt, save=lambda value: None)
    assert projects == ['participant/workshop']
    assert len(sdk) == len(run.logged) == 1


def test_run_history_readback_checks_the_exact_saved_marker():
    paths = []
    stored = SimpleNamespace(scan_history=lambda **kwargs: [{'routing': dict(MARKER)}])

    def read(path):
        paths.append(path)
        return stored

    api = SimpleNamespace(run=read)
    assert verify_run_history('participant/workshop/run', 'routing', MARKER,
                              api=api)['history_verified']
    assert paths == ['participant/workshop/run']
    stored.scan_history = lambda **kwargs: [{'routing': {**MARKER, 'nrows': 1}}]
    with pytest.raises(RuntimeError, match='marker is not stored'):
        verify_run_history('participant/workshop/run', 'routing', MARKER, api=api)
