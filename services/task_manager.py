# coding: utf-8
"""BusinessHub v3 - Unified task lifecycle manager.

Replaces scattered ``_background_tasks``, ``_signing_tasks``, ``_monitoring_tasks``
dicts/sets with a single registry grouped by purpose.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional

log = logging.getLogger("task_manager")

_IRREVERSIBLE_DRAIN_GROUPS = ("voice_tools", "mcp_hitl")


class TaskManager:
    """Manages named groups of asyncio.Tasks with keyed lookup.

    Groups:
        - "background"  — long-running daemon-like tasks (token cleanup, signing cleanup)
        - "signing"     — per-document signing tasks (fire-and-forget)
        - "monitoring"  — per-business bank monitoring loops (keyed by bank_{uid}_{business_id})
    """

    def __init__(self) -> None:
        self._groups: Dict[str, Dict[str, asyncio.Task]] = {}

    def _ensure_group(self, group: str) -> Dict[str, asyncio.Task]:
        if group not in self._groups:
            self._groups[group] = {}
        return self._groups[group]

    def _on_task_done(self, group: str, key: str, task: asyncio.Task) -> None:
        """Auto-remove finished tasks and log exceptions."""
        grp = self._groups.get(group)
        if grp and grp.get(key) is task:
            grp.pop(key, None)
        if task.cancelled():
            return
        try:
            exc = task.exception()
            if exc:
                log.error("Task %s/%s failed: %s", group, key, exc, exc_info=exc)
        except asyncio.CancelledError:
            pass

    def add(self, group: str, task: asyncio.Task, key: Optional[str] = None) -> asyncio.Task:
        """Register a task under *group* with optional *key*.

        If *key* is None, uses the task's id as key.
        If a task with the same key already exists and is not done, the incoming
        *task* is cancelled and the existing one is returned (so a duplicate
        never keeps running untracked outside the registry).

        Thread-safety note: this method is intentionally synchronous (not async)
        Because it contains no ``await`` points, it executes atomically within a
        single iteration of the asyncio event loop — no other coroutine can
        interleave.  Converting it to async would break all existing callers
        (which call it without ``await``) for zero concurrency benefit.
        """
        if key is None:
            key = str(id(task))
        grp = self._ensure_group(group)
        existing = grp.get(key)
        if existing and not existing.done():
            log.warning("Task %s/%s already exists and is running, not replacing", group, key)
            # Cancel the rejected duplicate so it does not run untracked (no
            # done-callback, never cancelled on shutdown) alongside the winner.
            if task is not existing and not task.done():
                task.cancel()
            return existing
        grp[key] = task
        task.add_done_callback(lambda t: self._on_task_done(group, key, t))
        return task

    def get(self, group: str, key: str) -> Optional[asyncio.Task]:
        """Get a task by group and key."""
        grp = self._groups.get(group, {})
        return grp.get(key)

    def get_all(self, group: str) -> Dict[str, asyncio.Task]:
        """Get all tasks in a group (snapshot)."""
        return dict(self._groups.get(group, {}))

    def remove(self, group: str, key: str) -> Optional[asyncio.Task]:
        """Remove (but don't cancel) a task from the registry. Returns the task."""
        grp = self._groups.get(group, {})
        return grp.pop(key, None)

    async def cancel_group(self, group: str, timeout: float = 10.0) -> int:
        """Cancel all tasks in a group and wait up to *timeout* seconds.

        Returns the number of tasks that were cancelled.
        """
        grp = self._groups.get(group, {})
        if not grp:
            return 0

        tasks = list(grp.values())
        for t in tasks:
            if not t.done():
                t.cancel()

        if tasks:
            done, pending = await asyncio.wait(tasks, timeout=timeout)
            if pending:
                log.warning("cancel_group(%s): %d tasks did not finish within %.0fs", group, len(pending), timeout)
        grp.clear()
        return len(tasks)

    async def shutdown(self, timeout: float = 15.0) -> None:
        """Stop tracked tasks within one bounded shutdown budget.

        Confirmed voice tools may already be changing external state. Give
        those tasks a short grace period before cancellation so a routine
        deploy does not turn a successful action into an ambiguous result.
        The grace period is part of (not added to) *timeout*.
        """
        loop = asyncio.get_running_loop()
        deadline = loop.time() + max(0.0, timeout)

        irreversible_tasks = [
            task
            for group in _IRREVERSIBLE_DRAIN_GROUPS
            for task in self._groups.get(group, {}).values()
            if not task.done()
        ]
        if irreversible_tasks and timeout > 0:
            drain_timeout = min(10.0, timeout * 2 / 3)
            log.info(
                "TaskManager shutdown: draining %d confirmed irreversible task(s) for up to %.1fs",
                len(irreversible_tasks),
                drain_timeout,
            )
            _done, pending = await asyncio.wait(irreversible_tasks, timeout=drain_timeout)
            if pending:
                log.warning(
                    "TaskManager shutdown: %d irreversible task(s) still running after %.1fs grace period",
                    len(pending),
                    drain_timeout,
                )

        all_tasks = []
        for group_name in list(self._groups.keys()):
            grp = self._groups.get(group_name, {})
            for t in list(grp.values()):
                if not t.done():
                    t.cancel()
                all_tasks.append(t)

        if all_tasks:
            remaining = max(0.0, deadline - loop.time())
            done, pending = await asyncio.wait(all_tasks, timeout=remaining)
            if pending:
                log.warning("TaskManager shutdown: %d task(s) did not finish within %.0fs", len(pending), timeout)
                for t in pending:
                    log.warning("  Unfinished: %s", t.get_name())
            log.info("TaskManager shutdown complete (%d done, %d timed out)", len(done), len(pending))

        self._groups.clear()

    def stats(self) -> dict:
        """Return summary stats for all groups."""
        result = {}
        for group, tasks in self._groups.items():
            running = sum(1 for t in tasks.values() if not t.done())
            result[group] = {"total": len(tasks), "running": running}
        return result

    def spawn(self, coro, *, name: str, group: str = "background") -> asyncio.Task:
        """Create an asyncio.Task from *coro* and register it.

        Convenience wrapper: equivalent to
        ``task_manager.add(group, asyncio.create_task(coro, name=name), name)``
        but expresses intent ("run this coroutine as a tracked background
        task") in a single call.
        """
        task = asyncio.create_task(coro, name=name)
        # Return the actually-registered task: on a key collision add() cancels
        # *task* and returns the pre-existing one, so callers must observe that.
        return self.add(group, task, name)


# Singleton
task_manager = TaskManager()
