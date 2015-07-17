# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

from guestbook_app.api.services.guestbook import GuestbookService
from guestbook_app.api.models.greeting import Greeting
from guestbook_app.api.models.guestbook import Guestbook, AppConstants

GUESTBOOK_DEFAULT = AppConstants.get_default_guestbook_name()


class GreetingService(object):

	@staticmethod
	def list(guestbook_name=GUESTBOOK_DEFAULT, url_safe=None, count=20, **kwargs):
		greetings, next_cursor, is_more = Greeting.get_greeting_with_cursor(
			url_safe=url_safe,
			guestbook_name=guestbook_name,
			count=count,
			**kwargs
		)

		data = {
			"guestbook_name": guestbook_name,
			"greetings": greetings,
			"more": is_more,
			"next_cursor": str(next_cursor.urlsafe()) if is_more else None
		}

		return data

	@staticmethod
	def get(greeting_id=None, guestbook_name=GUESTBOOK_DEFAULT, **kwargs):
		greeting = Greeting.get_greeting(greeting_id, guestbook_name)

		data = {
			"guestbook_name": guestbook_name,
			"greeting_id": str(greeting_id),
			"updated_by": str(greeting.author),
			"content": greeting.content,
			"date": str(greeting.date)
		}

		return data

	@staticmethod
	def create(guestbook_name=GUESTBOOK_DEFAULT, **kwargs):

		@ndb.transactional
		def txn(ent, **kwds):
			ent.populate(**kwds)
			ent.do_with_retry(lambda: ent.put())
			return ent

		is_guestbook_exist = True
		if Guestbook.check_is_exist(guestbook_name) is False:
			is_guestbook_exist = GuestbookService.create(guestbook_name)

		if is_guestbook_exist:
			greeting = Greeting.create_greeting(guestbook_name)
			return txn(greeting, **kwargs)

		return False

	@staticmethod
	def update(guestbook_name=GUESTBOOK_DEFAULT, greeting_id=None, **kwargs):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		greeting = Greeting.get_greeting(greeting_id, guestbook_name)
		if greeting:

			@ndb.transactional
			def txn(key, **kwds):
				ent = key.get()
				ent.populate(**kwds)
				ent.do_with_retry(lambda: ent.put())
				return ent

			return txn(greeting.key, **kwargs)

		return False

	@staticmethod
	def delete(guestbook_name=GUESTBOOK_DEFAULT, greeting_id=None, **kwargs):
		try:
			greeting_id = int(greeting_id)
		except ValueError:
			raise ValueError("Greeting ID must be a positive integer. Please try again!")

		greeting = Greeting.get_greeting(greeting_id, guestbook_name)
		if greeting:

			@ndb.transactional
			def txn(ent):
				if ent:
					ent.do_with_retry(lambda: ent.key.delete())
					return True
				return False

			return txn(greeting)

		return False