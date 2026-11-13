"""Run asynchronous SDK operations from synchronous notebook exercises."""
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context


def run_async(factory):
    """Create and await the coroutine once, even inside marimo's active event loop."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(factory())
    context = copy_context()
    with ThreadPoolExecutor(max_workers=1, thread_name_prefix='workshop-sdk') as executor:
        return executor.submit(context.run, lambda: asyncio.run(factory())).result()
