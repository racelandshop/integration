import pytest

from custom_components.racelandshop.share import SHARE
from custom_components.racelandshop.validate import (
    async_initialize_rules,
    async_run_repository_checks,
)


@pytest.mark.asyncio
async def test_async_initialize_rules(racelandshop):

    await async_initialize_rules()


@pytest.mark.asyncio
async def test_async_run_repository_checks(racelandshop, repository_integration):
    await async_run_repository_checks(repository_integration)

    racelandshop.system.action = True
    racelandshop.system.running = True
    repository_integration.tree = []
    with pytest.raises(SystemExit):
        await async_run_repository_checks(repository_integration)

    racelandshop.system.action = False
    SHARE["rules"] = {}
    await async_run_repository_checks(repository_integration)
    racelandshop.system.running = False
