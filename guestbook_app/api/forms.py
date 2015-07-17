# -*- coding: utf-8 -*-
from django import forms


class SignForm(forms.Form):
	greeting_message = forms.CharField(
		label="Greeting Massage",
		max_length=50,
		required=True,
		widget=forms.Textarea()
	)


class QueryCursorForm(forms.Form):
	url_safe = forms.CharField(
		label="Cursor",
		max_length=200,
		required=False,
		widget=forms.TextInput()
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
