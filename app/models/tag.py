from mongoengine import Document, StringField


class Tag(Document):
    name = StringField(required=True, unique=True)

    meta = {"collection": "tag", "indexes": ["name"]}
