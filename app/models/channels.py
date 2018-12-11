from db import Document, StringField, URLField, ListField, IntField, DateTimeField, DictField, EmbeddedDocumentField
import datetime


class Channel(Document):
    title = StringField(required=True, max_length=200)
    ytUserID = StringField(unique = True, required=True, max_length=100)
    URL = URLField(required=True)
    socialblade = URLField()
    tags = ListField(StringField())
    startdate = DateTimeField()
    comments = ListField(StringField())
    minMonthEarnings = IntField()
    maxMonthEarnings = IntField()
    subscriberRank = IntField()
    subscriberCount = IntField()
    viewRank = IntField()
    country = StringField()
