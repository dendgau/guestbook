# -*- coding: utf-8 -*-

from django import http
from django.http import Http404, HttpResponse
from django.utils import simplejson as json
from django.views.generic.detail import DetailView

from google.appengine.ext import ndb

from guestbook.models import Greeting


class HttpResponseNoContent(HttpResponse):
    status_code = 204


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
    def get(self, **kwargs):
        greeting_id = kwargs["greeting_id"]
        guestbook_name = kwargs["guestbook_name"]

        greeting = Greeting.get_greeting(guestbook_name, greeting_id)
        if greeting is None:
            raise Http404

        data = {
            "greeting_id": str(greeting_id),
            "content": greeting.content,
            "date": str(greeting.date),
            "updated_by": str(greeting.author),
            "guestbook_name": guestbook_name
        }
        
        return self.render_to_response(data)


class GreetingDeleteService(DetailView):
    def get(self, **kwargs):
        greeting_id = kwargs["greeting_id"]
        guestbook_name = kwargs["guestbook_name"]
        
        greeting = Greeting.get_greeting(guestbook_name, greeting_id)
        if greeting is None:
            raise Http404
        else:
            dictionary = {
                'guestbook_name': guestbook_name,
                'greeting_id': greeting_id
            }
            Greeting.delete_greeting(dictionary)

        return HttpResponse(status=204)
