import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from guestbook_app.models import Greeting, Guestbook, AppConstants


class TestBassClass(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

    def tearDown(self):
        self.testbed.deactivate()


class TestClassGreeting(TestBassClass):

    def test_get_greetings(self):
        greetings = Greeting.get_greetings(AppConstants.get_default_guestbook_name())
        assert(greetings is not None and len(greetings) > 0)

    def test_put_from_dict(self):
        dictionary = {
            "dictionary": AppConstants.get_default_guestbook_name(),
            "content": "test"
        }
        greeting = Greeting.put_from_dict(dictionary)
        assert(greeting is not None)

    def test_delete_greeting(self):
        dictionary = {
            "dictionary": AppConstants.get_default_guestbook_name(),
            "content": "test"
        }
        greeting = Greeting.put_from_dict(dictionary)
        dictionary_test = {
            "greeting_id": str(greeting.key.id),
            "guestbook_name": str(greeting.key.parent.id)
        }
        is_delete = Greeting.delete_greeting(dictionary_test)
        assert(is_delete is True)

    def test_update_greeting(self):
        dictionary = {
            "guestbook_name": AppConstants.get_default_guestbook_name(),
            "content": "test"
        }
        greeting = Greeting.put_from_dict(dictionary)

        dict_update = {
            "greeting_id": greeting.key.id,
            "guestbook_name": greeting.key.parent.id,
            "author": None,
            "content": "test_version2"
        }
        greeting_after_update = Greeting.update_greeting(dict_update)
        assert(
            dict_update["greeting_id"] == greeting_after_update.key.id and
            dict_update["guestbook_name"] == greeting_after_update.key.parent.id and
            dict_update["author"] == greeting_after_update.author and
            dict_update["content"] == greeting_after_update.content
        )








