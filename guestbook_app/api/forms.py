# -*- coding: utf-8 -*-
from django import forms


class SignForm(forms.Form):
	content = forms.CharField(
		label="Greeting Massage",
		max_length=50,
		required=True,
		widget=forms.Textarea()
	)


class QueryCursorForm(forms.Form):
	url_safe = forms.CharField(
		max_length=200,
		required=False,
	)
	count = forms.IntegerField(
		min_value=10,
		max_value=100,
		required=False,
	)


class DeleteForm(forms.Form):
	guestbook_name = forms.CharField(
		max_length=20,
		required=False,
		widget=forms.HiddenInput()
	)
	greeting_id = forms.CharField(
		max_length=50,
		required=False,
		widget=forms.HiddenInput()
	)
