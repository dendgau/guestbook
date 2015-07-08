# -*- coding: utf-8 -*-
import datetime

from django import http
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.generic.edit import FormView
from django.http import QueryDict

from google.appengine.api import users

from google.appengine.ext import ndb

from guestbook_app.models import Greeting, AppConstants
from guestbook_app.views import SignForm


class JSONResponseMixin(object):
	def render_to_response(self, context):
		return self.get_json_response(self.convert_context_to_json(context))

	def get_json_response(self, content, **httpresponse_kwargs):
		return http.HttpResponse(content,
			content_type='application/json',
			**httpresponse_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(context)


class GreetingService(JSONResponseMixin, FormView):
	form_class = SignForm
	success_url = '/'

	def get(self, *args, **kwargs):
		"""API GET list greetings"""

		url_safe = self.request.GET.get("cursor", None)
		guestbook_name = kwargs.get("guestbook_name")

		greetings, next_cursor, is_more = Greeting.get_greeting_with_cursor(
			url_safe,
			guestbook_name, 20
		)

		data = {
			"guestbook_name": guestbook_name,
			"greetings": greetings,
			"more": is_more,
			"next_cursor": str(next_cursor.urlsafe())
		}

		return self.render_to_response(data)

	def post(self, request, *args, **kwargs):
		"""Access to API POST greeting"""
		if self.request.POST:
			try:
				json_object = json.loads(self.request.body)
			except ValueError:
				self.request.POST = QueryDict(self.request.body)

			else:
				self.request.POST = json_object

		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		"""API POST greeting when form valid"""

		new_greeting = self.greeting_create(form)
		if new_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def form_invalid(self, form):
		"""API POST greeting when form invalid"""
		return HttpResponse(status=400)

	def greeting_create(self, form):
		"""Function update greeting"""

		guestbook_name = str(form.cleaned_data["guestbook_name"])

		dictionary = {
			'content': form.cleaned_data["greeting_message"],
			'author': users.get_current_user() if users.get_current_user() else "Anonymous",
		}
		return Greeting.put_from_dict(guestbook_name, **dictionary)


class GreetingServiceDetail(JSONResponseMixin, FormView):
	form_class = SignForm
	success_url = '/'

	def put(self, request, *args, **kwargs):
		"""API put (update) greeting"""

		try:
			json_object = json.loads(self.request.body)
		except ValueError:
			self.request.POST = QueryDict(self.request.body)
		else:
			self.request.POST = json_object

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		"""Implement when form put valid"""

		greeting = self.greeting_update(form)
		if greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def form_invalid(self, form):
		"""Implement when form put invalid"""
		return HttpResponse(status=400)

	def greeting_update(self, form):
		"""Implement when form put invalid"""

		greeting_id = self.kwargs.get("greeting_id")
		guestbook_name = self.kwargs.get("guestbook_name")
		greeting_content = form.cleaned_data["greeting_message"]

		dictionary = {
			'author': users.get_current_user() if users.get_current_user() else "Anonymous",
			'content': greeting_content,
			'date': datetime.datetime.now(),
		}

		return Greeting.update_greeting(
			guestbook_name=guestbook_name,
			greeting_id=greeting_id,
			**dictionary
		)

	def get(self, request, *args, **kwargs):
		"""API GET detail greeting"""

		greeting_id = kwargs.get("greeting_id")
		guestbook_name = kwargs.get("guestbook_name")

		greeting = Greeting.get_greeting(greeting_id, guestbook_name)
		if greeting is None:
			return HttpResponse(status=404)

		data = {
			"guestbook_name": guestbook_name,
			"greeting_id": str(greeting_id),
			"updated_by": str(greeting.author),
			"content": greeting.content,
			"date": str(greeting.date)
		}

		return self.render_to_response(data)

	def delete(self, *args, **kwargs):
		"""API DELETE greeting"""

		greeting_id = kwargs.get("greeting_id")
		guestbook_name = kwargs.get("guestbook_name")

		is_delete_success = Greeting.delete_greeting(guestbook_name, greeting_id)
		if is_delete_success is True:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)
