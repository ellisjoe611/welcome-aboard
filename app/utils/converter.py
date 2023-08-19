from bson import ObjectId
from bson.errors import InvalidId
from flask import Flask
from werkzeug.routing import BaseConverter, ValidationError


class ObjectIdConverter(BaseConverter):
    def to_python(self, value) -> ObjectId:
        try:
            return ObjectId(value)
        except InvalidId:
            raise ValidationError()

    def to_url(self, value) -> str:
        return str(value)


def register_path_converter(app: Flask):
    app.url_map.converters["object_id"] = ObjectIdConverter
