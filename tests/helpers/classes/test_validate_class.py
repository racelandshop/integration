from custom_components.racelandshop.helpers.classes.validate import Validate


def test_validate():
    validate = Validate()
    assert validate.success
    validate.errors.append("test")
    assert not validate.success
