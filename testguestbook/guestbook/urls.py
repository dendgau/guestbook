# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guestbook.views import SignView, GreetingEditView, GreetingDeleteView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^sign$", SignView.as_view(), name="sign"),
                       url(r"^edit", GreetingEditView.as_view(), name="edit"),
                       url(r"^delete$", GreetingDeleteView.as_view(), name="delete"),)