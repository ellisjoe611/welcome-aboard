from marshmallow import fields, Schema, validate


class UserInfoSchema(Schema):
    email = fields.Email()
    name = fields.String()
    subscribing = fields.Boolean()
    is_master = fields.Boolean()
    created_at = fields.DateTime()


class UserLoginFormSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(error="정확한 이메일 형식으로 입력해주세요"))
    password = fields.String(required=True, validate=validate.Length(min=8, error="비밀번호는 8자 이상 입니다."))


class UserCreateFormSchema(UserLoginFormSchema):
    name = fields.String(required=True)
    subscribing = fields.Boolean(default=False)


class UserUpdateFormSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=8))
    subscribing = fields.Boolean()
