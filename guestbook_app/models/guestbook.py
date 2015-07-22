# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from guestbook_app.decorator import retry


class AppConstants(object):

	@staticmethod
	def get_default_guestbook_name():
		return "default_guestbook"


class Guestbook(ndb.Model):
	name = ndb.StringProperty(indexed=True)

	@classmethod
	def init(cls):
		return cls()

	@classmethod
	def get_guestbook_key(cls, guestbook_name):
		return ndb.Key(cls, guestbook_name)
		
	@classmethod
	def get_guestbook_by_name(cls, guestbook_name):
		return cls.query(cls.name == guestbook_name).get()
	
	@classmethod
	def check_is_exist(cls, guestbook_name):
		if cls.get_guestbook_by_name(guestbook_name) is None:
			return False
		return True

	@staticmethod
	def do_with_retry(function, try_count=5, back_off=1, *args, **kwargs):

		@retry(try_count=try_count, back_off=back_off)
		def do_retry(func):
			func(*args, **kwargs)

		do_retry(function)