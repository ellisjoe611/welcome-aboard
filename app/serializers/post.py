from marshmallow import fields, Schema

from app.serializers.user import UserInfoSchema
from app.serializers.tag import TagInfoSchema


class PostSearchFormSchema(Schema):
    query = fields.String(required=True)


class PostMasterSchema(Schema):
    title = fields.String()
    tags = fields.Nested(TagInfoSchema, many=True)
    count_likes = fields.Integer()

    created_by = fields.Nested(UserInfoSchema, only=["email", "name"])
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()
