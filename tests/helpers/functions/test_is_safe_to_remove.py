from custom_components.racelandshop.helpers.functions.is_safe_to_remove import is_safe_to_remove


def test_is_safe_to_remove(racelandshop):
    assert is_safe_to_remove("/test")

    assert not is_safe_to_remove(
        f"{racelandshop.core.config_path}/{racelandshop.configuration.theme_path}/"
    )

    assert not is_safe_to_remove(f"{racelandshop.core.config_path}/custom_components/")

    assert not is_safe_to_remove(f"{racelandshop.core.config_path}/custom_components")
