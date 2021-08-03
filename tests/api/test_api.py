import os

import pytest
from homeassistant.core import HomeAssistant

from custom_components.racelandshop.api.acknowledge_critical_repository import (
    acknowledge_critical_repository,
)
from custom_components.racelandshop.api.check_local_path import check_local_path
from custom_components.racelandshop.api.get_critical_repositories import (
    get_critical_repositories,
)
from custom_components.racelandshop.api.racelandshop_config import racelandshop_config
from custom_components.racelandshop.api.racelandshop_removed import racelandshop_removed
from custom_components.racelandshop.api.racelandshop_repositories import racelandshop_repositories
from custom_components.racelandshop.api.racelandshop_repository import racelandshop_repository
from custom_components.racelandshop.api.racelandshop_repository_data import racelandshop_repository_data
from custom_components.racelandshop.api.racelandshop_settings import racelandshop_settings
from custom_components.racelandshop.api.racelandshop_status import racelandshop_status


@pytest.mark.asyncio
async def test_check_local_path(racelandshop, connection, tmpdir):
    racelandshop.hass = HomeAssistant()
    os.makedirs(tmpdir, exist_ok=True)
    check_local_path(racelandshop.hass, connection, {"path": tmpdir, "id": 1})
    check_local_path(racelandshop.hass, connection, {"id": 1})
    get_critical_repositories(racelandshop.hass, connection, {"id": 1})
    racelandshop_config(racelandshop.hass, connection, {"id": 1})
    racelandshop_removed(racelandshop.hass, connection, {"id": 1})
    racelandshop_repositories(racelandshop.hass, connection, {"id": 1})
    racelandshop_repository(racelandshop.hass, connection, {"id": 1})
    racelandshop_repository_data(racelandshop.hass, connection, {"id": 1})
    racelandshop_settings(racelandshop.hass, connection, {"id": 1})
    racelandshop_status(racelandshop.hass, connection, {"id": 1})

    acknowledge_critical_repository(
        racelandshop.hass, connection, {"repository": "test/test", "id": 1}
    )
