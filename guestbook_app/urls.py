# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guestbook_app.views import SignView, GreetingEditView, GreetingDeleteView
from guestbook_app.api import GreetingServiceDetail, GreetingService
from django.views.generic.base import TemplateView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	url(r"^sign$", SignView.as_view(), name="sign"),
	url(r"^edit", GreetingEditView.as_view(), name="edit"),
	url(r"^delete$", GreetingDeleteView.as_view(), name="delete"),
	url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$",
					GreetingServiceDetail.as_view(), name="greeting-service-detail"),
	url(r"^guestbook/(?P<guestbook_name>.+)/greeting$",
					GreetingService.as_view(), name="greeting-service"),
	url(r"^test-get-greeting-by-dojo$",
					TemplateView.as_view(template_name="main_template_get_greeting_by_dojo.html"),
					name="test-get-greeting-by-dojo$"),)
