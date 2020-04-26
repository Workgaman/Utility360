import logging

from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Table,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from superset import security_manager, app
from superset.models.helpers import AuditMixinNullable, ImportMixin

metadata = Model.metadata  # pylint: disable=no-member
config = app.config
logger = logging.getLogger(__name__)


folder_slices = Table(
    "folder_slices",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("folder_id", Integer, ForeignKey("folders.id")),
    Column("slice_id", Integer, ForeignKey("slices.id")),
    UniqueConstraint("folder_id", "slice_id"),
)

folder_dashboards = Table(
    "folder_dashboards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("dashboard_id", Integer, ForeignKey("dashboards.id")),
    Column("folder_id", Integer, ForeignKey("folders.id")),
    UniqueConstraint("folder_id", "dashboard_id"),
)


folder_user = Table(
    "folder_user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("ab_user.id")),
    Column("folder_id", Integer, ForeignKey("folders.id")),
)


class Folder(  # pylint: disable=too-many-instance-attributes
    Model, AuditMixinNullable, ImportMixin
):
    """The dashboard object!"""

    __tablename__ = "folders"
    id = Column(Integer, primary_key=True)
    folder_name = Column(String(500))
    description = Column(Text)
    slug = Column(String(255), unique=True)
    parent_id = Column(Integer, ForeignKey(id))
    dashboards = relationship(
        "Dashboard", secondary=folder_dashboards, backref="folders"
    )
    slices = relationship("Slice", secondary=folder_slices, backref="folders")
    owners = relationship(security_manager.user_model, secondary=folder_user)
    children = relationship(
        "Folder",
        cascade="all, delete-orphan",
        backref=backref("parent", remote_side=[id]),
        lazy="dynamic",
    )

    def __init__(self, folder_name, parent=None):
        self.folder_name = folder_name
        self.parent = parent

    def __repr__(self):
        return self.folder_name or str(self.id)

    def add_subfolder(self, folder_name):
        return Folder(folder_name=folder_name, parent=self)

    def list_folder(self, folder):
        f = {"folder_name": folder.folder_name, "id": folder.id}
        if folder.children:
            child_arr = []
            for i in folder.children:
                x = self.list_folder(i)
                child_arr.append(x)
            if child_arr:
                f["children"] = child_arr
            return f
        else:
            return f
