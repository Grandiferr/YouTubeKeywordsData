from db import Document, StringField


class Animal(Document):
    name = StringField()
    