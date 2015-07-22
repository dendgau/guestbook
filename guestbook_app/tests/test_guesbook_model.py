# -*- coding: utf-8 -*-
import pytest
import unittest

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from guestbook_app.models.guestbook import Guestbook

GUESTBOOK_OBJECT = {"name": "guestbook_data1"}


class TestBassClass(unittest.TestCase):

	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()

		guestbook_instance = Guestbook.init()
		guestbook_instance.populate(**GUESTBOOK_OBJECT)
		guestbook_instance.put()

	def tearDown(self):
		self.testbed.deactivate()


class TestClassGuestbook(TestBassClass):

	def test_get_guestbook_key(self):
		key_before = ndb.Key('Guestbook', "guestbook_key")
		key_after = Guestbook.get_guestbook_key("guestbook_key")
		assert key_after == key_before

	def test_get_guestbook_by_name(self):
		guestbook_name_before = GUESTBOOK_OBJECT["name"]
		guestbook_name_after = (Guestbook.get_guestbook_by_name(guestbook_name_before)).name
		assert guestbook_name_after is not None
		assert guestbook_name_after == guestbook_name_before

	def test_check_is_exist(self):
		guestbook_name_before = GUESTBOOK_OBJECT["name"]
		is_exist = Guestbook.check_is_exist(guestbook_name_before)
		assert is_exist is True

	def test_check_is_not_exist(self):
		guestbook_name_before = "bla_bla_bla"
		is_exist = Guestbook.check_is_exist(guestbook_name_before)
		assert is_exist is False

	def test_do_with_retry_success(self):
		guestbook_object = {"name": "guestbook_data2"}
		guestbook_instance = Guestbook.init()
		guestbook_instance.populate(**guestbook_object)
		guestbook_instance.do_with_retry(lambda: guestbook_instance.put())
		guestbook_after = Guestbook.get_guestbook_by_name(guestbook_object["name"])

		assert guestbook_instance is not None
		assert guestbook_instance is guestbook_after

	def test_do_with_retry_with_wrong_try_count(self):
		guestbook_object = {"name": "guestbook_data3"}
		guestbook_instance = Guestbook.init()
		guestbook_instance.populate(**guestbook_object)

		with pytest.raises(TypeError):
			guestbook_instance.do_with_retry(lambda: guestbook_instance.put(), try_count=0)

	def test_do_with_retry_with_wrong_back_off(self):
		guestbook_object = {"name": "guestbook_data4"}
		guestbook_instance = Guestbook.init()
		guestbook_instance.populate(**guestbook_object)

		with pytest.raises(TypeError):
			guestbook_instance.do_with_retry(lambda: guestbook_instance.put(), back_off=-1)



