from forge_workshop_kit import WorkshopSession
from forge_workshop_kit.publication import _workshop_labels, comparison_metrics


def test_source_rehearsal_slug_uses_declared_metrics_without_changing_identity(tmp_path):
    session = WorkshopSession('person/project', 'airline_monitoring', state_dir=tmp_path)
    identity = dict(session.identity)
    assert _workshop_labels(session)['id'] == 'airline-monitoring'
    result = comparison_metrics(session, 'airline-final', [
        {'scores': {'task_success': True, 'execution_errors': 1}, 'error': 0},
        {'scores': {'task_success': False, 'execution_errors': 0}, 'error': 1},
    ])
    assert result['airline-final/task_success'] == .5
    assert result['airline-final/execution_errors'] == .5
    assert session.identity == identity
