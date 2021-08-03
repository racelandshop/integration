from custom_components.racelandshop.helpers.classes.removed import RemovedRepository


def test_removed():
    removed = RemovedRepository()
    assert isinstance(removed.to_json(), dict)
