"""Helpers: Information: get_frontend_version."""
import json

# pylint: disable=missing-docstring
import os

from custom_components.racelandshop.helpers.functions.information import get_frontend_version


def temp_cleanup(tmpdir):
    racelandshopdir = f"{tmpdir.dirname}/custom_components/racelandshop"
    manifestfile = f"{racelandshopdir}/manifest.json"
    if os.path.exists(manifestfile):
        os.remove(manifestfile)
    if os.path.exists(racelandshopdir):
        os.removedirs(racelandshopdir)


def test_get_frontend_version(racelandshop, tmpdir):
    racelandshopdir = f"{tmpdir.dirname}/custom_components/racelandshop"
    manifestfile = f"{racelandshopdir}/manifest.json"
    racelandshop.core.config_path = tmpdir.dirname

    data = {"requirements": ["racelandshop_frontend==999999999999"]}

    os.makedirs(racelandshopdir, exist_ok=True)
    with open(manifestfile, "w") as manifest_file:
        manifest_file.write(json.dumps(data))

    frontend_version = get_frontend_version()
    assert frontend_version == "999999999999"
    temp_cleanup(tmpdir)
