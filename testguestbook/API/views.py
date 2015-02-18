from django.shortcuts import render, render_to_response
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView

from django.http import HttpResponse
from google.appengine.ext import ndb

from guestbook.models import Greeting, Guestbook
import cgi
import urllib
import webapp2
import time

from django import http
from django.utils import simplejson as json

from django.http import Http404
from django.views.generic import View
#from bottle import request

class HttpResponseNoContent(HttpResponse):
    status_code = 204

class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class GreetingService(JSONResponseMixin, DetailView):
    def get(self, request, *args, **kwargs):
            greeting_id = kwargs["greeting_id"]
            guestbook_name = kwargs["guestbook_name"]
            
            greeting = Greeting.get_greeting(guestbook_name, greeting_id)
            if greeting is None:
                raise Http404
            
            data = {
                "greeting_id" : str(greeting_id),
                "content" : greeting.content,
                "date" : str(greeting.date),
                "updated_by" : str(greeting.author),
                "guestbook_name" : guestbook_name
            }
        
            return self.render_to_response(data)
    
class GreetingDeleteService(DetailView):
    def get(self, request, *args, **kwargs):
        greeting_id = kwargs["greeting_id"]
        guestbook_name = kwargs["guestbook_name"]
        
        greeting = Greeting.get_greeting(guestbook_name, greeting_id)
        if greeting is None:
            raise Http404
        else:
            dictionary = {
                  'guestbook_name' : guestbook_name,
                  'greeting_id' : greeting_id        
            }
            Greeting.delete_greeting(dictionary)
        return HttpResponse(status=204)
