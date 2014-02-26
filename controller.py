__author__ = 'beast'

import random
import string
import importlib
import json

import dateutil.parser as dtparser
import dateutil.tz
from pymongo.database import InvalidName


def getCode(length=4, char=string.ascii_uppercase +
                           string.digits +
                           string.ascii_lowercase):
    return ''.join(random.choice(char) for x in range(length))


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


class Manager(object):
    def __init__(self, config, db, raw_db):
        self.DEBUG = config.DEBUG
        self.mongo = db
        self.raw_db = raw_db


    def prepare_search_params(self, search_params):
        collection, spec, fields, limit = None, None, None, 0

        if search_params["search"] and len(search_params["search"]) > 0:
            spec = json.loads(search_params["search"])
        collection = search_params["collection"]

        return collection, spec, fields, limit

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


    def get_available_collections(self):
        return {"Customers": "Customers"}

    def get_available_objects(self):
        return {"Customers": "Customers"}

    def create_search(self):
        pass


    def refined_search(self, search_params):
        collection, spec, fields, limit = self.prepare_search_params(search_params)

        if collection:
            try:
                results = []
                print spec
                if spec:
                    results = self.raw_db.db[collection].find(spec=spec, fields=fields, limit=limit)
                else:
                    results = self.raw_db.db[collection].find()
                    #(spec=spec, fields=fields, limit=limit)

                if results and results.count() > 0:
                    results = self.read_in(results)

                    headers = self.get_fields(results)

                    return results, headers, results

            except InvalidName:
                return None, None, None

        return None, None, None


    def search(self, search_params):
        collection, spec, fields, limit = self.prepare_search_params(search_params)

        if collection:
            try:
                results = []
                print spec
                if spec:
                    results = self.raw_db.db[collection].find(spec=spec, fields=fields, limit=limit)
                else:
                    results = self.raw_db.db[collection].find()
                    #(spec=spec, fields=fields, limit=limit)

                if results and results.count() > 0:
                    results = self.read_in(results)

                    headers = self.get_fields(results)

                    return results, headers, results

            except InvalidName:
                return None, None, None

        return None, None, None
