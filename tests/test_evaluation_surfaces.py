"""Exercise publication reads saved work and exposes verified native destinations."""
import ast
import importlib
from pathlib import Path
import sys
from types import SimpleNamespace

from forge_workshop_kit import WorkshopSession, ui

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))


def authored_function(module, name, namespace):
    cells = importlib.import_module(module).cells
    source = next(cell.code for cell in cells if f'def {name}(' in cell.code)
    function = next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name)
    exec(compile(ast.Module(body=[function], type_ignores=[]), '<authored notebook>', 'exec'), namespace)
    return namespace[name]


def test_native_links_require_success_and_keep_task_names_separate(tmp_path):
    session = WorkshopSession('learner/project', 'solar-autoresearch', state_dir=tmp_path)
    records = {}
    for task in ('images', 'measurements'):
        name = f'solar-{task}-final'
        receipt = {'persistence': {'comparison_name': name, 'native_status': 'published',
            'native_url': f'https://forge.example/{task}/results',
            'native_comparison_url': f'https://forge.example/{task}/compare', 'weave_status': 'published'}}
        records[task] = receipt
        with session.transaction() as state:
            state['publications']['comparison/' + task] = receipt
    links = {key: value for receipt in records.values() for key, value in ui.comparison_links(receipt).items()}
    assert len(links) == 4
    assert links['Solar images · final · Compare in EvalTables'].endswith('/images/compare')
    assert links['GOES measurements · final · Compare in EvalTables'].endswith('/measurements/compare')
    records['images']['persistence']['native_status'] = 'unavailable'
    assert not ui.comparison_links(records['images'])
    mo = SimpleNamespace(md=lambda x: x, Html=lambda x: x, ui=SimpleNamespace(table=lambda x, **kw: x),
                         vstack=lambda x: x, callout=lambda x, **kw: x, accordion=lambda x: x)
    rendered = ui.publication(mo, session, names=('solar-images-final',))
    assert '/images/compare' in rendered[1]
    assert '/measurements/' not in rendered[1]


def test_routing_publication_uses_saved_reviews_and_preserves_unavailable_judgments():
    reviews = {
        'r1': {'case_id': 'c1', 'id': 'r1', 'proposed_label': 'lost', 'accepted_label': 'late',
               'dataset_version': 'dataset1', 'evidence': {'text': 'My card has not arrived'}},
        'r2': {'case_id': 'c2', 'id': 'r2', 'proposed_label': 'broken', 'accepted_label': 'broken',
               'dataset_version': 'dataset1', 'evidence': {'text': 'My card does not work'}},
    }
    summary = {'config': {'reviews': ['r1', 'r2']}, 'result': {
        'human_reviews': [{'case_id': 'c1', 'failed': True}, {'case_id': 'c2', 'failed': False}],
        'predictions': {'c1': {'failed': False, 'reason': 'A wrong judgment'}, 'c2': None},
        'attempts': [{'case_id': 'c1', 'stage_id': 'j1'}, {'case_id': 'c2', 'stage_id': 'j2'}]}}
    session = SimpleNamespace(read=lambda: {'reviews': reviews, 'publications': {
        'trace/j1': {'url': 'https://forge.example/j1', 'verified': True}}})
    publications = []
    namespace = {'teaching': SimpleNamespace(saved=lambda _session, name: summary if name == 'routing/judge/summary' else None),
                 'publish_comparison': lambda session, name, versions: publications.append((name, versions)) or versions}
    publish = authored_function('routing_cells', 'publish_routing_results', namespace)
    publish(session, include_final=False)
    publish(session, include_final=False)
    assert publications[0] == publications[1]
    name, versions = publications[0]
    assert name == 'banking-routing-judge-alignment'
    rows = versions['automated-judge']
    assert rows[0]['input']['request'] == 'My card has not arrived'
    assert rows[0]['target']['accepted_intent'] == 'late'
    assert rows[0]['error'] == 1.0
    assert rows[0]['evidence']['agent_lens'] == 'https://forge.example/j1'
    assert rows[1]['prediction']['status'] == 'unavailable'
    assert rows[1]['error'] is None
    assert rows[1]['scores']['agrees_with_review'] is None


def test_pending_retry_uploads_saved_manual_comparison_without_employee_calls():
    cells = importlib.import_module('pending_cells').cells
    source = next(cell.code for cell in cells if cell.code.startswith('mo.stop(not pending_retry.value)'))
    records = {'pending/development-manual-comparison': {'result': {'rows': {'starting': [{'case_id': 'a'}], 'manual': [{'case_id': 'a'}]}}},
               'pending/final-comparison': {'result': {'rows': {'agent': [{'case_id': 'b'}]}}}}
    session = SimpleNamespace(retry_publication=lambda: None, read=lambda: {'stages': {}})
    published = []
    namespace = {'mo': SimpleNamespace(stop=lambda value: None), 'pending_retry': SimpleNamespace(value=True),
                 'get_pending': lambda: {'session': session},
                 'teaching': SimpleNamespace(functions=lambda _: {}, restore=lambda _: {}, latest=lambda _, name: records.get(name)),
                 'pending_publish': lambda _, name, rows: published.append((name, rows)), 'pending_refresh': lambda _: None}
    exec(compile(source, '<authored retry>', 'exec'), namespace)
    assert len(published) == 2
    assert set(published[0][1]) == {'starting', 'manual'}
    assert published[1][0] == 'pending-final'
