# -*- coding: utf-8 -*-
import datetime
import importlib

from django import http
from django.http import QueryDict
from django.utils import simplejson as json
from django.views.generic.edit import FormView, BaseFormView
from django.http import HttpResponse

from google.appengine.api import users

from guestbook_app.models import Greeting, AppConstants
from guestbook_app.views import SignForm


def _execute_service(view, method_name, **param):
	svc = view.get_service()
	kwargs = view.kwargs.copy()
	kwargs.update(param)

	method = getattr(svc, method_name, None)
	if method and callable(method):
		try:
			return method(**kwargs)
		except NotImplementedError, exc:
			view.logger.info('%r', exc, exc_info=1)


class JSONResponseMixin(object):
	def render_to_response(self, context):
		return self.get_json_response(self.convert_context_to_json(context))

	@staticmethod
	def get_json_response(content, **http_response_kwargs):
		return http.HttpResponse(content, content_type='application/json', **http_response_kwargs)

	@staticmethod
	def convert_context_to_json(context):
		return json.dumps(context)


class GreetingViewBase(JSONResponseMixin, BaseFormView):
	service_name = None

	def get_service(self):

		services_dir = '.'.join(("guestbook_app", "services", self.service_name))
		try:
			import_module = importlib.import_module(services_dir)
		except ImportError:
			raise ImportError("No module name")

		try:
			import_class = getattr(import_module, self.service_name)
		except AttributeError:
			raise AttributeError("No class name")

		return import_class

	def list_resources(self, **param):
		return _execute_service(self, 'list', **param)

	def get_resources(self, **param):
		return _execute_service(self, 'get', **param)

	def create_resources(self, **param):
		return _execute_service(self, 'create', **param)

	def update_resources(self, **param):
		return _execute_service(self, 'update', **param)

	def delete_resources(self, **param):
		return _execute_service(self, 'delete', **param)


class GreetingView(GreetingViewBase):

	def form_valid(self, form, *args, **kwargs):
		new_greeting = self.greeting_create(form, **kwargs)
		if new_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def form_invalid(self, form):
		return HttpResponse(status=400)

	def get(self, *args, **kwargs):
		url_safe = self.request.GET.get("cursor", None)
		guestbook_name = kwargs.get("guestbook_name", AppConstants.get_default_guestbook_name())

		res = self.list_resources(guestbook_name=guestbook_name, url_safe=url_safe)
		return self.render_to_response(res)

	def post(self, request, *args, **kwargs):
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

	def greeting_create(self, form, **kwargs):

		guestbook_name = self.kwargs.get(
			"guestbook_name",
			AppConstants.get_default_guestbook_name()
		)
		greeting_content = form.cleaned_data["greeting_message"]

		dictionary = {
			'content': greeting_content,
			'author': users.get_current_user() if users.get_current_user() else None
		}
		return self.create_resources(guestbook_name=guestbook_name, **dictionary)


class GreetingDetailView(GreetingViewBase):

	def form_valid(self, form):
		greeting = self.greeting_update(form)
		if greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def form_invalid(self, form):
		return HttpResponse(status=400)

	def get(self, request, *args, **kwargs):

		greeting_id = kwargs.get("greeting_id")
		guestbook_name = kwargs.get("guestbook_name")

		res = self.get_resources(greeting_id=greeting_id, guestbook_name=guestbook_name)
		if res is None:
			return HttpResponse(status=404)

		return self.render_to_response(res)

	def put(self, request, *args, **kwargs):
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

	def delete(self, *args, **kwargs):

		greeting_id = kwargs.get("greeting_id")
		guestbook_name = kwargs.get("guestbook_name")

		res = self.delete_resources(
			guestbook_name=guestbook_name,
			greeting_id=greeting_id
		)

		if res:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def greeting_update(self, form):

		greeting_id = self.kwargs.get("greeting_id")
		guestbook_name = self.kwargs.get("guestbook_name")
		greeting_content = form.cleaned_data["greeting_message"]

		dictionary = {
			'author': users.get_current_user() if users.get_current_user() else None,
			'content': greeting_content,
			'date': datetime.datetime.now(),
		}

		return self.update_resources(
			guestbook_name=guestbook_name,
			greeting_id=greeting_id,
			**dictionary
		)
