from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_

from ..base import get_user_roles
from ... import security_manager, db
from ...models.folder import Folder


class FolderFilter(BaseFilter):
    def apply(self, query, value):
        user_roles = [role.name.lower() for role in list(get_user_roles())]
        if "admin" in user_roles:
            return query

        owner_ids_query = (
            db.session.query(Folder.id)
            .join(Folder.owners)
            .filter(
                security_manager.user_model.id
                == security_manager.user_model.get_user_id()
            )
        )

        query = query.filter(
            or_(
                Folder.id.in_(owner_ids_query),
            )
        )

        return query