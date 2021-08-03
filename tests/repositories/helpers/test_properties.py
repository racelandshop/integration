"""RACELANDSHOP Repository Helper properties."""
# pylint: disable=missing-docstring
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository


def test_repository_helpers_properties_can_be_installed():
    repository = RacelandshopRepository()
    assert repository.can_be_installed


def test_repository_helpers_properties_custom():
    repository = RacelandshopRepository()

    repository.data.full_name = "test/test"
    repository.data.full_name_lower = "test/test"
    assert repository.custom

    repository.data.id = 1337
    repository.racelandshop.common.default.append(str(repository.data.id))
    assert not repository.custom

    repository.racelandshop.common.default = []
    assert repository.custom

    repository.data.full_name = "racelandshop/integration"
    repository.data.full_name_lower = "racelandshop/integration"
    assert not repository.custom


def test_repository_helpers_properties_pending_update():
    repository = RacelandshopRepository()
    repository.racelandshop.system.ha_version = "0.109.0"
    repository.data.homeassistant = "0.110.0"
    repository.data.releases = True
    assert not repository.pending_update

    repository = RacelandshopRepository()
    repository.data.installed = True
    repository.data.default_branch = "main"
    repository.data.selected_tag = "main"
    assert not repository.pending_update

    repository.data.installed_commit = "1"
    repository.data.last_commit = "2"
    assert repository.pending_update
