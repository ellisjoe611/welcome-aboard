from marshmallow import fields, Schema, validate


class UserInfoSchema(Schema):
    email = fields.Email()
    name = fields.String()
    subscribing = fields.Boolean()
    is_master = fields.Boolean()

    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()


class UserSearchFormSchema(Schema):
    email = fields.Email(load_default=None, allow_none=True, validate=validate.Email(error="정확한 이메일 형식으로 입력해 주세요"))
    page_no = fields.Integer(load_default=1, validate=validate.Range(min=1, error="페이지 번호는 1부터 입니다."))
    page_size = fields.Integer(load_default=20, validate=validate.OneOf(choices=(10, 20, 50, 100), error="조회 가능한 페이지 크기는 [10, 20, 50, 100] 입니다."))


class UserLoginFormSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email(error="정확한 이메일 형식으로 입력해 주세요."))
    password = fields.String(required=True, validate=validate.Length(min=8, error="비밀번호는 8자 이상 입니다."))


class UserCreateFormSchema(UserLoginFormSchema):
    name = fields.String(required=True)
    subscribing = fields.Boolean(load_default=False)


class UserUpdateFormSchema(Schema):
    change_pw = fields.Boolean(load_default=False)
    password = fields.String(load_default=None, allow_none=True, validate=validate.Length(min=8, error="비밀번호는 8자 이상 입니다."))
    new_password = fields.String(load_default=None, allow_none=True, validate=validate.Length(min=8, error="비밀번호는 8자 이상 입니다."))
    subscribing = fields.Boolean(load_default=None, allow_none=True)
