__author__ = 'beast'
import unittest
from urllib import urlencode

from bs4 import BeautifulSoup

from lxml import etree
from ..main import app as App
from ..controller import Manager
from ..settings import config
from ..model import db, raw_db, SearchableCollections
from fake_creator import create_fake_set


class TestController(unittest.TestCase):
    def setUp(self):
        self.app = App

        self.app.config.update(config(test_only=True).config_dict)
        self.test_app = self.app.test_client()


        #raw_db.init_app(self.app, "RAWMONGODB")
        #db.init_app(self.app)



        self.manager = Manager(config(test_only=True), db, raw_db)
        self.setup_data()

        self.addCleanup(self.remove_data)


    def setup_data(self):
        self.test_collection = "TestCustomerCollection"

        with self.app.app_context():
            self.data = create_fake_set(raw_db.db, self.test_collection)

            SearchableCollections.drop_collection()


    def remove_data(self):
        with self.app.app_context():
            raw_db.db.drop_collection(self.test_collection)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsNotNone(self.app)

    def test_search(self):
        with self.app.app_context():
            search_params = {"search": '{"name": "Bob"}',
                            "collection": "Customer",
                            "id":None,
                            "type":"basic"}

            result_object = self.manager.search(search_params)

            self.assertIsNotNone(result_object)

    def test_refined_search(self):
        with self.app.app_context():

            search_params = {"search": '{"name":"Bob"}',
                            "collection": "Customer",
                            "id":None,
                            "type":"fancy"}

            result_object = self.manager.search(search_params)

            self.assertIsNotNone(result_object)

    def test_aggregation_search(self):

        with self.app.app_context():
            search_params = {
                                 "command-1-type": '$group',
                                 "command-1": '{"_id": "$tags", "count": {"$sum": 1}}',
                                 "collection": "Customer"}

            result_object = self.manager.search(search_params)

            self.assertIsNotNone(result_object)



if __name__ == '__main__':
    unittest.main()
