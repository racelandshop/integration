import pytest

from custom_components.racelandshop.validate.common.repository_description import (
    RepositoryDescription,
)


@pytest.mark.asyncio
async def test_repository_no_description(repository):
    repository.data.description = ""
    check = RepositoryDescription(repository)
    await check._async_run_check()
    assert check.failed


@pytest.mark.asyncio
async def test_repository_racelandshop_description(repository):
    check = RepositoryDescription(repository)
    await check._async_run_check()
    assert not check.failed
