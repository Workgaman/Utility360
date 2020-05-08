from flask_babel import lazy_gettext as _

from superset.views.base import check_ownership
from .filters import FolderFilter


class FolderMixin:
    list_title = _("Folders")
    show_title = _("Show Folder")
    add_title = _("Add Folder")
    edit_title = _("Edit Folder")

    list_columns = ["folder_name", "description", "creator", "modified"]
    order_columns = ["folder_name", "modified", "owners"]
    edit_columns = [
        "folder_name",
        "slug",
        "owners",
    ]
    show_columns = edit_columns + ["slices", "dashboards"]
    search_columns = ("folder_name", "slug", "owners")
    add_columns = edit_columns
    base_order = ("changed_on", "desc")
    description_columns = {
        "slug": _("To get a readable URL for your dashboard"),
        "owners": _("Owners is a list of users who can alter the dashboard."),
    }
    base_filters = [[ FolderFilter, lambda: []]]
    label_columns = {
        "folder_link": _("Folder"),
        "folder_name": _("Folder Name"),
        "slug": _("Slug"),
        "charts": _("Charts"),
        "dashboards":_("Dashboards"),
        "owners": _("Owners"),
        "creator": _("Creator"),
        "modified": _("Modified"),
    }

    def pre_delete(self, item):  # pylint: disable=no-self-use
        check_ownership(item)