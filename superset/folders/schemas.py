from marshmallow import Schema, fields
from marshmallow.validate import Length


class FolderPostSchema(Schema):
    folder_name = fields.String(allow_none=True, validate=Length(0, 500))
    description = fields.String(allow_none=True)
    parent_id = fields.Integer(allow_none=True)
    owners = fields.List(fields.Integer(allow_none=True))

class FolderPutSchema(Schema):
    folder_name = fields.String(allow_none=True, validate=Length(0, 500))
    description = fields.String(allow_none=True)
    parent_id = fields.Integer(allow_none=True)
    owners = fields.List(fields.Integer(allow_none=True))
