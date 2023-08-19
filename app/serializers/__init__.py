from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from marshmallow import ValidationError
from marshmallow.fields import Field


class ObjectIdSchemaField(Field):
    """
    Marshmallow field for :class:`bson.ObjectId`
    """

    def _serialize(self, value, attr, obj) -> Optional[str]:
        if value is None:
            return None
        return value if isinstance(value, str) else str(value)

    def _deserialize(self, value, attr, data) -> Optional[ObjectId]:
        if value is None:
            return None
        try:
            return ObjectId(value)
        except (TypeError, InvalidId):
            raise ValidationError("invalid ObjectId `%s`" % value)
