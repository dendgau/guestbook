from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.conf.urls.defaults import *

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from guestbook.views import MainView, SignView, GreetingEditView, GreetingDeleteView
admin.autodiscover()

urlpatterns = patterns('',

	url(r"^$", MainView.as_view(), name="home"),
	url(r'^guestbook/', include('guestbook.urls')),
	
)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
