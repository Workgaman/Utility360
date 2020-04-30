from superset import db, security_manager
from superset.models.folder import Folder
from sqlalchemy.orm.query import Query
from typing import Any
from superset.views.base import BaseFilter, get_user_roles
from flask_babel import lazy_gettext as _


class FolderTitleFilter(BaseFilter):
    name = _("Folder Name")
    arg_name = "folder_name"

    def apply(self, query: Query, value: Any) -> Query:
        if not value:
            return query
        ilike_value = f"%{value}%"
        return query.filter(
                Folder.dashboard_title.ilike(ilike_value),
        )




class FolderFilter(BaseFilter):

    def apply(self, query: Query, value: Any) -> Query:
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
                Folder.id.in_(owner_ids_query),
        )

        return query
