import os

from custom_components.racelandshop.share import SHARE, get_racelandshop, list_removed_repositories


def test_list_removed_repositories():
    list_removed_repositories()


def test_get_racelandshop():
    SHARE["racelandshop"] = None
    os.environ["GITHUB_ACTION"] = "value"
    if "PYTEST" in os.environ:
        del os.environ["PYTEST"]
    get_racelandshop()
    SHARE["racelandshop"] = None
    del os.environ["GITHUB_ACTION"]
    os.environ["PYTEST"] = "value"
