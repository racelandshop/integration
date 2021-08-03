import pytest

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException


@pytest.mark.asyncio
async def test_installation_method(repository):
    with pytest.raises(RacelandshopException):
        await repository.async_install()
    repository.content.path.local = ""

    with pytest.raises(RacelandshopException):
        await repository.async_install()

    # repository.can_install = True

    await repository._async_post_install()
