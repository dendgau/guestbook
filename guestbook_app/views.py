# -*- coding: utf-8 -*-

from google.appengine.api import users
from google.appengine.ext import ndb

from django import forms
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from guestbook_app.models import Greeting, AppConstants


class SignForm(forms.Form):
    guestbook_name = forms.CharField(
        label="Guest_book Name",
        max_length=20,
        required=False,
        widget=forms.TextInput()
    )
    greeting_message = forms.CharField(
        label="Greeting Massage",
        max_length=50,
        required=True,
        widget=forms.Textarea()
    )


class DeleteForm(forms.Form):
    guestbook_name = forms.CharField(
        label="Guestbook Name",
        max_length=20,
        required=False,
        widget=forms.HiddenInput()
    )
    greeting_id = forms.CharField(
        label="Greeting ID",
        max_length=50,
        required=False,
        widget=forms.HiddenInput()
    )


class SignView(FormView):
    form_class = SignForm
    template_name = "greeting_form.html"
    success_url = 'sign'
    messages = {
        "greeting_create": {
            "level": messages.SUCCESS,
            "text": "Greeting create success."
        },
    }
    
    def get_initial(self):
        initial = super(SignView, self).get_initial()
        initial["guestbook_name"] = AppConstants.get_default_guestbook_name()
        return initial

    def form_valid(self, form):
        if self.messages.get("greeting_create"):
            messages.add_message(
                self.request,
                self.messages["greeting_create"]["level"],
                self.messages["greeting_create"]["text"]
            )
        self.greeting_create(form)
        return super(SignView, self).form_valid(form)

    def greeting_create(self, form):
        dictionary = {
            'guestbook_name': form.cleaned_data["guestbook_name"],
            'content': form.cleaned_data["greeting_message"]
        }
        Greeting.put_from_dict(dictionary)


class GreetingEditView(FormView):
    form_class = SignForm
    template_name = "greeting_edit.html"
    success_url = "/"
    
    def get_initial(self):
        initial = super(GreetingEditView, self).get_initial()

        guestbook_name = self.request.GET.get("guestbook_name")
        greeting_id = self.request.GET.get("greeting_id")
        greeting = Greeting.get_greeting(greeting_id, guestbook_name)

        initial["greeting_message"] = greeting.content
        initial["guestbook_name"] = guestbook_name
        return initial

    def form_valid(self, form):
        self.greeting_update(form)
        return super(GreetingEditView, self).form_valid(form)

    def greeting_update(self, form):
        greeting_id = self.request.GET.get("greeting_id")
        guestbook_name = form.cleaned_data["guestbook_name"]
        greeting_content = form.cleaned_data["greeting_message"]
        dictionary = {
            'guestbook_name': guestbook_name,
            'greeting_id': greeting_id,
            'content': greeting_content
        }
        Greeting.update_greeting(dictionary)


class GreetingDeleteView(FormView):
    form_class = DeleteForm
    template_name = "greeting_delete.html"
    success_url = '/'

    def get_initial(self):
        initial = super(GreetingDeleteView, self).get_initial()

        guestbook_name = self.request.GET.get("guestbook_name")
        greeting_id = self.request.GET.get("greeting_id")

        initial["greeting_id"] = greeting_id
        initial["guestbook_name"] = guestbook_name

        return initial

    def form_valid(self, form):
        self.greeting_delete(form)
        return super(GreetingDeleteView, self).form_valid(form)

    def greeting_delete(self, form):
        if self.request.POST.get("btn_yes"):
            greeting_id = form.cleaned_data["greeting_id"]
            guestbook_name = form.cleaned_data["guestbook_name"]
            dictionary = {
                'greeting_id': greeting_id,
                'guestbook_name': guestbook_name
            }
            Greeting.delete_greeting(dictionary)


class MainView(TemplateView):
    template_name = "main_view.html"
    
    def get_context_data(self):
        guestbook_name = self.request.GET.get('guestbook_name', AppConstants.get_default_guestbook_name())
        greetings = Greeting.get_greetings(guestbook_name)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.get_full_path())
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.get_full_path())
            url_linktext = 'Login'

        template_values = {
            'isAdmin': users.is_current_user_admin(),
            'userInfo': users.get_current_user(),
            'greetings': greetings,
            'guestbook_name': guestbook_name,
            'url': url,
            'url_linktext': url_linktext,
        }

        return template_values