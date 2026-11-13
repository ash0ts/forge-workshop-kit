import asyncio
from contextvars import ContextVar

import pytest

from forge_workshop_kit.execution import run_async


def test_async_sdk_inside_notebook_keeps_context_and_runs_once():
    project = ContextVar('project', default='missing')
    calls = []

    async def sdk_call():
        calls.append(project.get())
        await asyncio.sleep(0)
        return project.get()

    async def notebook_cell():
        project.set('participant/solar')
        assert run_async(sdk_call) == 'participant/solar'

    asyncio.run(notebook_cell())
    assert calls == ['participant/solar']


def test_async_sdk_propagates_errors_without_retrying():
    calls = []

    async def unavailable():
        calls.append(1)
        raise PermissionError('publication unavailable')

    with pytest.raises(PermissionError, match='publication unavailable'):
        run_async(unavailable)
    assert calls == [1]
