"""Helpers: Information: read_racelandshop_manifest."""
import json

# pylint: disable=missing-docstring
import os

from custom_components.racelandshop.helpers.functions.information import read_racelandshop_manifest


def temp_cleanup(tmpdir):
    racelandshopdir = f"{tmpdir.dirname}/custom_components/racelandshop"
    manifestfile = f"{racelandshopdir}/manifest.json"
    if os.path.exists(manifestfile):
        os.remove(manifestfile)
    if os.path.exists(racelandshopdir):
        os.removedirs(racelandshopdir)


def test_read_racelandshop_manifest(racelandshop, tmpdir):
    racelandshopdir = f"{tmpdir.dirname}/custom_components/racelandshop"
    manifestfile = f"{racelandshopdir}/manifest.json"
    racelandshop.core.config_path = tmpdir.dirname

    data = {"test": "test"}

    os.makedirs(racelandshopdir, exist_ok=True)
    with open(manifestfile, "w") as manifest_file:
        manifest_file.write(json.dumps(data))

    manifest = read_racelandshop_manifest()
    assert data == manifest
    temp_cleanup(tmpdir)
