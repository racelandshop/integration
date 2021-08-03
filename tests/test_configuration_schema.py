"""RACELANDSHOP configuration schema Test Suite."""
# pylint: disable=missing-docstring
from custom_components.racelandshop.helpers.functions.configuration_schema import (
    racelandshop_config_combined,
)


def test_combined():
    assert isinstance(racelandshop_config_combined(), dict)
