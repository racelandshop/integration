import os

from custom_components.racelandshop.helpers.functions.logger import getLogger


def test_logger():
    os.environ["GITHUB_ACTION"] = "value"
    getLogger()
    del os.environ["GITHUB_ACTION"]
