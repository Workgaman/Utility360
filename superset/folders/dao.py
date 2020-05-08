from superset.extensions import db
from superset.dao.base import BaseDAO
from superset.folders.filters import FolderFilter
from superset.models.folder import Folder


class FolderDAO(BaseDAO):
    model_cls = Folder
    base_filter = FolderFilter

    @staticmethod
    def update_folder_owners(model: Folder, commit:bool = True) -> Folder:
        owners = [owner for owner in model.owners]
        for subfolder in model.children:
            subfolder.owners = list(set(owners) | set(subfolder.owners))
        if commit:
            db.session.commit()
        return model
    
    @staticmethod
    def validate_name_owner(folder_name: str, owners: list, parent_id: int) -> bool:
        folder_query = db.session.query(Folder).filter(Folder.folder_name == folder_name, Folder.parent_id == parent_id)
        ##TODO check for owners as well
        return not db.session.query(folder_query.exists()).scalar()
