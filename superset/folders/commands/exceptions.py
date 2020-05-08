from flask_babel import lazy_gettext as _
from marshmallow import ValidationError

from superset.commands.exceptions import CreateFailedError, CommandInvalidError



class FolderNameOwnersValidationError(ValidationError):
    """
        Marshmallow validation error for dashboard slug already exists
        """

    def __init__(self) -> None:
        super().__init__(_("Must be unique"), field_names=["folder_name", "parent"])


class FolderCreateFailedError(CreateFailedError):
    message = _("Folder could not be created.")

class FolderInvalidError(CommandInvalidError):
    message = _("Folder parameters are invalid.")
