from marshmallow import fields, Schema, validate

from app.serializers import ObjectIdSchemaField
from app.serializers.user import UserInfoSchema
from app.serializers.post import PostMasterInfoSchema


class CommentListSearchFormSchema(Schema):
    post_id = ObjectIdSchemaField(required=True)
    page_no = fields.Integer(load_default=1, validate=validate.Range(min=1, error="페이지 번호는 1부터 입니다."))
    page_size = fields.Integer(load_default=20, validate=validate.OneOf(choices=(10, 20, 50, 100), error="조회 가능한 페이지 크기는 [10, 20, 50, 100] 입니다."))


class CommentCreateFormSchema(Schema):
    post_id = ObjectIdSchemaField(required=True)
    content = fields.String(required=True, validate=validate.Length(max=300, error="댓글은 300자 이내로 작성이 가능합니다."))


class CommentInfoSchema(Schema):
    id = ObjectIdSchemaField(data_key="comment_id")
    post = fields.Nested(PostMasterInfoSchema, only=["id", "title"])
    content = fields.String()
    likes = fields.Nested(UserInfoSchema, only=["email", "name"], many=True)
    likes_cnt = fields.Integer()

    created_by = fields.Nested(UserInfoSchema, only=["email", "name"])
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()
