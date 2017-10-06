from django.conf.urls import patterns, include, url
from django.contrib import admin
from subscribers.views import subsciber_new

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crmapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$',subsciber_new,name='signup'),
)
