from django.shortcuts import render
from designs.models import Design
from cmsplugin_blog.models import EntryTitle
from oscar.apps.catalogue.models import Product
from random import shuffle
from datetime import datetime, timedelta
from pytz import timezone
import collections
import re
from itertools import chain

def index(request):
	#TODO: currently hardcoded to show latest shop product, needs fixing
	last_week = Design.objects.filter(name__exact='Trophy Skull').order_by('created').reverse()[:1]

	#different hardcode for dev page
	if not last_week:
		last_week = Design.objects.filter(name__exact='Grizzly Bear').order_by('created').reverse()[:1]	

	#query designs to show in news center
	latest = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14)).order_by('created').reverse()[0]
	in_store = Design.objects.order_by('product').exclude(product__exact=None)
	blogpost = EntryTitle.objects.all().order_by('entry')[0]

	if not blogpost.entry.is_published:
		blogpost = EntryTitle.objects.all().order_by('entry')[1]

	#extract blogpost image
	blogextract = blogpost.entry.placeholders.filter(slot='excerpt')[0].get_plugins()[0].get_plugin_instance()[0].content
	pat = re.compile (r'<img [^>]*src="([^"]+)')
	blogimg = pat.findall(blogextract)[0]

	return render(request, 'garmsby_home.html', {
		'last_week': last_week[0], 
		'blogpost':blogpost,
		'latest' : latest,
		'blogimg':blogimg,
		'in_store':in_store[0],
		})