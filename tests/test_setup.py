"""RACELANDSHOP Setup Test Suite."""
# pylint: disable=missing-docstring
import os

import pytest

from custom_components.racelandshop.operational.setup_actions.clear_storage import (
    async_clear_storage,
)


@pytest.mark.asyncio
async def test_clear_storage(racelandshop):
    os.makedirs(f"{racelandshop.core.config_path}/.storage")
    with open(f"{racelandshop.core.config_path}/.storage/racelandshop", "w") as h_f:
        h_f.write("")
    assert os.path.exists(f"{racelandshop.core.config_path}/.storage/racelandshop")

    await async_clear_storage()
    assert not os.path.exists(f"{racelandshop.core.config_path}/.storage/racelandshop")

    os.makedirs(f"{racelandshop.core.config_path}/.storage/racelandshop")
    assert os.path.exists(f"{racelandshop.core.config_path}/.storage/racelandshop")

    await async_clear_storage()
    assert os.path.exists(f"{racelandshop.core.config_path}/.storage/racelandshop")
