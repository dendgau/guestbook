# -*- coding: utf-8 -*-
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor

from .decorator import retry


class AppConstants(object):
	"""Constants Application"""
	@staticmethod
	def get_default_guestbook_name():
		return "default_guestbook"


class Guestbook(ndb.Model):
	"""Guestbook Model"""
	name = ndb.StringProperty(indexed=True)
	
	@staticmethod
	def get_guestbook_key(guestbook_name=AppConstants.get_default_guestbook_name()):
		return ndb.Key('Guestbook', guestbook_name)
		
	@classmethod
	def get_guestbook_by_name(cls, guestbook_name):
		return cls.query(Guestbook.name == guestbook_name).get()
	
	@classmethod
	def check_is_exist(cls, guestbook_name):
		if cls.get_guestbook_by_name(guestbook_name) is None:
			return False
		return True
	
	@classmethod
	def add_new_book(cls, guestbook_name):
		guestbook = cls()

		@ndb.transactional
		@retry
		def txn(ent):
			ent.populate()
			return ent

		guestbook.populate(name=guestbook_name)
		return txn(guestbook)


class Greeting(ndb.Model):
	"""Greeting Model"""
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_greeting_with_cursor(cls, url_safe, guestbook_name, count=20):
		start_cursor = Cursor(urlsafe=url_safe)
		greetings, next_cursor, is_more = cls.query(
			ancestor=Guestbook.get_guestbook_key(guestbook_name)
		).order(-Greeting.date).fetch_page(count, start_cursor=start_cursor)

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
			ancestor=Guestbook.get_guestbook_key(guestbook_name)
		).order(-Greeting.date).fetch(count)

		return greetings

	@classmethod
	def get_greeting(cls, greeting_id, guestbook_name=AppConstants.get_default_guestbook_name()):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		key = ndb.Key("Guestbook", str(guestbook_name), "Greeting", greeting_id)
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
			@retry
			def txn(ent):
				ent.put()
				return ent

			greeting.populate(**kwargs)
			return txn(greeting)

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
			@retry
			def txn(ent):
				if ent:
					ent.key.delete()
					return True
				return False

			return txn(greeting)

		return False

	@classmethod
	def put_from_dict(cls, guestbook_name=AppConstants.get_default_guestbook_name(), **kwargs):

		@ndb.transactional
		@retry
		def txn(ent):
			ent.put()
			return ent

		is_guestbook_exist = True
		if Guestbook.check_is_exist(guestbook_name) is False:
			is_guestbook_exist = Guestbook.add_new_book(guestbook_name)

		if is_guestbook_exist:
			greeting = cls(parent=Guestbook.get_guestbook_key(guestbook_name))
			greeting.populate(**kwargs)

			return txn(greeting)

		return False
