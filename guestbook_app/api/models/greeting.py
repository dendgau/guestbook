# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

from guestbook_app.api.models.guestbook import Guestbook
from guestbook_app.decorator import retry


class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_greeting_with_cursor(cls, url_safe, guestbook_name, count=20):
		start_cursor = Cursor(urlsafe=url_safe)
		greetings, next_cursor, is_more = cls.query(
			ancestor=Guestbook.get_guestbook_key(guestbook_name)
		).order(-cls.date).fetch_page(count, start_cursor=start_cursor)

		greeting_json = [
			{
				"greeting_id": greeting.key.id(),
				"greeting_auth": str(greeting.author),
				"greeting_content": str(greeting.content),
				"greeting_date": str(greeting.date)
			} for greeting in greetings
		]

		return greeting_json, next_cursor, is_more

	@classmethod
	def get_greeting(cls, guestbook_name, greeting_id):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		key = ndb.Key("Guestbook", str(guestbook_name), "Greeting", greeting_id)
		greeting = key.get()
		return greeting

	@classmethod
	def create_greeting(cls, guestbook_name):
		return cls(parent=Guestbook.get_guestbook_key(guestbook_name))

	@staticmethod
	def do_with_retry(function, *args, **kwargs):

		@retry(try_count=5, back_off=1)
		def do_retry(func):
			func(*args, **kwargs)

		do_retry(function)
