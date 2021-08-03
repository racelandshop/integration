import pytest

from custom_components.racelandshop.operational.setup_actions.websocket_api import (
    async_setup_racelandshop_websockt_api,
)


@pytest.mark.asyncio
async def test_async_setup_racelandshop_websockt_api():
    await async_setup_racelandshop_websockt_api()
