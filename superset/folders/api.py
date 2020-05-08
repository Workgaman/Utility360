import logging

from flask import Response, request, g
from flask_appbuilder.api import expose, protect, safe
from flask_appbuilder.models.sqla.interface import SQLAInterface

from superset import security_manager
from superset.constants import RouteMethod
from superset.folders.commands.create import CreateFolderCommand
from superset.folders.filters import FolderTitleFilter, FolderFilter
from superset.folders.schemas import FolderPostSchema, FolderPutSchema
from superset.models.folder import Folder
from superset.views.base_api import BaseSupersetModelRestApi, RelatedFieldFilter, statsd_metrics
from superset.views.filters import FilterRelatedOwners

logger = logging.getLogger(__name__)

class FolderRestApi(BaseSupersetModelRestApi):
    datamodel = SQLAInterface(Folder)
    include_route_methods = RouteMethod.REST_MODEL_VIEW_CRUD_SET | {
        RouteMethod.EXPORT,
        RouteMethod.RELATED,
        "bulk_delete",  # not using RouteMethod since locally defined
    }
    resource_name = "folder"
    allow_browser_login = True

    class_permission_name = "FolderModelView"
    show_columns = [
        "id",
        "folder_name",
        "description",
        "owners.id",
        "owners.username",
        "owners.first_name",
        "owners.last_name",
        "changed_by_name",
        "changed_by.username",
        "changed_on",
    ]
    order_columns = ["folder_name", "changed_on", "changed_by_fk"]
    list_columns = [
        "id",
        "folder_name",
        "description",
        "owners.id",
        "owners.username",
        "owners.first_name",
        "owners.last_name",
        "changed_by_name",
        "changed_by.username",
        "changed_on",
    ]
    edit_columns = [
        "folder_name",
        "owners",
        "description",
    ]
    search_columns = ("folder_name", "owners")
    search_filters = {"folder_name": [FolderTitleFilter]}
    add_columns = edit_columns
    base_order = ("changed_on", "desc")

    add_model_schema = FolderPostSchema()
    edit_model_schema = FolderPutSchema()

    # base_filters = [[ FolderFilter, lambda: []]]

    openapi_spec_tag = "Folders"
    order_rel_fields = {
        "owners": ("first_name", "asc"),
    }
    related_field_filters = {
        "owners": RelatedFieldFilter("first_name", FilterRelatedOwners)
    }
    allowed_rel_fields = {"owners"}

    def __init__(self) -> None:
        super().__init__()


    @expose("/", methods=["POST"])
    @safe
    @protect()
    @statsd_metrics
    def post(self) -> Response:
        """
        Create a folder object
        """
        if not request.is_json:
            return self.response_400(message="Request is not JSON")
        item = self.add_model_schema.load(request.json)
        if item.errors:
            return self.response_400(message=item.errors)
        try:
            new_model = CreateFolderCommand(g.user, item.data).run()
            return self.response(201, id=new_model.id, result=item.data)
        except Exception as ex:
            logger.error(f"Error Creating model {self.__class__.__name__}: {ex}")
            return self.response_422(message=str(ex))

    @expose("/", methods=["GET"])
    @safe
    @protect()
    @statsd_metrics
    def get(self) -> Response:
        """Get top level folders for a user"""

        # top_folders = GetTopLevelFoldersCommand(g.user).run()
        query = self.datamodel.session.query(Folder).join(Folder.owners).filter(
            security_manager.user_model.id == security_manager.user_model.get_user_id(),
            Folder.parent_id.is_(None)
        )
        ids = [item.id for item in query.all()]
        folder_arr = [item.list_child_folders() for item in query.all()]
        return self.response(201, id=ids, result=folder_arr)