from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testguestbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
	url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
