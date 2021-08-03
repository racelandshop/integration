"""RACELANDSHOP Manifest Test Suite."""
# pylint: disable=missing-docstring
import pytest

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.classes.manifest import RacelandshopManifest


def test_manifest_structure():
    manifest = RacelandshopManifest.from_dict({"name": "TEST"})

    assert isinstance(manifest.manifest, dict)

    assert isinstance(manifest.name, str)
    assert manifest.name == "TEST"

    assert isinstance(manifest.content_in_root, bool)
    assert not manifest.content_in_root

    assert isinstance(manifest.zip_release, bool)
    assert not manifest.zip_release

    assert isinstance(manifest.filename, (str, type(None)))
    assert manifest.filename is None

    assert isinstance(manifest.domains, list)
    assert not manifest.domains

    assert isinstance(manifest.country, list)
    assert not manifest.country

    assert isinstance(manifest.homeassistant, (str, type(None)))
    assert manifest.homeassistant is None

    assert isinstance(manifest.persistent_directory, (str, type(None)))
    assert manifest.persistent_directory is None

    assert isinstance(manifest.iot_class, (str, type(None)))
    assert manifest.iot_class is None

    assert isinstance(manifest.render_readme, bool)
    assert not manifest.render_readme

    assert isinstance(manifest.racelandshop, (str, type(None)))
    assert not manifest.racelandshop

    assert isinstance(manifest.hide_default_branch, bool)
    assert not manifest.hide_default_branch


def test_edge_pass_none():
    with pytest.raises(RacelandshopException):
        assert RacelandshopManifest.from_dict(None)
