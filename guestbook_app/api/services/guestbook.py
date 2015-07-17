# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from guestbook_app.api.models.guestbook import Guestbook, AppConstants

GUESTBOOK_DEFAULT = AppConstants.get_default_guestbook_name()


class GuestbookService(object):

	@staticmethod
	def create(guestbook_name=GUESTBOOK_DEFAULT, **kwargs):

		@ndb.transactional
		def txn(**kwds):
			ent = Guestbook.create_guestbook()
			if ent:
				ent.populate(**kwds)
				ent.do_with_retry(lambda: ent.put())
				return ent
			return False

		return txn(name=guestbook_name, **kwargs)

