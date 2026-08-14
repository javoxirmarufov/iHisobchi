# coding: utf-8
"""Regression tests for services.task_manager."""

from __future__ import annotations

import asyncio

from services.task_manager import TaskManager


async def _wait_forever() -> None:
    await asyncio.Event().wait()


async def test_add_collision_cancels_rejected_duplicate_and_returns_existing():
    manager = TaskManager()
    existing = asyncio.create_task(_wait_forever(), name="existing")
    duplicate = asyncio.create_task(_wait_forever(), name="duplicate")

    try:
        assert manager.add("background", existing, key="same") is existing

        registered = manager.add("background", duplicate, key="same")
        await asyncio.sleep(0)

        assert registered is existing
        assert manager.get("background", "same") is existing
        assert duplicate.cancelled()
        assert not existing.done()
    finally:
        await manager.shutdown(timeout=0.1)


async def test_spawn_collision_returns_pre_existing_registered_task():
    manager = TaskManager()
    first = manager.spawn(_wait_forever(), name="same", group="background")

    try:
        second = manager.spawn(_wait_forever(), name="same", group="background")
        await asyncio.sleep(0)

        assert second is first
        assert manager.get_all("background") == {"same": first}
        assert manager.stats()["background"] == {"total": 1, "running": 1}
    finally:
        await manager.shutdown(timeout=0.1)


async def test_shutdown_gives_confirmed_voice_tool_time_to_finish():
    manager = TaskManager()
    completed = asyncio.Event()

    async def _finish_action() -> None:
        await asyncio.sleep(0.01)
        completed.set()

    task = manager.spawn(_finish_action(), name="confirmed-action", group="voice_tools")

    await manager.shutdown(timeout=0.15)

    assert completed.is_set()
    assert task.done()
    assert not task.cancelled()


async def test_shutdown_gives_hitl_approval_time_to_finish():
    manager = TaskManager()
    completed = asyncio.Event()

    async def _finish_approval() -> None:
        await asyncio.sleep(0.01)
        completed.set()

    task = manager.spawn(_finish_approval(), name="approved-sign", group="mcp_hitl")

    await manager.shutdown(timeout=0.15)

    assert completed.is_set()
    assert task.done()
    assert not task.cancelled()


async def test_shutdown_cancels_voice_tool_after_bounded_grace_period():
    manager = TaskManager()
    cancelled = asyncio.Event()

    async def _stuck_action() -> None:
        try:
            await asyncio.Event().wait()
        finally:
            cancelled.set()

    task = manager.spawn(_stuck_action(), name="stuck-action", group="voice_tools")

    await manager.shutdown(timeout=0.06)

    assert cancelled.is_set()
    assert task.cancelled()
