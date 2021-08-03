import pytest

from custom_components.racelandshop.enums import RacelandshopCategory
from custom_components.racelandshop.operational.setup_actions.categories import (
    async_setup_extra_stores,
)


@pytest.mark.asyncio
async def test_extra_stores_python_script(racelandshop):
    await async_setup_extra_stores()
    assert RacelandshopCategory.PYTHON_SCRIPT not in racelandshop.common.categories
    racelandshop.hass.config.components.add("python_script")
    await async_setup_extra_stores()
    assert RacelandshopCategory.PYTHON_SCRIPT in racelandshop.common.categories


@pytest.mark.asyncio
async def test_extra_stores_theme(racelandshop):
    await async_setup_extra_stores()
    assert RacelandshopCategory.THEME not in racelandshop.common.categories
    racelandshop.hass.services._services["frontend"] = {"reload_themes": "dummy"}
    await async_setup_extra_stores()
    assert RacelandshopCategory.THEME in racelandshop.common.categories


@pytest.mark.asyncio
async def test_extra_stores_appdaemon(racelandshop):
    await async_setup_extra_stores()
    assert RacelandshopCategory.APPDAEMON not in racelandshop.common.categories
    racelandshop.configuration.appdaemon = True
    await async_setup_extra_stores()
    assert RacelandshopCategory.APPDAEMON in racelandshop.common.categories


@pytest.mark.asyncio
async def test_extra_stores_netdaemon(racelandshop):
    await async_setup_extra_stores()
    assert RacelandshopCategory.NETDAEMON not in racelandshop.common.categories
    racelandshop.configuration.netdaemon = True
    await async_setup_extra_stores()
    assert RacelandshopCategory.NETDAEMON in racelandshop.common.categories
