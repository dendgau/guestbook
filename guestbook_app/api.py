# -*- coding: utf-8 -*-

from django import http
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.generic.edit import FormView
from django.http import QueryDict

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

		dictionary = {
			'guestbook_name': form.cleaned_data["guestbook_name"],
			'content': form.cleaned_data["greeting_message"]
		}
		return Greeting.put_from_dict(dictionary)


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
		book_id = self.kwargs.get("guestbook_name")
		greeting_content = form.cleaned_data["greeting_message"]

		dictionary = {
			'guestbook_name': book_id,
			'greeting_id': greeting_id,
			'content': greeting_content
		}

		return Greeting.update_greeting(dictionary)

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
			"content": greeting.content,
			"date": str(greeting.date),
			"updated_by": str(greeting.author),
		}

		return self.render_to_response(data)

	def delete(self, *args, **kwargs):
		"""API DELETE greeting"""

		greeting_id = kwargs.get("greeting_id")
		guestbook_name = kwargs.get("guestbook_name")

		dictionary = {
			'guestbook_name': guestbook_name,
			'greeting_id': greeting_id
		}

		is_delete_success = Greeting.delete_greeting(dictionary)
		if is_delete_success is True:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)
