from django.conf.urls import patterns, url
from API.views import GreetingService, GreetingDeleteService

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$",
                           GreetingService.as_view()),

                       url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$",
                           GreetingDeleteService.as_view()),
                       )
