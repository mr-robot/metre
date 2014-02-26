__author__ = 'beast'

import datetime
from flask.ext.mongoengine import MongoEngine

from flask.ext.pymongo import PyMongo


db = MongoEngine()

raw_db = PyMongo()


class Search(db.Document):
    name = db.StringField(max_length=60)
    spec = db.StringField()
    done = db.BooleanField(default=False)
    created_date = db.DateTimeField(default=datetime.datetime.now)


class User(db.Document):
    email = db.StringField(required=True)

    recent_searches = db.ListField(db.ReferenceField(Search))


class Object(db.Document):
    name = db.StringField(max_length=60)
    created_date = db.DateTimeField(default=datetime.datetime.now)

    map = db.ReferenceField(DownMap)


class Entity(Object):
    pass


class Event(Object):
    pass


class DocMap(db.EmbeddedDocument):
    pass


class DownMap(db.Document):
    name = db.StringField(max_length=60)
    collections = db.ListField(EmbeddedDocumentField(DocMap))
    created_date = db.DateTimeField(default=datetime.datetime.now)

