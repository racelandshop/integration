import pytest

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException


@pytest.mark.asyncio
async def test_get_package_content(repository_plugin):
    await repository_plugin.get_package_content()


@pytest.mark.asyncio
async def test_validate_repository(repository_plugin):
    with pytest.raises(RacelandshopException):
        await repository_plugin.validate_repository()


@pytest.mark.asyncio
async def test_update_repository(repository_plugin):
    await repository_plugin.update_repository()
