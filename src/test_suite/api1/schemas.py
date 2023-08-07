from marshmallow import Schema, fields


class AddressInfoSchema(Schema):
    street = fields.String(required=True)
    city = fields.String(required=True)
    zip_code = fields.String(required=True)


class AddressSchema(Schema):
    type = fields.String(required=True)
    info = fields.Nested(AddressInfoSchema, required=True)


class Api1ModelSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True)
    addresses = fields.List(fields.Nested(AddressSchema), required=True)
