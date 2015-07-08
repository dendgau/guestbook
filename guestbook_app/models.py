# -*- coding: utf-8 -*-
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor

from .retry import retry


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
		guestbook.name = guestbook_name
		guestbook.put()
		return guestbook


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
			key = ndb.Key("Guestbook", str(guestbook_name), "Greeting", greeting_id)
			greeting = key.get()
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		return greeting

	@classmethod
	def update_greeting(cls, dictionary):
		greeting = cls.get_greeting(dictionary["greeting_id"], dictionary["guestbook_name"])

		@ndb.transactional
		def txn(ent):
			if ent:
				retry(try_count=5, back_off=1)(lambda: ent.put())()
				return ent
			return False

		if greeting:
			greeting.content = dictionary["content"]
			greeting.updated_date = datetime.datetime.now()
			if users.get_current_user():
				greeting.author = users.get_current_user()

		return txn(greeting)

	@classmethod
	def delete_greeting(cls, dictionary):
		try:
			greeting_id = int(dictionary["greeting_id"])
			greeting = cls.get_greeting(greeting_id, dictionary["guestbook_name"])

			if greeting is None:
				return False
			else:
				key = ndb.Key(
					"Guestbook", dictionary["guestbook_name"],
					"Greeting", greeting_id
				)

				@ndb.transactional
				def txn(key):
					ent = key.get()
					if ent:
						retry(try_count=5, back_off=1)(lambda: ent.key.delete())()
						return True
					return False

				return txn(key)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

	@classmethod
	def put_from_dict(cls, dictionary):
		guestbook_name = dictionary["guestbook_name"]

		@ndb.transactional
		def txn(ent):
			if ent:
				retry(try_count=5, back_off=1)(lambda: ent.put())()
				return True
			return False

		if Guestbook.check_is_exist(guestbook_name) is False:
			Guestbook.add_new_book(guestbook_name)

		greeting = Greeting(parent=Guestbook.get_guestbook_key(guestbook_name))
		greeting.content = dictionary["content"]
		if users.get_current_user():
			greeting.author = users.get_current_user()
		
		return txn(greeting)
