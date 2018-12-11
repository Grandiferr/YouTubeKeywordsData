from db import Document, StringField, FloatField, IntField, queryset
import datetime
class Keyword(Document):
    key = StringField(unique=True, required=True)
    cpc = FloatField(required=True)
    volume = IntField()
    competition = FloatField()