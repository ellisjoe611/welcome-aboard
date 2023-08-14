from marshmallow import fields, Schema, validate

from app.serializers.user import UserInfoSchema


class TagSearchFormSchema(Schema):
    name = fields.String(load_default=None, allow_none=True, validate=validate.Length(min=2, max=10, error="태그명의 길이는 2~10자 이내입니다."))
    page_no = fields.Integer(load_default=1, validate=validate.Range(min=1, error="페이지 번호는 1부터 입니다."))
    page_size = fields.Integer(load_default=20, validate=validate.OneOf(choices=(10, 20, 50, 100), error="조회 가능한 페이지 크기는 [10, 20, 50, 100] 입니다."))


class TagCreateFormSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=10, error="태그명의 길이는 2~10자 이내입니다."))


class TagDeleteFormSchema(TagCreateFormSchema):
    pass


class TagInfoSchema(Schema):
    name = fields.String()

    created_by = fields.Nested(UserInfoSchema, only=["email", "name"])
    created_at = fields.DateTime()
    is_deleted = fields.Boolean()
