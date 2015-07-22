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

	def tearDown(self):
		self.testbed.deactivate()

	def get_service(self):
		service_name = "GuestbookService"
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

	def test_create(self):
		new_guestbook_name = "new_guestbook_name"
		svc = self.get_service()
		res = svc.create(guestbook_name=new_guestbook_name)

		assert res is not None
		assert res.name == new_guestbook_name















