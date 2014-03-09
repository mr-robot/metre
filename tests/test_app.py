#Embedded file name: /home/beast/Projects/confer/confer/tests/test_app.py
__author__ = 'beast'
import unittest
from urllib import urlencode

from bs4 import BeautifulSoup

from lxml import etree
from ..main import app as App
from ..controller import Manager
from ..settings import config
from ..model import db, raw_db
from fake_creator import create_fake_set


class TestApplication(unittest.TestCase):
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


    def remove_data(self):
        with self.app.app_context():
            raw_db.db.drop_collection(self.test_collection)

    def tearDown(self):
        pass

    def test_init(self):
        self.assertIsNotNone(self.app)

    def test_get_search(self):
        with self.app.app_context():
            response = self.test_app.get('/search')
            self.assertIsNotNone(response)
            self.assertEquals(response.status_code, 200)
            bs = BeautifulSoup(response.data)
            self.assertEquals(bs.title.string, u' Search ')
            form = bs.find_all('form')[0]
            self.assertIsNotNone(form)
            self.assertEquals(form.get('action'), '/search')
            self.assertEquals(form.get('class')[0], 'navbar-form')
            self.assertEquals(form.get('method'), 'get')
            self.assertIsNotNone(form.find(id='csrf_token'))
            self.assertEquals(form.find(id='csrf_token').get('type'), 'hidden')
            self.assertEquals(form.find(id='csrf_token').get('name'), 'csrf_token')
            self.assertNotEqual(form.find(id='csrf_token').get('value'), '')

    def test_send_search(self):
        with self.app.app_context():
            response = self.test_app.get('/search')
            bs = BeautifulSoup(response.data)
            self.assertEquals(bs.title.string, u' Search ')
            form = bs.find_all('form')[0]
            self.assertIsNotNone(form)

            search_params = {'csrf_token': form.find(id='csrf_token').get('value'),
                             "search": '{"name": "%s"}' % self.data["customers"][0]["name"],
                             "collection": "test"}

            search_url = urlencode(search_params)

            response = self.test_app.get("/search?%s" % (search_url), )
            self.assertIsNotNone(response)
            self.assertEquals(response.status_code, 200)

    def test_get_refined_search(self):
        with self.app.app_context():
            response = self.test_app.get('/search')
            self.assertIsNotNone(response)
            self.assertEquals(response.status_code, 200)
            bs = BeautifulSoup(response.data)
            self.assertEquals(bs.title.string, u' Search ')
            form = bs.find_all('form')[0]
            self.assertIsNotNone(form)
            self.assertEquals(form.get('action'), '/search')
            self.assertEquals(form.get('class')[0], 'navbar-form')
            self.assertEquals(form.get('method'), 'get')
            self.assertIsNotNone(form.find(id='csrf_token'))
            self.assertEquals(form.find(id='csrf_token').get('type'), 'hidden')
            self.assertEquals(form.find(id='csrf_token').get('name'), 'csrf_token')
            self.assertNotEqual(form.find(id='csrf_token').get('value'), '')


if __name__ == '__main__':
    unittest.main()
