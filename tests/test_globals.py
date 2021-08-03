"""Test globals."""
# pylint: disable=missing-docstring
from custom_components.racelandshop.share import get_removed, is_removed


def test_global_racelandshop(racelandshop):
    assert racelandshop.core.lovelace_mode == "yaml"
    racelandshop.core.lovelace_mode = "storage"
    assert racelandshop.core.lovelace_mode == "storage"


def test_is_removed():
    repo = "test/test"
    assert not is_removed(repo)


def test_get_removed():
    repo = "removed/removed"
    removed = get_removed(repo)
    assert removed.repository == repo
