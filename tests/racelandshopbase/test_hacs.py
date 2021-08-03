# pylint: disable=missing-module-docstring, missing-function-docstring
import pytest

from custom_components.racelandshop.enums import RacelandshopStage


@pytest.mark.asyncio
async def test_racelandshop(racelandshop, repository, tmpdir):
    racelandshop.hass.config.config_dir = tmpdir

    racelandshop.async_set_repositories([])
    assert racelandshop.get_by_id(None) is None

    repository.data.id = "1337"

    racelandshop.async_set_repositories([repository])
    assert racelandshop.get_by_id("1337").data.full_name == "test/test"
    assert racelandshop.get_by_id("1337").data.full_name_lower == "test/test"

    racelandshop.async_set_repositories([])
    assert racelandshop.get_by_name(None) is None

    racelandshop.async_set_repositories([repository])
    assert racelandshop.get_by_name("test/test").data.id == "1337"
    assert racelandshop.is_known("1337")

    await racelandshop.prosess_queue()
    await racelandshop.clear_out_removed_repositories()


@pytest.mark.asyncio
async def test_add_remove_repository(racelandshop, repository, tmpdir):
    racelandshop.hass.config.config_dir = tmpdir

    repository.data.id = "0"
    racelandshop.async_add_repository(repository)

    with pytest.raises(ValueError):
        racelandshop.async_add_repository(repository)

    racelandshop.async_set_repository_id(repository, "42")

    # Once its set, it should never change
    with pytest.raises(ValueError):
        racelandshop.async_set_repository_id(repository, "30")

    # Safe to set it again
    racelandshop.async_set_repository_id(repository, "42")

    assert racelandshop.get_by_name("test/test") is repository
    assert racelandshop.get_by_id("42") is repository

    racelandshop.async_remove_repository(repository)
    assert racelandshop.get_by_name("test/test") is None
    assert racelandshop.get_by_id("42") is None

    # Verify second removal does not raise
    racelandshop.async_remove_repository(repository)


@pytest.mark.asyncio
async def test_set_stage(racelandshop):
    assert racelandshop.stage == RacelandshopStage.SETUP
    await racelandshop.async_set_stage(RacelandshopStage.RUNNING)
    assert racelandshop.stage == RacelandshopStage.RUNNING
