# -*- coding: utf-8 -*-
import pytest
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from guestbook_app.models.greeting import Greeting
from guestbook_app.models.guestbook import AppConstants

GUESTBOOK_DEFAULT = AppConstants.get_default_guestbook_name()


class TestBassClass(unittest.TestCase):

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		self.greetings = []

		for num in range(0, 4, 1):
			greeting_instance = Greeting.init(GUESTBOOK_DEFAULT)
			greeting_instance.content = "greeting"+str(num+1)
			greeting_instance.put()

			self.greetings.insert(0, {
				"id": greeting_instance.key.id(),
				"key": greeting_instance.key,
				"author": greeting_instance.author,
				"content": greeting_instance.content,
				"date": greeting_instance.date
			})

	def tearDown(self):
		self.testbed.deactivate()


class TestClassGreeting(TestBassClass):

	def test_get_greeting_with_cursor_none(self):
		greetings, next_cursor, is_more = \
			Greeting.get_greeting_with_cursor(None, GUESTBOOK_DEFAULT)
		expected = [greeting["id"] for greeting in self.greetings]

		assert greetings is not None
		assert len(greetings) == 4
		assert [greeting["greeting_id"] for greeting in greetings] == expected

	def test_get_greeting_with_pagination(self):
		greetings1, next_cursor1, is_more1 = \
			Greeting.get_greeting_with_cursor(None, GUESTBOOK_DEFAULT, 2)

		greetings2, next_cursor2, is_more2 = \
			Greeting.get_greeting_with_cursor(next_cursor1.urlsafe(), GUESTBOOK_DEFAULT, 2)

		expected = [greeting["id"] for greeting in self.greetings]

		assert greetings1 is not None
		assert len(greetings1) == 2
		assert is_more1 is True

		assert greetings2 is not None
		assert len(greetings2) == 2
		assert is_more2 is False

		greetings1.extend(greetings2)

		assert [greeting["greeting_id"] for greeting in greetings1] == expected

	def test_get_greeting_with_none_pagination(self):
		greetings1, next_cursor1, is_more1 = \
			Greeting.get_greeting_with_cursor(None, GUESTBOOK_DEFAULT, 4)

		greetings2, next_cursor2, is_more2 = \
			Greeting.get_greeting_with_cursor(next_cursor1.urlsafe(), GUESTBOOK_DEFAULT, 4)

		expected = [greeting["id"] for greeting in self.greetings]

		assert greetings1 is not None
		assert len(greetings1) == 4
		assert is_more1 is False

		assert len(greetings2) == 0
		assert is_more2 is False

		greetings1.extend(greetings2)

		assert [greeting["greeting_id"] for greeting in greetings1] == expected

	def test_get_greeting_with_greeting_id_is_true(self):
		greeting_id = self.greetings[3]["id"]
		greeting = Greeting.get_greeting(GUESTBOOK_DEFAULT, greeting_id)

		assert greeting is not None
		assert greeting.key == self.greetings[3]["key"]

	def test_get_greeting_with_wrong_greeting_id(self):
		greeting_id = "bla bla bla"

		with pytest.raises(ValueError):
			greeting = Greeting.get_greeting(GUESTBOOK_DEFAULT, greeting_id)

	def test_get_greeting_with_greeting_id_is_not_exist(self):
		greeting_id = 100
		greeting = Greeting.get_greeting(GUESTBOOK_DEFAULT, greeting_id)

		assert greeting is None

	def test_do_with_retry_success(self):
		greeting_object = {"content": "greeting_test_retry0"}
		greeting_instance = Greeting.init(GUESTBOOK_DEFAULT)
		greeting_instance.populate(**greeting_object)
		greeting_instance.do_with_retry(lambda: greeting_instance.put())
		greeting_after = Greeting.get_greeting(GUESTBOOK_DEFAULT, greeting_instance.key.id())

		assert greeting_instance is not None
		assert greeting_instance is greeting_after

	def test_do_with_retry_with_wrong_try_count(self):
		greeting_object = {"content": "greeting_test_retry1"}
		greeting_instance = Greeting.init(GUESTBOOK_DEFAULT)
		greeting_instance.populate(**greeting_object)

		with pytest.raises(TypeError):
			greeting_instance.do_with_retry(lambda: greeting_instance.put(), try_count=0)

	def test_do_with_retry_with_wrong_back_off(self):
		greeting_object = {"content": "greeting_test_retry2"}
		greeting_instance = Greeting.init(GUESTBOOK_DEFAULT)
		greeting_instance.populate(**greeting_object)

		with pytest.raises(TypeError):
			greeting_instance.do_with_retry(lambda: greeting_instance.put(), back_off=-1)






