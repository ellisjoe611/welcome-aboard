from marshmallow import fields, Schema


class AuthTokenSchema(Schema):
    token = fields.String()
