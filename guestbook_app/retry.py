# -*- coding: utf-8 -*-
import logging
from functools import wraps
from google.appengine.ext import db
from google.appengine.runtime import apiproxy_errors


RETRY_ACCESS_DATASTORE_ERRORS = (
	db.Timeout,
	db.InternalError,
	db.TransactionFailedError,
	apiproxy_errors.DeadlineExceededError
)


def retry(try_count=5, back_off=1):

	if try_count < 1:
		raise TypeError("Count of retry must be greater than 1")

	if back_off <= 0:
		raise TypeError("Backoff must be greater than 1")

	def wrapper(func):

		@wraps(func)
		def wrapped(*args, **kwargs):
			count = int(try_count) - 1
			delay = int(back_off)

			while True:
				try:
					return func(*args, **kwargs)
				except RETRY_ACCESS_DATASTORE_ERRORS:
					if count < 1:
						raise logging.info("Can not access to Database. Please try again!")
					count -= 1
					delay(delay)

		return wrapped

	return wrapper