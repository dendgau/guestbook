from django.shortcuts import render, render_to_response
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.base import TemplateView
from django import forms
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import users
from google.appengine.ext import ndb

from guestbook.models import Greeting, Guestbook

import cgi
import urllib
import webapp2
import time
#FORM SIGN
class SignForm(forms.Form):
	guestbook_name = forms.CharField(
		label="Guestbook Name",
		max_length=10,
		required=True,
		widget=forms.TextInput()
	)
	greeting_message = forms.CharField(
		label = "Greeting Massage",
		max_length=50,
		required=True,
		widget=forms.Textarea()
	)
	greeting_id = forms.CharField(
		max_length=100,
		required=False,
		widget=forms.HiddenInput()
	)
	

class SignView(FormView):
    template_name = "greetingform.html"
    form_class = SignForm
    success_url = "signform"
    messages = {
        "greeting_create": {
            "level": messages.SUCCESS,
            "text": "Greeting create success."
        },
    }
	
    def form_valid(self, form):
		if self.messages.get("greeting_create"):
			messages.add_message(
				self.request,
				self.messages["greeting_create"]["level"],
				self.messages["greeting_create"]["text"]
			)	
		self.greeting_create(form)	
		
		return redirect("sign")
	
    def greeting_create(self, form):
		guestbook_name = form.cleaned_data["guestbook_name"]
		guestbook = Guestbook.query(Guestbook.name == guestbook_name).get()
		
		if guestbook is None:
			guestbook = Guestbook()
			guestbook.name = guestbook_name
			guestbook.put()
		
		greeting = Greeting()
		if users.get_current_user():
			greeting.author = users.get_current_user()
    
		greeting.content = form.cleaned_data["greeting_message"]
		greeting.guestbook = guestbook
		greeting.put()

class GreetingEditView(FormView):
    template_name = "greetingedit.html"
    form_class = SignForm
    success_url = "signform"
    messages = {
        "greeting_create": {
            "level": messages.SUCCESS,
            "text": "Greeting updated."
        },
    }
    
    def get_initial(self):
		initial = super(GreetingEditView, self).get_initial()
		
		greeting_id = self.request.GET.get("id")
		greeting = Greeting.query(Greeting.key==ndb.Key("Greeting", int(greeting_id))).get()
		#greeting = greeting.filter(Greeting.key == ndb.Key("Greeting", greeting_id)).get()
		
		initial["guestbook_name"] = greeting.guestbook.name
		initial["greeting_message"] = greeting.content
		initial["greeting_id"] = int(greeting_id)
		
		return initial
	
    def form_valid(self, form):
		if self.messages.get("greeting_create"):
			messages.add_message(
				self.request,
				self.messages["greeting_create"]["level"],
				self.messages["greeting_create"]["text"]
			)	
		self.greeting_update(form)	
		time.sleep(0.5)
		return redirect("/edit?id=" + str(form.cleaned_data["greeting_id"]))
	
    def greeting_update(self, form):
    	greeting_id = form.cleaned_data["greeting_id"]
    	greeting_content = form.cleaned_data["greeting_message"]
    	guestbook_name = form.cleaned_data["guestbook_name"]
    	
    	guestbook = Guestbook.query(Guestbook.name == guestbook_name).get()
    	if guestbook is None:
			guestbook = Guestbook()
			guestbook.name = guestbook_name
			guestbook.put()
        greeting = Greeting.query(Greeting.key==ndb.Key("Greeting", int(greeting_id))).get()
        greeting.content = greeting_content
        greeting.guestbook = guestbook
        greeting.put()

class GreetingDeleteView(TemplateView):	
	template_name = "greetingdelete.html"
	

def post_delete_greeting(request):
	if request.POST.get("btn_yes"):
		greeting_id = request.GET.get("id")
		key = ndb.Key("Greeting", int(greeting_id))
		greeting = key.get()
		greeting.key.delete()
	time.sleep(0.5)
	return redirect("/")
		
	
class MainView(TemplateView):
    template_name = "mainview.html"
    
    def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', "test1")
		#greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		#greetings_query = Greeting.query(Greeting.key==ndb.Key('Guestbook', 'a', 'Greeting', 5785905063264256)).order(-Greeting.date)
		greetings_query = Greeting.query().order(-Greeting.date)
		greetings = greetings_query.filter()
		
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.get_full_path())
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linktext = 'Login'
		
		template_values = {
			'isAdmin' : users.is_current_user_admin(),
			'userInfo' : users.get_current_user(),
			'greetings': greetings,
			'guestbook_name': guestbook_name,
			'url': url,
			'url_linktext': url_linktext,
		}

		return template_values;