from django.conf.urls.defaults import *
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from designs.forms import FileForm, StyleForm, InfoForm
from designs.views import upload_wizard, FORMS

urlpatterns = patterns('designs.views',
	url(r'^upload$', upload_wizard.as_view(FORMS)),
	#url(r'^upload$', 'coming_soon_upload', name='coming_soon_upload'),
	url(r'^(?P<designurl>\w+)/$', 'design', name='design'),
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)