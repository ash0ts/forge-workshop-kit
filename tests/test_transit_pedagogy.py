"""The opening query and acceptance exercise work before project access."""
from pathlib import Path
from unittest.mock import Mock

from forge_workshop_kit import WorkshopSession, factory_teaching, transit_workshop
from forge_workshop_kit.rehearsal import AuthoredAdapter

ROOT = Path(__file__).resolve().parents[1]


def test_free_opening_and_checked_draft_survive_connection(tmp_path, monkeypatch):
    monkeypatch.setattr('forge_workshop_kit.provider.Provider.complete', Mock(side_effect=AssertionError('Opening is free')))
    runner = AuthoredAdapter(ROOT, 'transit_factory', project='attendee/transit', state=tmp_path, output=lambda _: None)
    assert runner.refresh() == {}
    runner.run('transit_factory/action/try_departure')
    rows = runner.scope['get_output']()['opening departures']['rows']
    assert any(row['trip_id'] == '63926435' for row in rows)
    runner.scope['opening_clock']._update('00:09, after it left')
    runner.run('transit_factory/action/try_departure')
    assert not any(row['trip_id'] == '63926435' for row in runner.scope['get_output']()['opening departures']['rows'])
    runner.scope['acceptance_code']._update(factory_teaching.ACCEPTANCE_SOLUTION)
    runner.run('transit_factory/action/acceptance_check')
    assert runner.scope['get_output']()['acceptance check']['passed']
    assert runner.scope['current_session']() is None
    session = WorkshopSession('attendee/transit', 'transit-factory', state_dir=tmp_path)
    monkeypatch.setattr(WorkshopSession, 'from_environment', lambda *a, **k: session)
    monkeypatch.setattr(session, 'check_access', lambda: {'status': 'passed'})
    monkeypatch.setattr(session, 'restore', lambda: None)
    runner.run('transit_factory/action/connect')
    assert session.get_draft('factory/acceptance') == factory_teaching.ACCEPTANCE_SOLUTION
    assert transit_workshop._checked(session, 'acceptance')
    assert session.read()['requests'] == {}
