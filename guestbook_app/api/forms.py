# -*- coding: utf-8 -*-
from django import forms


class SignForm(forms.Form):
	content = forms.CharField(
		max_length=50,
		required=True,
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