from django.conf.urls import patterns, include, url
from django.contrib import admin
from subscribers.views import subsciber_new
from marketing.views import HomePage

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'crmapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^signup/$',subsciber_new,name='sub_new'),
    url(r'^$',HomePage.as_view(),name="home"),
    (r'^login/$',
    'django.contrib.auth.views.login', {'template_name': 'login.html'}
    ),
    (r'^logout/$',
        'django.contrib.auth.views.logout', {'next_page': '/login/'}
    ),
)
