# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from guestbook_app.views import MainView

admin.autodiscover()

urlpatterns = patterns('',
	url(r"^$", MainView.as_view(), name="home"),
	url(r'^guestbook_app/', include('guestbook_app.urls')),
)

