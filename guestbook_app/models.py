# -*- coding: utf-8 -*-

import datetime

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext.db import Timeout
from functools import wraps


def retry(transaction):
	@wraps(transaction)
	def wrapped(*args, **kwargs):
		try:
			return transaction(*args, **kwargs)
		except Timeout:
			raise "Can not connect to DB"
	return wrapped


class AppConstants(object):
	@staticmethod
	def get_default_guestbook_name():
		return "default_guestbook"


class Guestbook(ndb.Model):
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
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@retry
	def get_greeting_with_cursor(self, url_safe, guestbook_name, count=20):
		start_cursor = Cursor(urlsafe=url_safe)
		greetings, next_cursor, is_more = self.query(
			ancestor=Guestbook.get_guestbook_key(guestbook_name)).order(-Greeting.date)\
			.fetch_page(count, start_cursor=start_cursor)

		greeting_json = [
			{
				"greeting_id": greeting.key.id(),
				"greeting_auth": str(greeting.author),
				"greeting_content": greeting.content,
				"greeting_date": str(greeting.date)
			} for greeting in greetings
		]

		return greeting_json, next_cursor, is_more

	@retry
	def get_greetings(self, guestbook_name=AppConstants.get_default_guestbook_name(), count=20):
		greetings = self.query(ancestor=Guestbook.get_guestbook_key(guestbook_name))\
			.order(-Greeting.date).fetch(count)
		return greetings

	@retry
	def get_greeting(self, greeting_id, guestbook_name=AppConstants.get_default_guestbook_name()):
		try:
			greeting_id = int(greeting_id)
			key = ndb.Key("Guestbook", str(guestbook_name), "Greeting", greeting_id)
			greeting = key.get()
		except ValueError:
			raise ValueError("Khong the ep kieu")

		return greeting

	@retry
	def update_greeting(self, dictionary):
		greeting = self.get_greeting(dictionary["greeting_id"], dictionary["guestbook_name"])

		@ndb.transactional
		def txn(greeting):
			if greeting:
				greeting.put()
				return greeting
			return False

		if greeting:
			greeting.content = dictionary["content"]
			greeting.updated_date = datetime.datetime.now()
			if users.get_current_user():
				greeting.author = users.get_current_user()

		return txn(greeting)

	@retry
	def delete_greeting(self, dictionary):
		try:
			greeting_id = int(dictionary["greeting_id"])
			greeting = self.get_greeting(greeting_id, dictionary["guestbook_name"])

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
						ent.key.delete()
						return True
					return False

				return txn(key)
		except ValueError:
			raise ValueError("Khong the ep kieu")

	@retry
	def put_from_dict(self, dictionary):
		guestbook_name = dictionary["guestbook_name"]

		@ndb.transactional
		def txn(greeting):
			if greeting:
				greeting.put()
				return True
			return False

		if Guestbook.check_is_exist(guestbook_name) is False:
			Guestbook.add_new_book(guestbook_name)

		greeting = Greeting(parent=Guestbook.get_guestbook_key(guestbook_name))
		
		if users.get_current_user():
			greeting.author = users.get_current_user()
			
		greeting.content = dictionary["content"]
		
		return txn(greeting)
