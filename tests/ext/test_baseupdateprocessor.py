#!/usr/bin/env python

import asyncio
import pytest
from asyncio import Queue
from telegram import Update
from telegram.ext import CallbackContext, SimpleUpdateProcessor
from tests.auxil.asyncio_helpers import call_after
from tests.auxil.slots import mro_slots


@pytest.fixture()
def mock_processor():
    class MockProcessor(SimpleUpdateProcessor):
        test_flag = False

        async def do_process_update(self, update: Update, coroutine):
            await coroutine
            self.test_flag = True

    return MockProcessor(5)


class TestSimpleUpdateProcessor:
    def test_slot_behaviour(self):
        inst = SimpleUpdateProcessor(1)
        slots = set(inst.__slots__)
        for attr in inst.__slots__:
            assert getattr(inst, attr, "err") != "err", f"got extra slot '{attr}'"
        assert len(slots) == len(mro_slots(inst)), "duplicate slot"

    @pytest.mark.parametrize("concurrent_updates", [-1, 0])
    def test_init(self, concurrent_updates):
        with pytest.raises(ValueError, match="must be a positive integer"):
            SimpleUpdateProcessor(concurrent_updates)

    async def test_process_update(self, mock_processor):
        """Test that process_update calls do_process_update."""
        update = Update(1)

        async def coroutine():
            pass

        await mock_processor.process_update(update, coroutine())
        # This flag is set in the mock processor in do_process_update, telling us that
        # do_process_update was called.
        assert mock_processor.test_flag

    async def test_do_process_update(self):
        """Test that do_process_update calls the coroutine."""
        processor = SimpleUpdateProcessor(1)
        update = Update(1)
        test_flag = False

        async def coroutine():
            nonlocal test_flag
            test_flag = True

        await processor.do_process_update(update, coroutine())
        assert test_flag

    async def test_max_concurrent_updates_enforcement(self, mock_processor):
        """Test that max_concurrent_updates is enforced, i.e. that the processor will run
        at most max_concurrent_updates coroutines at the same time."""
        count = 2 * mock_processor.max_concurrent_updates
        events = {i: asyncio.Event() for i in range(count)}
        queue = Queue()
        for event in events.values():
            await queue.put(event)

        async def callback():
            await asyncio.sleep(0.5)
            (await queue.get()).set()

        # We start several calls to `process_update` at the same time, each of them taking
        # 0.5 seconds to complete. We know that they are completed when the corresponding
        # event is set.
        tasks = [
            asyncio.create_task(mock_processor.process_update(update=_, coroutine=callback()))
            for _ in range(count)
        ]

        # Right now we expect no event to be set
        for i in range(count):
            assert not events[i].is_set()

        # After 0.5 seconds (+ some buffer), we expect that exactly max_concurrent_updates
        # events are set.
        await asyncio.sleep(0.75)
        for i in range(mock_processor.max_concurrent_updates):
            assert events[i].is_set()
        for i in range(
            mock_processor.max_concurrent_updates,
            count,
        ):
            assert not events[i].is_set()

        # After wating another 0.5 seconds, we expect that the next max_concurrent_updates
        # events are set.
        await asyncio.sleep(0.5)
        for i in range(count):
            assert events[i].is_set()

        # Sanity check: we expect that all tasks are completed.
        await asyncio.gather(*tasks)

    async def test_context_manager(self, monkeypatch, mock_processor):
        self.test_flag = set()

        async def after_initialize(*args, **kwargs):
            self.test_flag.add("initialize")

        async def after_shutdown(*args, **kwargs):
            self.test_flag.add("stop")

        monkeypatch.setattr(
            SimpleUpdateProcessor,
            "initialize",
            call_after
