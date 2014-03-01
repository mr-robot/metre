__author__ = 'beast'

import datetime
from flask.ext.mongoengine import MongoEngine

from flask.ext.pymongo import PyMongo


db = MongoEngine()

raw_db = PyMongo()

'''
    Search Objects

'''


class BaseSearch(db.Document):
    name = db.StringField(max_length=60)
    done = db.BooleanField(default=False)
    created_date = db.DateTimeField(default=datetime.datetime.now)


    meta = {'allow_inheritance': True}

class Search(BaseSearch):
    spec = db.StringField()

class MapReduceQuery(BaseSearch):
    map = db.StringField()
    reduce = db.StringField()
    out = db.StringField()


class Aggregation(Search):
    pass


'''
    User Management Objects

'''




class User(db.Document):
    email = db.StringField(required=True)

    recent_searches = db.ListField(db.ReferenceField(Search))



'''
    Refined Objects

'''
class DocMap(db.EmbeddedDocument):

    default_search = db.ReferenceField(Search)
    collection_name = db.StringField()

    included_fields = db.ListField(db.StringField())

class DownMap(db.Document):
    name = db.StringField(max_length=60)
    collections = db.ListField(db.EmbeddedDocumentField(DocMap))
    created_date = db.DateTimeField(default=datetime.datetime.now)


class Object(db.Document):
    name = db.StringField(max_length=60)
    created_date = db.DateTimeField(default=datetime.datetime.now)

    map = db.ReferenceField(DownMap)

    mr_search = db.ListField(MapReduceQuery)
    aggregatations= db.ListField(Aggregation)





