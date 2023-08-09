from typing import Optional
from marshmallow import Schema, fields


class ApiError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        Exception.__init__(self)
        self.status_code = status_code or 400
        self.message = message


class ApiStatusSchema(Schema):
    status_code = fields.Integer(data_key="code", required=True)
    message = fields.String()
