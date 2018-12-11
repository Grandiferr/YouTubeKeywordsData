from db import Document, StringField, EmbeddedDocumentField, EmbeddedDocument
class Comment(EmbeddedDocument):
    content = StringField()