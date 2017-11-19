from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from subscribers.views import subsciber_new
from marketing.views import HomePage
from accounts.views import AccountList, AccountDetail, account_cru
from contacts.views import ContactDetail, ContactCru, ContactDelete
from communications.views import comm_detail, comm_cru, CommDelete
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
    url(r'^account/new/$', account_cru, name="account_new"),
    url(r'^account/list/$', AccountList.as_view(), name="account_list"),
    url(r'^account/(?P<uuid>[\w-]+)/$', login_required(AccountDetail.as_view()), name="account_detail" ),
    url(r'^account/(?P<uuid>[\w-]+)/edit/$', account_cru, name="account_update" ),
    url(r'^contact/(?P<pk>[\w-]+)/delete/$',ContactDelete.as_view(), name='contact_delete'),
    url(r'^contact/edit/(?P<uuid>[\w-]+)/', login_required(ContactCru.as_view()), name='contact_update'),
    url(r'^contact/new/$', login_required(ContactCru.as_view()), name='contact_new'),
    url(r'^contact/(?P<uuid>[\w-]+)/', login_required(ContactDetail.as_view()), name='contact_detail'),
    url(r'^comm/(?P<pk>[\w-]+)/delete/$',CommDelete.as_view(), name='comm_delete'),
    url(r'^comm/(?P<uuid>[\w-]+)/', comm_detail, name='comm_detail'),
    url(r'^comm/new/$',comm_cru, name='comm_new'),
    url(r'^edit/(?P<uuid>[\w-]+)/$',comm_cru, name='comm_update'),

)
