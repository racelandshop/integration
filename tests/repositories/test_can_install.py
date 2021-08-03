"""Configuration Test Suite: can install."""
# pylint: disable=missing-docstring
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository


def test_racelandshop_can_install(racelandshop):
    repository = RacelandshopRepository()
    repository.repository_manifest = {"test": "test"}
    repository.data.releases = True

    racelandshop.system.ha_version = "1.0.0"
    repository.data.homeassistant = "1.0.0b1"
    assert repository.can_install

    racelandshop.system.ha_version = "1.0.0b1"
    repository.data.homeassistant = "1.0.0"
    assert not repository.can_install

    racelandshop.system.ha_version = "1.0.0b1"
    repository.data.homeassistant = "1.0.0b2"
    assert not repository.can_install

    racelandshop.system.ha_version = "1.0.0"
    repository.data.homeassistant = "1.0.0"
    assert repository.can_install
