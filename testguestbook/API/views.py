# -*- coding: utf-8 -*-

from django import http
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from google.appengine.ext import ndb

from guestbook.models import Greeting, AppConstants
from guestbook.views import SignForm


class JSONResponseMixin(object):
    def render_to_response(self, context):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class GreetingService(JSONResponseMixin, DetailView):
    def get(self, *args, **kwargs):
        url_safe = self.request.GET.get("cursor", None)
        guestbook_name = kwargs.get("guestbook_name", AppConstants.get_default_guestbook_name())
        greetings, next_cursor, is_more = Greeting.get_greeting_with_cursor(url_safe, 1)

        greeting_json = []
        for greeting in greetings:
            greeting_object = {}
            greeting_object["greeting_auth"] = str(greeting.author)
            greeting_object["greeting_content"] = str(greeting.content)
            greeting_object["greeitng_date"] = str(greeting.date)
            greeting_json.append(greeting_object)

        data = {
            "guestbook_name": guestbook_name,
            "greetings": greeting_json,
            "more": is_more,
            "next_cursor": str(next_cursor.urlsafe())
        }

        return self.render_to_response(data)


class GreetingServiceDetail(JSONResponseMixin, FormView):
    form_class = SignForm
    template_name = "test_greeting_edit.html"
    success_url = '/'

    def get_initial(self):
        initial = super(GreetingServiceDetail, self).get_initial()

        book_id = self.request.GET.get("book")
        greeting_id = self.request.GET.get("id")
        greeting = Greeting.get_greeting(greeting_id, book_id)

        initial["greeting_message"] = greeting.content
        initial["guestbook_name"] = book_id
        return initial

    def form_valid(self, form):
        self.greeting_update(form)
        return super(GreetingServiceDetail, self).form_valid(form)

    def greeting_update(self, form):
        greeting_id = self.request.GET.get("id")
        book_id = self.request.GET.get("book")
        greeting_content = form.cleaned_data["greeting_message"]
        dictionary = {
            'guestbook_name': book_id,
            'greeting_id': greeting_id,
            'content': greeting_content
        }
        Greeting.update_greeting(dictionary)

    def get(self, request, *args, **kwargs):
        greeting_id = kwargs.get("greeting_id")
        guestbook_name = kwargs.get("guestbook_name", AppConstants.get_default_guestbook_name())

        greeting = Greeting.get_greeting(greeting_id, guestbook_name)
        if greeting is None:
            return HttpResponse(status=404)

        data = {
            "greeting_id": str(greeting_id),
            "content": greeting.content,
            "date": str(greeting.date),
            "updated_by": str(greeting.author),
            "guestbook_name": guestbook_name
        }

        return self.render_to_response(data)

    def delete(self, *args, **kwargs):
        greeting_id = kwargs.get("greeting_id")
        guestbook_name = kwargs.get("guestbook_name", AppConstants.get_default_guestbook_name())

        greeting = Greeting.get_greeting(greeting_id, guestbook_name)
        if greeting is None:
            return HttpResponse(status=404)
        else:
            dictionary = {
                'guestbook_name': guestbook_name,
                'greeting_id': greeting_id
            }
            Greeting.delete_greeting(dictionary)

            return HttpResponse(status=204)
