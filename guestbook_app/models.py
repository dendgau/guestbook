# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

from .decorator import retry


@retry(try_count=5, back_off=1)
def do_with_retry(func, *args, **kwargs):
	func(*args, **kwargs)


class AppConstants(object):
	"""Constants Application"""
	@staticmethod
	def get_default_guestbook_name():
		return "default_guestbook"


class GuestbookModel(ndb.Model):
	"""Guestbook Model"""
	name = ndb.StringProperty(indexed=True)
	
	@staticmethod
	def get_guestbook_key(guestbook_name=AppConstants.get_default_guestbook_name()):
		return ndb.Key('GuestbookModel', guestbook_name)
		
	@classmethod
	def get_guestbook_by_name(cls, guestbook_name):
		return cls.query(cls.name == guestbook_name).get()
	
	@classmethod
	def check_is_exist(cls, guestbook_name):
		if cls.get_guestbook_by_name(guestbook_name) is None:
			return False
		return True
	
	@classmethod
	def add_new_book(cls, guestbook_name):
		guestbook = cls()

		@ndb.transactional
		def txn(ent, **kwds):
			ent.populate(**kwds)
			do_with_retry(lambda: ent.put())
			return ent

		return txn(guestbook, name=guestbook_name)


class GreetingModel(ndb.Model):
	"""Greeting Model"""
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_greeting_with_cursor(cls, url_safe, guestbook_name, count=20):
		start_cursor = Cursor(urlsafe=url_safe)
		greetings, next_cursor, is_more = cls.query(
			ancestor=GuestbookModel.get_guestbook_key(guestbook_name)
		).order(-cls.date).fetch_page(count, start_cursor=start_cursor)

		greeting_json = [
			{
				"greeting_id": greeting.key.id(),
				"greeting_auth": str(greeting.author),
				"greeting_content": greeting.content,
				"greeting_date": str(greeting.date)
			} for greeting in greetings
		]

		return greeting_json, next_cursor, is_more

	@classmethod
	def get_greetings(cls, guestbook_name=AppConstants.get_default_guestbook_name(), count=20):
		greetings = cls.query(
			ancestor=GuestbookModel.get_guestbook_key(guestbook_name)
		).order(-cls.date).fetch(count)

		return greetings

	@classmethod
	def get_greeting(cls, greeting_id, guestbook_name=AppConstants.get_default_guestbook_name()):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		key = ndb.Key("GuestbookModel", str(guestbook_name), "GreetingModel", greeting_id)
		greeting = key.get()
		return greeting

	@classmethod
	def update_greeting(cls, guestbook_name, greeting_id, **kwargs):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		greeting = cls.get_greeting(greeting_id, guestbook_name)
		if greeting:

			@ndb.transactional
			def txn(key, **kwds):
				ent = key.get()
				ent.populate(**kwds)
				do_with_retry(lambda: ent.put())
				return ent

			return txn(greeting.key, **kwargs)

		return False

	@classmethod
	def delete_greeting(cls, guestbook_name, greeting_id):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		greeting = cls.get_greeting(greeting_id, guestbook_name)
		if greeting:

			@ndb.transactional
			def txn(ent):
				if ent:
					do_with_retry(lambda: ent.key.delete())
					return True
				return False

			return txn(greeting)

		return False

	@classmethod
	def put_from_dict(cls, guestbook_name=AppConstants.get_default_guestbook_name(), **kwargs):

		@ndb.transactional
		def txn(ent, **kwds):
			ent.populate(**kwds)
			do_with_retry(lambda: ent.put())
			return ent

		is_guestbook_exist = True
		if GuestbookModel.check_is_exist(guestbook_name) is False:
			is_guestbook_exist = GuestbookModel.add_new_book(guestbook_name)

		if is_guestbook_exist:
			greeting = cls(parent=GuestbookModel.get_guestbook_key(guestbook_name))
			return txn(greeting, **kwargs)

		return False
