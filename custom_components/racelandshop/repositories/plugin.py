"""Class for plugins in RACELANDSHOP."""
import json

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository
from custom_components.racelandshop.helpers.functions.information import find_file_name


class RacelandshopPlugin(RacelandshopRepository):
    """Plugins in RACELANDSHOP."""

    def __init__(self, full_name):
        """Initialize."""
        super().__init__()
        self.data.full_name = full_name
        self.data.full_name_lower = full_name.lower()
        self.data.file_name = None
        self.data.category = "plugin"
        self.information.javascript_type = None
        self.content.path.local = self.localpath

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.racelandshop.core.config_path}/www/community/{self.data.full_name.split('/')[-1]}"

    async def validate_repository(self):
        """Validate."""
        # Run common validation steps.
        await self.common_validate()

        # Custom step 1: Validate content.
        find_file_name(self)

        if self.content.path.remote is None:
            raise RacelandshopException(
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
            )

        if self.content.path.remote == "release":
            self.content.single = True

        # Handle potential errors
        if self.validate.errors:
            for error in self.validate.errors:
                if not self.racelandshop.status.startup:
                    self.logger.error("%s %s", self, error)
        return self.validate.success

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
            return

        # Get plugin objects.
        find_file_name(self)

        if self.content.path.remote is None:
            self.validate.errors.append(
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
            )

        if self.content.path.remote == "release":
            self.content.single = True

    async def get_package_content(self):
        """Get package content."""
        try:
            package = await self.repository_object.get_contents(
                "package.json", self.ref
            )
            package = json.loads(package.content)

            if package:
                self.data.authors = package["author"]
        except (Exception, BaseException):  # pylint: disable=broad-except
            pass
