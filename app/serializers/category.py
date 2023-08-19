from marshmallow import fields, Schema, validate

from app.serializers import ObjectIdSchemaField
from app.serializers.user import UserInfoSchema


class CategorySearchFormSchema(Schema):
    name = fields.String(load_default=None, allow_none=True, validate=validate.Length(min=2, max=10, error="카테고리 이름의 길이는 2~10자 이내입니다."))


class CategoryCreateFormSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=10, error="카테고리 이름의 길이는 2~10자 이내입니다."))


class CategoryDeleteFormSchema(CategoryCreateFormSchema):
    pass


class CategoryInfoSchema(Schema):
    id = ObjectIdSchemaField(data_key="category_id")
    name = fields.String()

    created_by = fields.Nested(UserInfoSchema, only=["email", "name"])
