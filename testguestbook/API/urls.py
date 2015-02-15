from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf.urls.defaults import *

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from guestbook.views import MainView, SignView, GreetingEditView, GreetingDeleteView
from API.views import GreetingService, GreetingDeleteService
admin.autodiscover()

urlpatterns = patterns('',
	url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$", GreetingService.as_view()),
	url(r"^guestbook/(?P<guestbook_name>.+)/greeting/(?P<greeting_id>\d+)$", GreetingDeleteService.as_view()),
)
