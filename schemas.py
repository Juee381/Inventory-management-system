from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    expiry_time = fields.DateTime()
    quantity = fields.Int()
    manufacturing_time = fields.DateTime()
    image = fields.Str()


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemUpdateSchema(Schema):
    name = fields.Str()
    category = fields.Str()
    expiry_time = fields.DateTime()
    quantity = fields.Int()
    manufacturing_time = fields.DateTime()


class StoreUpdateSchema(Schema):
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class DeleteSchema(Schema):
    del_items = fields.List(fields.Int(), required=True)


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image."
    }

    def _deserialize(self, value, attr, data, **kwargs, ) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")

        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)  # use custom datatype

# if any value missing then: intregrity error
# if different type then automatically convert into given type
