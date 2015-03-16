# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from guestbook_app.views import SignView, GreetingEditView, GreetingDeleteView
from guestbook_app.api import GreetingServiceDetail, GreetingService
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^sign$",
                           SignView.as_view(),
                           name="sign"),

                       url(r"^edit",
                           GreetingEditView.as_view(),
                           name="edit"),

                       url(r"^delete$",
                           GreetingDeleteView.as_view(),
                           name="delete"),

                       url(r"^test-greeting-detail",
                           TemplateView.as_view(template_name="test_greeting_detail.html"),
                           name="test-greeting-detail"),

                       url(r"^test-greeting-edit",
                           TemplateView.as_view(template_name="test_greeting_edit.html"),
                           name="test-greeting-edit"),

                       url(r"^test-get-greetings",
                           TemplateView.as_view(template_name="test_get_greetings.html"),
                           name="test-get-greetings"),

                       url(r"^test-greeting-add",
                           TemplateView.as_view(template_name="test_greeting_add.html"),
                           name="test-greeting-add"),

                       url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$",
                           GreetingServiceDetail.as_view(), name="greeting-service-detail"),

                       url(r"^guestbook/(?P<guestbook_name>.+)/greeting$",
                           GreetingService.as_view(), name="greeting-service"))

