from flask_appbuilder.models.sqla.interface import SQLAInterface

from superset.constants import RouteMethod
from superset.folders.filters import FolderTitleFilter, FolderFilter
from superset.folders.schemas import FolderPostSchema, FolderPutSchema
from superset.models.folder import Folder
from superset.views.base_api import BaseSupersetModelRestApi, RelatedFieldFilter
from superset.views.filters import FilterRelatedOwners

# import pdb
# pdb.set_trace()


class FolderRestApi(BaseSupersetModelRestApi):
    resource_name = "folder"
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