import json
import os

import pytest

from custom_components.racelandshop.operational.setup_actions.frontend import (
    async_setup_frontend,
)


@pytest.mark.asyncio
async def test_frontend_setup(racelandshop, tmpdir):
    racelandshop.core.config_path = tmpdir

    content = {}

    os.makedirs(f"{racelandshop.core.config_path}/custom_components/racelandshop", exist_ok=True)

    with open(
        f"{racelandshop.core.config_path}/custom_components/racelandshop/manifest.json", "w"
    ) as manifest:
        manifest.write(json.dumps(content))
    await async_setup_frontend()
