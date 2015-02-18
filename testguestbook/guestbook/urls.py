from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf.urls.defaults import *

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from guestbook.views import MainView, SignView, GreetingEditView, GreetingDeleteView
admin.autodiscover()

from guestbook.views import MainView, SignView, GreetingEditView, GreetingDeleteView
urlpatterns = patterns("",           
	url(r"^sign$", SignView.as_view(), name="sign"),
	url(r"^edit$", GreetingEditView.as_view(), name="edit"),
	url(r"^delete$", GreetingDeleteView.as_view(), name="delete"),
)