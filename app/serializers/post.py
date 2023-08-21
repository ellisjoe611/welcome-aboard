from marshmallow import fields, Schema, validate

from app.serializers import ObjectIdSchemaField
from app.serializers.user import UserInfoSchema
from app.serializers.category import CategoryInfoSchema


class PostMasterSearchFormSchema(Schema):
    title = fields.String(load_default=None, allow_none=True, validate=validate.Length(max=100, error="제목은 100자 이내로 작성이 가능합니다."))
    category_id = ObjectIdSchemaField(load_default=None, allow_none=True)
    page_no = fields.Integer(load_default=1, validate=validate.Range(min=1, error="페이지 번호는 1부터 입니다."))
    page_size = fields.Integer(load_default=20, validate=validate.OneOf(choices=(10, 20, 50, 100), error="조회 가능한 페이지 크기는 [10, 20, 50, 100] 입니다."))


class PostCreateFormSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=100, error="제목은 100자 이내로 작성이 가능합니다."))
    content = fields.String(required=True, validate=validate.Length(max=1000, error="본문은 1,000자 이내로 작성이 가능합니다."))
    category_ids = fields.List(ObjectIdSchemaField, load_default=None, allow_none=True)


class PostUpdateFormSchema(PostCreateFormSchema):
    pass


class PostMasterInfoSchema(Schema):
    id = ObjectIdSchemaField(data_key="post_id")
    title = fields.String()
    categories = fields.Nested(CategoryInfoSchema, only=["id", "name"], many=True)
    likes_cnt = fields.Integer()

    created_by = fields.Nested(UserInfoSchema, only=["email", "name"])
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()


class PostDetailInfoSchema(PostMasterInfoSchema):
    content = fields.String()
    likes = fields.Nested(UserInfoSchema, only=["email", "name"], many=True)
