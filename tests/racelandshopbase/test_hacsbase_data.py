"""Data Test Suite."""
import pytest
from tests.async_mock import patch
from custom_components.racelandshop.racelandshopbase.data import RacelandshopData


@pytest.mark.asyncio
async def test_racelandshop_data_async_write1(racelandshop, repository):
    data = RacelandshopData()
    repository.data.installed = True
    repository.data.installed_version = "1"
    racelandshop.async_set_repositories([repository])
    await data.async_write()


@pytest.mark.asyncio
async def test_racelandshop_data_async_write2(racelandshop):
    data = RacelandshopData()
    racelandshop.status.background_task = False
    racelandshop.system.disabled = False
    racelandshop.async_set_repositories([])
    await data.async_write()


@pytest.mark.asyncio
async def test_racelandshop_data_restore_write_new(racelandshop):
    data = RacelandshopData()
    await data.restore()
    with patch(
        "custom_components.racelandshop.racelandshopbase.data.async_save_to_store"
    ) as mock_async_save_to_store, patch(
        "custom_components.racelandshop.racelandshopbase.data.async_save_to_store_default_encoder"
    ):
        await data.async_write()
    assert mock_async_save_to_store.called


@pytest.mark.asyncio
async def test_racelandshop_data_restore_write_not_new(racelandshop):
    data = RacelandshopData()

    async def _mocked_loads(hass, key):
        if key == "repositories":
            return {
                "172733314": {
                    "category": "integration",
                    "full_name": "racelandshop/integration",
                    "installed": True,
                },
                "202226247": {
                    "category": "integration",
                    "full_name": "shbatm/racelandshop-isy994",
                    "installed": False,
                },
            }
        elif key == "racelandshop":
            return {"view": "Grid", "compact": False, "onboarding_done": True}
        else:
            raise ValueError(f"No mock for {key}")

    def _mocked_load(*_):
        return {
            "category": "integration",
            "show_beta": True,
        }

    with patch("os.path.exists", return_value=True), patch(
        "custom_components.racelandshop.racelandshopbase.data.async_load_from_store",
        side_effect=_mocked_loads,
    ), patch(
        "custom_components.racelandshop.helpers.functions.store.RACELANDSHOPStore.load",
        side_effect=_mocked_load,
    ):
        await data.restore()

    assert racelandshop.get_by_id("202226247")
    assert racelandshop.get_by_name("shbatm/racelandshop-isy994")

    assert racelandshop.get_by_id("172733314")
    assert racelandshop.get_by_name("racelandshop/integration")

    assert racelandshop.get_by_id("172733314").data.show_beta is True
    assert racelandshop.get_by_id("172733314").data.installed is True

    assert racelandshop.get_by_id("202226247").data.show_beta is True
    assert racelandshop.get_by_id("202226247").data.installed is True

    with patch(
        "custom_components.racelandshop.racelandshopbase.data.async_save_to_store"
    ) as mock_async_save_to_store, patch(
        "custom_components.racelandshop.racelandshopbase.data.async_save_to_store_default_encoder"
    ) as mock_async_save_to_store_default_encoder:
        await data.async_write()
    assert mock_async_save_to_store.called
    assert mock_async_save_to_store_default_encoder.called
