# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url, include
from guestbook.views import SignView, GreetingEditView, GreetingDeleteView
from API.views import GreetingServiceDetail
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
                           GreetingServiceDetail.as_view(),
                           name="test-greeting-edit"),

                       url(r"^test-get-greetings",
                           TemplateView.as_view(template_name="test_get_greetings.html"),
                           name="test-get-greetings"),
                       )