# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guestbook_app.api import forms
from guestbook_app.api import api

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
	'',
	url(
		r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$",
		api.SingleResourceView.as_view(
			service_name="GreetingService",
			form_class=forms.SignForm),
		name="greeting-service-detail"
	),
	url(
		r"^guestbook/(?P<guestbook_name>.+)/greeting$",
		api.CollectionResourceView.as_view(
			service_name="GreetingService",
			form_class=forms.SignForm,
			query_form_class=forms.QueryCursorForm),
		name="greeting-service")
)
