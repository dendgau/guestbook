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

from guestbook.models import Greeting, Guestbook, DEFAULT_GUESTBOOK_NAME

import cgi
import urllib
import webapp2
import time
from types import DictionaryType
#FORM SIGN
class SignForm(forms.Form):
	guestbook_name = forms.CharField(
		label="Guestbook Name",
		max_length=20,
		required=True,
		widget=forms.TextInput()
	)
	greeting_message = forms.CharField(
		label = "Greeting Massage",
		max_length=50,
		required=True,
		widget=forms.Textarea()
	)
	
class DeleteForm(forms.Form):
	guestbook_name = forms.CharField(
		label="Guestbook Name",
		max_length=20,
		widget=forms.HiddenInput()
	)
	greeting_id = forms.CharField(
		label = "Greeting ID",
		max_length=50,
		widget=forms.HiddenInput()
	)
	

class SignView(FormView):
    template_name = "greetingform.html"
    form_class = SignForm
    messages = {
        "greeting_create": {
            "level": messages.SUCCESS,
            "text": "Greeting create success."
        },
    }
    
    def get_initial(self):
		initial = super(SignView, self).get_initial()
		initial["guestbook_name"] = DEFAULT_GUESTBOOK_NAME

		return initial
	
    def form_valid(self, form):
		if self.messages.get("greeting_create"):
			messages.add_message(
				self.request,
				self.messages["greeting_create"]["level"],
				self.messages["greeting_create"]["text"]
			)	
		self.greeting_create(form)	
		self.success_url = 'sign'
		
		return super(SignView, self).form_valid(form)
	
    def greeting_create(self, form):
    	dictionary = {
			'guestbook_name' : form.cleaned_data["guestbook_name"],
			'content' : form.cleaned_data["greeting_message"]
		}
    	Greeting.put_from_dict(dictionary)

class GreetingEditView(FormView):
    template_name = "greetingedit.html"
    form_class = SignForm
    #success_url = "signform"
    messages = {
        "greeting_create": {
            "level": messages.SUCCESS,
            "text": "Greeting updated."
        },
    }
    
    def get_initial(self):
		initial = super(GreetingEditView, self).get_initial()
		
		greeting_id = self.request.GET.get("id")
		book_id = self.request.GET.get("book")
		
		greeting = Greeting.get_greeting(book_id, greeting_id)
		
		initial["greeting_message"] = greeting.content
		initial["guestbook_name"] = book_id
		
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
		self.success_url = '/'
		return super(GreetingEditView, self).form_valid(form)
	
    def greeting_update(self, form):
    	greeting_id = self.request.GET.get("id")
    	book_id = self.request.GET.get("book")
    	greeting_content = form.cleaned_data["greeting_message"]
    	
    	dictionary = {
				'guestbook_name' : book_id,
				'greeting_id' : greeting_id,
				'content' : greeting_content
		}
    	greeting = Greeting.update_greeting(dictionary)

class GreetingDeleteView(FormView):	
	template_name = "greetingdelete.html"
	form_class = DeleteForm
	
	def get_initial(self):
		initial = super(GreetingDeleteView, self).get_initial()
		
		greeting_id = self.request.GET.get("id")
		book_id = self.request.GET.get("book")
		
		#greeting = Greeting.get_greeting(book_id, greeting_id)
		
		initial["greeting_id"] = greeting_id
		initial["guestbook_name"] = book_id
		
		return initial
	
	def form_valid(self, form):
		self.greeting_delete(form)	
		time.sleep(0.5)
		self.success_url = '/'
		return super(GreetingDeleteView, self).form_valid(form)
	
	def greeting_delete(self, form):
		if self.request.POST.get("btn_yes"):
			greeting_id = self.request.GET.get("id")
			guestbook_name = self.request.GET.get("book")
			dictionary = {
				'greeting_id' : greeting_id,
				'guestbook_name' : guestbook_name
			}
			Greeting.delete_greeting(dictionary)
	
class MainView(TemplateView):
    template_name = "mainview.html"
    
    def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		#greetings = Greeting.get_greetings(guestbook_name, 20)
		greetings = Greeting.get_all_greetings(20)
		
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