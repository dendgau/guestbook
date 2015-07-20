# -*- coding: utf-8 -*-
import importlib

from django import http
from django.http import QueryDict
from django.utils import simplejson as json
from django.views.generic.edit import BaseFormView
from django.http import HttpResponse

from guestbook_app.models.guestbook import AppConstants

GUESTBOOK_DEFAULT = AppConstants.get_default_guestbook_name()


def _execute_service(view, method_name, form=None, **extra):
	svc = view.get_service()
	kwargs = view.kwargs.copy()
	kwargs.update(extra)

	if form is not None:
		kwargs.update(form.cleaned_data)

	method = getattr(svc, method_name, None)
	if method and callable(method):
		try:
			return method(**kwargs)
		except NotImplementedError:
			raise NotImplementedError("Can't found method in class")


class JSONResponseMixin(object):
	def render_to_response(self, context):
		return self.get_json_response(self.convert_context_to_json(context))

	@staticmethod
	def get_json_response(content, **http_response_kwargs):
		return http.HttpResponse(content, content_type='application/json', **http_response_kwargs)

	@staticmethod
	def convert_context_to_json(context):
		return json.dumps(context)


class ResourceViewBase(JSONResponseMixin, BaseFormView):
	service_name = None
	query_form_class = None

	def get_service(self):
		module_name = self.service_name.split("Service")[0]
		module_name = module_name.lower()
		services_module = '.'.join(("guestbook_app", "services", module_name))
		try:
			import_module = importlib.import_module(services_module)
		except ImportError:
			raise ImportError("Can't found module name")

		try:
			import_class = getattr(import_module, self.service_name)
		except AttributeError:
			raise AttributeError("Can't found class name")

		return import_class

	def get_query_form(self, query_form_class):
		kwargs = {}
		kwargs.update({
			'data': self.request.GET,
		})
		return query_form_class(**kwargs)


class CollectionResourceView(ResourceViewBase):

	def get(self, *args, **kwargs):
		query_form = self.get_query_form(self.query_form_class)

		if not query_form.is_valid():
			return HttpResponse(status=400)

		res = self.list_resources(query_form, **kwargs)
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

		if not form.is_valid():
			return HttpResponse(status=400)

		new_greeting = self.create_resources(form, **kwargs)
		if new_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def list_resources(self, form, **extra):
		return _execute_service(self, 'list', form, **extra)

	def create_resources(self, form, **extra):
		return _execute_service(self, 'create', form, **extra)


class SingleResourceView(ResourceViewBase):

	def get(self, request, *args, **kwargs):

		res = self.get_resources(**kwargs)
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

		if not form.is_valid():
			return HttpResponse(status=400)

		update_greeting = self.update_resources(form, **kwargs)
		if update_greeting:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def delete(self, *args, **kwargs):
		res = self.delete_resources(**kwargs)
		if res:
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	def get_resources(self, **extra):
		return _execute_service(self, 'get', **extra)

	def update_resources(self, form, **extra):
		return _execute_service(self, 'update', form, **extra)

	def delete_resources(self, **extra):
		return _execute_service(self, 'delete', **extra)
