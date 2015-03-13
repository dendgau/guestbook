# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from API.views import GreetingServiceDetail, GreetingService

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$",
                           GreetingServiceDetail.as_view(), name="greeting-service-detail"),

                       url(r"^guestbook/(?P<guestbook_name>.+)/greeting$",
                           GreetingService.as_view(), name="greeting-service"))
