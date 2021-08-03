from custom_components.racelandshop.validate.base import (
    ActionValidationBase,
    ValidationException,
)


class RacelandshopManifest(ActionValidationBase):
    def check(self):
        if "racelandshop.json" not in [x.filename for x in self.repository.tree]:
            raise ValidationException("The repository has no 'racelandshop.json' file")
