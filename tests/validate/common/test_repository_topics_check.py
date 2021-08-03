import pytest

from custom_components.racelandshop.validate.common.repository_topics import RepositoryTopics


@pytest.mark.asyncio
async def test_repository_no_topics(repository):
    repository.data.topics = []
    check = RepositoryTopics(repository)
    await check._async_run_check()
    assert check.failed


@pytest.mark.asyncio
async def test_repository_racelandshop_topics(repository):
    repository.data.topics = ["test"]
    check = RepositoryTopics(repository)
    await check._async_run_check()
    assert not check.failed
