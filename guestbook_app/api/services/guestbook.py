# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from guestbook_app.api.models.guestbook import GuestbookModel, AppConstants

GUESTBOOK_DEFAULT = AppConstants.get_default_guestbook_name()


class GuestbookService(object):

	@staticmethod
	def create(guestbook_name=GUESTBOOK_DEFAULT, **kwargs):
		guestbook = GuestbookModel.create_guestbook()

		@ndb.transactional
		def txn(ent, **kwds):
			ent.populate(**kwds)
			ent.do_with_retry(lambda: ent.put())
			return ent

		return txn(guestbook, name=guestbook_name, **kwargs)

