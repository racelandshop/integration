import pytest
from homeassistant.config_entries import ConfigEntries, ConfigEntry

from custom_components.racelandshop.operational.setup_actions.sensor import async_add_sensor


@pytest.mark.asyncio
async def test_async_add_sensor_ui(racelandshop, hass):
    hass.data["custom_components"] = None
    hass.config_entries = ConfigEntries(hass, {"racelandshop": {}})
    racelandshop.configuration.config_entry = ConfigEntry(
        1,
        "racelandshop",
        "racelandshop",
        {},
        "user",
        {},
    )
    racelandshop.configuration.config = {"key": "value"}
    await async_add_sensor()


@pytest.mark.asyncio
async def test_async_add_sensor_yaml(racelandshop):
    racelandshop.configuration.config = {"key": "value"}

    racelandshop.configuration.config_type = "yaml"
    await async_add_sensor()
