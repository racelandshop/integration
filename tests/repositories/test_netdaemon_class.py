import pytest

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException


@pytest.mark.asyncio
async def test_async_post_installation(repository_netdaemon):
    await repository_netdaemon.async_post_installation()


@pytest.mark.asyncio
async def test_validate_repository(repository_netdaemon):
    with pytest.raises(RacelandshopException):
        await repository_netdaemon.validate_repository()


@pytest.mark.asyncio
async def test_update_repository(repository_netdaemon):
    await repository_netdaemon.update_repository()
