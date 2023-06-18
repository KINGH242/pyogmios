"""Event emitter playground"""
import asyncio
import logging
import pytest
from pyee import AsyncIOEventEmitter

LOG = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_setup(event_loop):
    """Receive event from emitter and complete future!"""
    LOG.info("1 - start")
    event_emitter = AsyncIOEventEmitter(asyncio.new_event_loop())

    @event_emitter.on("event")
    def async_handler(message):
        LOG.info(">>> %s", message)
        future_result.set_result(message)

    future_result = event_loop.create_future()
    LOG.info("2 - emit event")
    event_emitter.emit("event", "Hi")

    LOG.info(await future_result)
