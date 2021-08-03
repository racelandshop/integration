"""Set up some common test helper things."""
import asyncio
import logging

import pytest
from homeassistant.exceptions import ServiceNotFound
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.runner import HassEventLoopPolicy

from custom_components.racelandshop.racelandshopbase.configuration import Configuration
from custom_components.racelandshop.racelandshopbase.racelandshop import Racelandshop
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository
from custom_components.racelandshop.helpers.functions.version_to_install import (
    version_to_install,
)
from custom_components.racelandshop.repositories import (
    RacelandshopAppdaemon,
    RacelandshopIntegration,
    RacelandshopNetdaemon,
    RacelandshopPlugin,
    RacelandshopPythonScript,
    RacelandshopTheme,
)
from custom_components.racelandshop.share import SHARE
from tests.async_mock import MagicMock

from tests.common import (  # noqa: E402, isort:skip
    async_test_home_assistant,
    fixture,
    mock_storage as mock_storage,
    TOKEN,
    dummy_repository_base,
)


# Set default logger
logging.basicConfig(level=logging.DEBUG)

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

asyncio.set_event_loop_policy(HassEventLoopPolicy(False))
# Disable fixtures overriding our beautiful policy
asyncio.set_event_loop_policy = lambda policy: None


@pytest.fixture()
def connection():
    """Mock fixture for connection."""
    yield MagicMock()


@pytest.fixture
def hass_storage():
    """Fixture to mock storage."""
    with mock_storage() as stored_data:
        yield stored_data


@pytest.fixture
def hass(event_loop, tmpdir):
    """Fixture to provide a test instance of Home Assistant."""

    def exc_handle(loop, context):
        """Handle exceptions by rethrowing them, which will fail the test."""
        exceptions.append(context["exception"])
        orig_exception_handler(loop, context)

    exceptions = []
    hass_obj = event_loop.run_until_complete(
        async_test_home_assistant(event_loop, tmpdir)
    )
    orig_exception_handler = event_loop.get_exception_handler()
    event_loop.set_exception_handler(exc_handle)

    hass_obj.http = MagicMock()

    yield hass_obj

    event_loop.run_until_complete(hass_obj.async_stop(force=True))
    for ex in exceptions:
        if isinstance(ex, (ServiceNotFound, FileExistsError)):
            continue
        raise ex


@pytest.fixture
def racelandshop(hass):
    """Fixture to provide a RACELANDSHOP object."""
    racelandshop_obj = Racelandshop()
    racelandshop_obj.hass = hass
    racelandshop_obj.session = async_create_clientsession(hass)
    racelandshop_obj.configuration = Configuration()
    racelandshop_obj.configuration.token = TOKEN
    racelandshop_obj.core.config_path = hass.config.path()
    racelandshop_obj.system.action = False
    SHARE["racelandshop"] = racelandshop_obj
    yield racelandshop_obj


@pytest.fixture
def repository(racelandshop):
    """Fixtrue for RACELANDSHOP repository object"""
    repository_obj = RacelandshopRepository()
    repository_obj.racelandshop = racelandshop
    repository_obj.hass = racelandshop.hass
    repository_obj.racelandshop.core.config_path = racelandshop.hass.config.path()
    repository_obj.logger = logging.getLogger("test")
    repository_obj.data.full_name = "test/test"
    repository_obj.data.full_name_lower = "test/test"
    repository_obj.data.domain = "test"
    repository_obj.data.last_version = "3"
    repository_obj.data.selected_tag = "3"
    repository_obj.ref = version_to_install(repository_obj)
    repository_obj.integration_manifest = {"config_flow": False, "domain": "test"}
    repository_obj.data.published_tags = ["1", "2", "3"]
    repository_obj.data.update_data(fixture("repository_data.json"))

    async def update_repository():
        pass

    repository_obj.update_repository = update_repository
    yield repository_obj


@pytest.fixture
def repository_integration(racelandshop):
    """Fixtrue for RACELANDSHOP integration repository object"""
    repository_obj = RacelandshopIntegration("test/test")
    yield dummy_repository_base(racelandshop, repository_obj)


@pytest.fixture
def repository_theme(racelandshop):
    """Fixtrue for RACELANDSHOP theme repository object"""
    repository_obj = RacelandshopTheme("test/test")
    yield dummy_repository_base(racelandshop, repository_obj)


@pytest.fixture
def repository_plugin(racelandshop):
    """Fixtrue for RACELANDSHOP plugin repository object"""
    repository_obj = RacelandshopPlugin("test/test")
    yield dummy_repository_base(racelandshop, repository_obj)


@pytest.fixture
def repository_python_script(racelandshop):
    """Fixtrue for RACELANDSHOP python_script repository object"""
    repository_obj = RacelandshopPythonScript("test/test")
    yield dummy_repository_base(racelandshop, repository_obj)


@pytest.fixture
def repository_appdaemon(racelandshop):
    """Fixtrue for RACELANDSHOP appdaemon repository object"""
    repository_obj = RacelandshopAppdaemon("test/test")
    yield dummy_repository_base(racelandshop, repository_obj)


@pytest.fixture
def repository_netdaemon(racelandshop):
    """Fixtrue for RACELANDSHOP netdaemon repository object"""
    repository_obj = RacelandshopNetdaemon("test/test")
    yield dummy_repository_base(racelandshop, repository_obj)
