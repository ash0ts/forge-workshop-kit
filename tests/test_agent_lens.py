import httpx
import pytest

from forge_workshop_kit import WorkshopSession
from forge_workshop_kit import agent_lens as lens


class Native:
    def __init__(self):
        self.row = dict(id='tag-1', name='unrequested-change', criteria='Unrequested flight removed',
                        agent_name_filter=['airline-test'], llm_judge_enabled=True)
        self.calls = 0
        self.results = []

    def tag(self, tag_id):
        return dict(self.row)

    def outcomes(self, ids, agent_name):
        return [dict(tag_id='tag-1', conversation_id='one', source='judge', rationale='Return removed'),
                dict(tag_id='tag-1', conversation_id='two', source='human'),
                dict(tag_id='tag-1', conversation_id='three', source='unrecognized')]

    def alignment(self, tag_id):
        return [dict(id='example-1', conversation_id='one', trace_id='turn-1')]

    def test(self, *args):
        self.calls += 1
        if isinstance(self.results, Exception):
            raise self.results
        return self.results


def test_missing_live_assignment_is_unknown_including_manual_labels(tmp_path):
    session = WorkshopSession('person/project', 'airline-monitoring', state_dir=tmp_path)
    native = Native()
    lens.save_tag_snapshot(session, 'tag-1', 'airline-test', True, client=native)
    result = lens.read_monitoring(session, 'tag-1', iter(['one', 'two', 'three']), 'airline-test', client=native)
    assert [r['prediction'] for r in result['rows']] == [True, None, None]
    assert result['processing_coverage'] is None
    assert result['cost_usd'] is None
    native.row['criteria'] = 'Different rule'
    with pytest.raises(ValueError, match='frozen'):
        lens.read_monitoring(session, 'tag-1', ['one'], 'airline-test', client=native)


def test_native_tag_must_be_workspace_scoped_before_freezing(tmp_path):
    session = WorkshopSession('person/project', 'airline-monitoring', state_dir=tmp_path)
    native = Native()
    native.row['agent_name_filter'] = []
    with pytest.raises(ValueError, match='exact workshop agent'):
        lens.save_tag_snapshot(session, 'tag-1', 'airline-test', client=native)
    native.row['agent_name_filter'] = ['airline-test']
    native.row['llm_judge_enabled'] = False
    assert lens.save_tag_snapshot(session, 'tag-1', 'airline-test', client=native)
    with pytest.raises(ValueError, match='Enable'):
        lens.save_tag_snapshot(session, 'tag-1', 'airline-test', True, client=native)


def test_completed_alignment_no_match_is_negative_and_reused(tmp_path):
    session = WorkshopSession('person/project', 'airline-monitoring', state_dir=tmp_path)
    native = Native()
    first = lens.test_alignment(session, 'tag-1', 'example-1', 'Check the requested itinerary', client=native)
    assert first['status'] == 'complete' and first['prediction'] is False
    assert first['cost_usd'] is None
    assert lens.test_alignment(session, 'tag-1', 'example-1', first['criteria'], client=native) == first
    assert native.calls == 1


def test_uncertain_native_judge_is_not_resent_or_counted_negative(tmp_path):
    session = WorkshopSession('person/project', 'airline-monitoring', state_dir=tmp_path)
    native = Native()
    native.results = TimeoutError('Response lost')
    result = lens.test_alignment(session, 'tag-1', 'example-1', 'Check itinerary', client=native)
    assert result['prediction'] is None and result['status'] == 'unavailable'
    with pytest.raises(RuntimeError, match='not be automatically resent'):
        lens.test_alignment(session, 'tag-1', 'example-1', 'Check itinerary', client=native)
    assert native.calls == 1


def test_client_attaches_project_and_reports_permissions():
    def denied(request):
        assert request.headers['x-wandb-entity'] == 'person'
        assert request.headers['x-wandb-project'] == 'project'
        return httpx.Response(403)
    client = lens.LensClient('person/project', api_key='test-only', transport=httpx.MockTransport(denied))
    try:
        with pytest.raises(PermissionError, match='project permissions'):
            client.tags()
    finally:
        client.close()
