import unittest
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from guestbook_app.models import Greeting, Guestbook, AppConstants


class TestBassClass(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
        self.testbed.deactivate()


class TestClassGuestbook(TestBassClass):

    def test_get_guestbook_key(self):
        key_before = ndb.Key('Guestbook', "test_get_key")
        key_after = Guestbook.get_guestbook_key("test_get_key")
        assert key_after == key_before

    def test_get_guestbook_by_name(self):
        guestbook_name_before = "test_get_by_name"
        Guestbook.add_new_book(guestbook_name_before)
        guestbook_name_after = Guestbook.get_guestbook_by_name(guestbook_name_before)
        assert guestbook_name_after == guestbook_name_before

    def test_check_is_exist(self):
        guestbook_name_before = "test_check_is_exist"
        Guestbook.add_new_book(guestbook_name_before)
        is_exist = Guestbook.check_is_exist(guestbook_name_before)
        assert is_exist is True


class TestClassGreeting(TestBassClass):

    def test_get_greeting_with_cursor(self):
        for num in range(0, 25, 1):
            dictionary = {
                "guestbook_name": AppConstants.get_default_guestbook_name(),
                "content": str(num)
            }
            Greeting.put_from_dict(dictionary)

        greetings, next_cursor, is_more = Greeting.get_greeting_with_cursor(None, 20)
        assert (
            greetings is not None and len(greetings) == 20 and
            next_cursor is not None and is_more is True
        )


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
            "guestbook_name": AppConstants.get_default_guestbook_name(),
            "content": "test"
        }
        greeting = Greeting.put_from_dict(dictionary)
        dictionary_test = {
            "greeting_id": str(greeting.key.id),
            "guestbook_name": AppConstants.get_default_guestbook_name()
        }
        is_delete = Greeting.delete_greeting(dictionary_test)
        assert(is_delete is True)

    def test_update_greeting(self):
        dictionary = {
            "guestbook_name": AppConstants.get_default_guestbook_name(),
            "content": "test"
        }
        greeting = Greeting.put_from_dict(dictionary)

        dict_before = {
            "greeting_id": str(greeting.key.id),
            "guestbook_name": AppConstants.get_default_guestbook_name(),
            "author": str(greeting.author),
            "content": "test_version2"
        }
        greeting_after = Greeting.update_greeting(dict_before)
        assert(
            dict_before["greeting_id"] == str(greeting_after.key.id) and
            dict_before["author"] == str(greeting_after.author) and
            dict_before["content"] == str(greeting_after.content)
        )

    def test_get_greeting(self):
        dictionary = {
            "guestbook_name": AppConstants.get_default_guestbook_name(),
            "content": "test"
        }
        greeting = Greeting.put_from_dict(dictionary)

        dict_before = {
            "greeting_id": str(greeting.key.id),
            "guestbook_name": AppConstants.get_default_guestbook_name(),
            "author": str(greeting.author),
            "content": str(greeting.content)
        }
        greeting_after = Greeting.get_greeting(
            greeting.key.id, AppConstants.get_default_guestbook_name()
        )
        assert(
            dict_before["greeting_id"] == str(greeting_after.key.id) and
            dict_before["author"] == str(greeting_after.author) and
            dict_before["content"] == str(greeting_after.content)
        )








