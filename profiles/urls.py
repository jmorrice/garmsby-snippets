from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('profiles.views',
	url(r'^$', 'index', name='index'),
	url(r'^(?P<uname>\w+)/$', 'profile', name='profile'),
	url(r'^edit$', 'edit_profile', name='edit_profile')
)