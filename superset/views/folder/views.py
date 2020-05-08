from flask_appbuilder.models.sqla.interface import SQLAInterface

import superset.models.core as models
from superset.constants import RouteMethod
from superset.views.base import SupersetModelView, DeleteMixin
from superset.views.folder.mixin import FolderMixin


class FolderModelView(
    FolderMixin, SupersetModelView, DeleteMixin
):  # pylint: disable=too-many-ancestors
    route_base = "/folder"
    datamodel = SQLAInterface(models.Folder)
    # TODO disable api_read and api_delete (used by cypress)
    # once we move to ChartRestModelApi
    include_route_methods = RouteMethod.CRUD_SET | {
        RouteMethod.API_READ,
        RouteMethod.API_DELETE,
        "download_dashboards",
    }