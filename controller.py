__author__ = 'beast'

import random
import string
import importlib
import json
import logging

import dateutil.parser as dtparser
import dateutil.tz
from pymongo.database import InvalidName

from model import Search, FancySearch, MapReduceQuery, Aggregation, SearchConstants, Result, SearchableCollections




def class_from_string(whole_name, **kwargs):
    module_name = ".".join(whole_name.split(".")[0:-1])
    class_name = whole_name.split(".")[-1]


    #found_module = imp.find_module(module_name)

    module = importlib.import_module(module_name)
    #module = imp.load_module(found_module)
    class_ = getattr(module, class_name)
    instance = class_(kwargs)
    return instance


def get_default_exclusions():
    return {"_id"}

class SearchManager(object):

    def __init__(self, db):
        self.raw_db = db

    def search(self, search):
        pass


    def read_in(self, results):
        results_list = []

        for result in results:
            results_list.append(result)
        return results_list

    def get_fields(self, results):
        header_keys = results[0].keys()

        for key in get_default_exclusions():

            for i in range(len(header_keys) - 1, 0, -1):
                if header_keys[i] == header_keys:
                    del header_keys[i]

        return header_keys




class BasicSearchManager(SearchManager):

    def search(self, search):

        results = []
        if search.spec:
            results = self.raw_db.db[search.collection].find(spec=search.spec, limit=search.limit)
        else:
            results = self.raw_db.db[search.collection].find()
            #(spec=spec, fields=fields, limit=limit)

        if results and results.count() > 0:
            results = self.read_in(results)

            headers = self.get_fields(results)

            return Result(results, headers)
        return Result([],[])


class AggregationSearchManager(SearchManager):

    def search(self, search):

        results = []
        if search.spec:
            results = self.raw_db.db[search.collection].aggregate(search.spec)


        if results:
            results = self.read_in(results)

            headers = self.get_fields(results)

            return Result(results, headers)
        return Result([],[])


def fancy_search(search):
    return {}
def map_reduce(search):
    return {}



def search_factory(db, search_object):
    if search_object.type == SearchConstants.BASIC:
        return BasicSearchManager(db).search(search_object)
    if search_object.type == SearchConstants.FANCY:
        return BasicSearchManager(db).search(search_object)
    if search_object.type == SearchConstants.AGGREGATE:
        return AggregationSearchManager(db).search(search_object)

def get_name(spec):
    return spec[0:20]

def search_object_factory(collection, name, spec, type, fields, limit):
    if type == SearchConstants.FANCY:
        return FancySearch(name=name, collection=collection, type=type, spec=spec, limit=limit )
    elif type == SearchConstants.BASIC:
        return Search(name=name, collection=collection, type=type, spec=spec, limit=limit )
    elif type == SearchConstants.AGGREGATE:
        return Aggregation(name=name, collection=collection, type=type, spec=spec, limit=limit )
    else:
        return None


class Manager(object):
    def __init__(self, config, db, raw_db):
        self.DEBUG = config.DEBUG
        self.mongo = db
        self.raw_db = raw_db
        self.config_collections = config.Collections
        self.config_commands= config.Commands


    def prepare_search_params(self, search_params):
        print search_params

        if "id" in search_params and search_params["id"]:
            id = search_params["id"]
            #Get an Existing Search


            return ""

        else:

            collection, name, spec, type, fields, limit = None,None, None, SearchConstants.BASIC, None, 0

            if search_params["search"] and len(search_params["search"]) > 0:
                spec = json.loads(search_params["search"])
                name = get_name(search_params["search"])
            collection = search_params["collection"]

            if "type" in search_params and search_params["type"]:
                type = search_params["type"]


            if "commands" in search_params and search_params["commands"]:
                spec = search_params["commands"]


            search_object = search_object_factory(collection, name, spec, type, fields, limit)

            return search_object



    def get_available_collections(self):
        return self.config_collections

    def add_collection(self, label, collection_name):
        sc = SearchableCollections(label=label, collection_name=collection_name)
        sc.save()
        return sc

    def get_raw_collections(self):
        return self.raw_db.db.collection_names()


    def get_available_commands(self):
        return self.config_commands


    def create_search(self):
        pass

    def build_search(self, down_map, raw_search):
        if raw_search:
            return down_map.default_search.spec % raw_search
        else:
            return ""

    def search(self, search_params):

        logging.info("Received Search Request")
        search_object = self.prepare_search_params(search_params)

        if search_object:

            logging.info("Starting Search %s" % search_object.type)
            try:
                return search_factory(self.raw_db, search_object)


            except InvalidName:
                return Result([],[])

        return Result([],[])
