# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

from guestbook_app.views import SignView, GreetingEditView, GreetingDeleteView


admin.autodiscover()

urlpatterns = patterns(
	'',
	url(
		r"^$",
		TemplateView.as_view(
			template_name="dojo_template.html"),
		name="dojo"),
	url(
		r"^sign$",
		SignView.as_view(),
		name="sign"
	),
	url(
		r"^edit",
		GreetingEditView.as_view(),
		name="edit"
	),
	url(
		r"^delete$",
		GreetingDeleteView.as_view(),
		name="delete"
	),
	# access to API
	url(
		r"^api/",
		include('guestbook_app.api.urls')
	),
)
