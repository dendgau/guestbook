# -*- coding: utf-8 -*-
import pytest
import unittest
import importlib

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

	def get_service(self):
		service_name = "GreetingService"
		module_name = service_name.split("Service")[0]
		module_name = module_name.lower()
		services_module = '.'.join(("guestbook_app", "services", module_name))
		try:
			import_module = importlib.import_module(services_module)
		except ImportError:
			raise ImportError("Can't found module name")

		try:
			import_class = getattr(import_module, service_name)
		except AttributeError:
			raise AttributeError("Can't found class name")

		return import_class


class TestClassGreetingService(TestBassClass):

	def test_list_with_cursor_is_none(self):
		svc = self.get_service()
		res = svc.list(guestbook_name=GUESTBOOK_DEFAULT, url_safe=None, count=20)

		assert res["guestbook_name"] == GUESTBOOK_DEFAULT
		assert len(res["greetings"]) == 4
		assert res["more"] is False
		assert res["next_cursor"] is None

		expected = [greeting["greeting_id"] for greeting in res["greetings"]]
		assert [greeting["id"] for greeting in self.greetings] == expected

	def test_list_with_pagination(self):
		svc = self.get_service()
		res1 = svc.list(guestbook_name=GUESTBOOK_DEFAULT, url_safe=None, count=2)
		res2 = svc.list(guestbook_name=GUESTBOOK_DEFAULT, url_safe=res1["next_cursor"], count=2)

		assert res1["guestbook_name"] == GUESTBOOK_DEFAULT
		assert len(res1["greetings"]) == 2
		assert res1["more"] is True
		assert res1["next_cursor"] is not None

		assert res2["guestbook_name"] == GUESTBOOK_DEFAULT
		assert len(res2["greetings"]) == 2
		assert res2["more"] is False
		assert res2["next_cursor"] is None

		res1["greetings"].extend(res2["greetings"])
		expected = [greeting["greeting_id"] for greeting in res1["greetings"]]
		assert [greeting["id"] for greeting in self.greetings] == expected

	def test_list_with_greeting_id_is_true(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = self.greetings[0]["id"]
		content = self.greetings[0]["content"]

		svc = self.get_service()
		res = svc.get(guestbook_name=guestbook_name, greeting_id=greeting_id)

		assert guestbook_name == res["guestbook_name"]
		assert greeting_id == int(res["greeting_id"])
		assert content == res["content"]

	def test_list_with_greeting_id_is_false(self):
		svc = self.get_service()

		with pytest.raises(ValueError):
			res = svc.get(guestbook_name=GUESTBOOK_DEFAULT, greeting_id="wrong_id")

	def test_create_with_exist_guestbook_name(self):
		guestbook_name = GUESTBOOK_DEFAULT
		content = "blabla"

		svc = self.get_service()
		res = svc.create(guestbook_name=guestbook_name, content=content)

		assert res is not None
		assert res.key is not None
		assert res.content == content

	def test_create_with_guestbook_name_is_not_exist(self):
		guestbook_name = "guestbook_is_not_exist"
		content = "blabla"

		svc = self.get_service()
		res = svc.create(guestbook_name=guestbook_name, content=content)

		assert res is not None
		assert res.key is not None
		assert res.content == content

	def test_update_with_greeting_id_is_true(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = self.greetings[0]["id"]
		content_update = "blabla"

		svc = self.get_service()
		res = svc.update(guestbook_name=guestbook_name, greeting_id=greeting_id, content=content_update)

		assert res is not None
		assert res.content == content_update

	def test_update_with_wrong_greeting_id(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = "wrong_id"
		content_update = "blabla"

		svc = self.get_service()

		with pytest.raises(ValueError):
			res = svc.update(guestbook_name=guestbook_name, greeting_id=greeting_id, content=content_update)

	def test_update_with_greeting_id_is_not_exist(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = 100
		content_update = "blabla"

		svc = self.get_service()
		res = svc.update(guestbook_name=guestbook_name, greeting_id=greeting_id, content=content_update)

		assert res is False

	def test_update_with_greeting_id_is_true(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = self.greetings[0]["id"]

		svc = self.get_service()
		res = svc.delete(guestbook_name=guestbook_name, greeting_id=greeting_id)

		assert res is True

	def test_update_with_wrong_greeting_id(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = "wrong_id"

		svc = self.get_service()

		with pytest.raises(ValueError):
			res = svc.delete(guestbook_name=guestbook_name, greeting_id=greeting_id)

	def test_update_with_greeting_id_is_not_exist(self):
		guestbook_name = GUESTBOOK_DEFAULT
		greeting_id = 100

		svc = self.get_service()
		res = svc.update(guestbook_name=guestbook_name, greeting_id=greeting_id)

		assert res is False













