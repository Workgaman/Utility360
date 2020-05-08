import logging
from typing import Dict, Optional, List

from flask_appbuilder.security.sqla.models import User
from flask_appbuilder.models.sqla import Model
from marshmallow import ValidationError

from superset.commands.base import BaseCommand
from superset.commands.utils import populate_owners
from superset.dao.exceptions import DAOCreateFailedError
from superset.folders.commands.exceptions import FolderCreateFailedError, FolderInvalidError, \
    FolderNameOwnersValidationError
from superset.folders.dao import FolderDAO


logger = logging.getLogger(__name__)

class CreateFolderCommand(BaseCommand):
    def __init__(self, user: User, data: Dict):
        self._actor = user
        self._properties = data.copy()

    def run(self) -> Model:
        self.validate()
        try:
            folder = FolderDAO.create(self._properties, commit=False)
            folder = FolderDAO.update_folder_owners(folder, commit=True)
        except DAOCreateFailedError as ex:
            logger.exception(ex.exception)
            raise FolderCreateFailedError()
        return folder

    def validate(self) -> None:
        exceptions = list()
        owner_ids: Optional[List[int]] = self._properties.get("owners")
        folder_name: str = self._properties.get("folder_name")
        parent_id: int = self._properties.get("parent_id")
        if not FolderDAO.validate_name_owner(folder_name, owner_ids, parent_id):
            exceptions.append(FolderNameOwnersValidationError())
        try:
            owners = populate_owners(self._actor, owner_ids)
            self._properties["owners"] = owners
        except ValidationError as ex:
            exceptions.append(ex)
        if exceptions:
            exception = FolderInvalidError()
            exception.add_list(exceptions)
            raise exception
