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

    collection = db.StringField()

    type =  db.StringField()

    meta = {'allow_inheritance': True}

class Search(BaseSearch):
    spec = db.StringField()
    limit = db.IntField()


class FancySearch(Search):

    included_fields = db.ListField(db.StringField())

    excluded_fields = db.ListField(db.StringField())

class MapReduceQuery(BaseSearch):
    map = db.StringField()
    reduce = db.StringField()
    out = db.StringField()


class Aggregation(Search):
    pass


'''
    User Management Objects

'''

class SearchableCollections(db.Document):

    label = db.StringField()
    collection_name = db.StringField()
    created_date = db.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return self.label




class User(db.Document):
    email = db.StringField(required=True)

    recent_searches = db.ListField(db.ReferenceField(BaseSearch))





class Result(object):

    def __init__(self, results, headers):
        self.results = results
        self.raw_results = results

        self.headers = headers


class SearchConstants:
    BASIC="basic"
    FANCY="fancy"
    AGGREGATE="aggregate"

    MAPREDUCE="mapreduce"