from marshmallow import Schema, fields

class AddressInfo:
    def __init__(self, street, city, zip_code):
        self.street = street
        self.city = city
        self.zip_code = zip_code


class Address:
    def __init__(self, type, info):
        self.type = type
        self.info = info


class Api1Model:
    def __init__(self, name, age, addresses):
        self.name = name
        self.age = age
        self.addresses = addresses


# Marshmallow
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