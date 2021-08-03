import pytest
from aiogithubapi.objects.repository.content import AIOGitHubAPIRepositoryTreeContent

from custom_components.racelandshop.validate.common.racelandshop_manifest import RacelandshopManifest


@pytest.mark.asyncio
async def test_racelandshop_manifest_no_manifest(repository):
    check = RacelandshopManifest(repository)
    await check._async_run_check()
    assert check.failed


@pytest.mark.asyncio
async def test_racelandshop_manifest_with_manifest(repository):
    repository.tree = [
        AIOGitHubAPIRepositoryTreeContent(
            {"path": "racelandshop.json", "type": "file"}, "test/test", "main"
        )
    ]
    check = RacelandshopManifest(repository)
    await check._async_run_check()
    assert not check.failed
