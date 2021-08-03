import pytest
from aiogithubapi.objects.repository.content import AIOGitHubAPIRepositoryTreeContent

from custom_components.racelandshop.validate.integration.integration_manifest import (
    IntegrationManifest,
)


@pytest.mark.asyncio
async def test_racelandshop_manifest_no_manifest(repository_integration):
    check = IntegrationManifest(repository_integration)
    await check._async_run_check()
    assert check.failed


@pytest.mark.asyncio
async def test_racelandshop_manifest_with_manifest(repository_integration):
    repository_integration.tree = [
        AIOGitHubAPIRepositoryTreeContent(
            {"path": "manifest.json", "type": "file"}, "test/test", "main"
        )
    ]
    check = IntegrationManifest(repository_integration)
    await check._async_run_check()
    assert not check.failed
