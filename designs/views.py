from django.http import HttpResponseRedirect
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from designs.models import Design
from designs.forms import UploadForm, AgreementForm, FileForm, StyleForm, InfoForm
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render_to_response
from designs.models import Design, Like, ReadyNotification
from storages.backends.s3boto import S3BotoStorage
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from datetime import datetime, timedelta
from pytz import timezone
from django.http import Http404
from itertools import chain
from social_auth.models import UserSocialAuth
from oscar.apps.catalogue.models import Product
from random import shuffle
import collections

FORMS = [("agreement", AgreementForm),
		 ("files", FileForm),
         ("style", StyleForm),
         ("info", InfoForm)]

TEMPLATES = {"agreement": "upload_0.html",
			 "files": "upload_1.html",
             "style": "upload_2.html",
             "info": "upload_3.html"}

class upload_wizard(SessionWizardView):
	def get_template_names(self):
		return [TEMPLATES[self.steps.current]]

	def get_context_data(self, form, **kwargs):
		context = super(upload_wizard, self).get_context_data(form=form, **kwargs)
		data = self.get_all_cleaned_data()
		if self.steps.current == 'style':
			context.update({'design_pic': data['design_pic'] , 'tee_pic': data['tee_pic']})
		return context

	def done(self, form_list, **kwargs):
		design = Design()
		for form in form_list:
			for field, value in form.cleaned_data.iteritems():
				setattr(design, field, value)
		design.designer = self.request.user
		design.url = design.name.replace(" ", "_")
		design.save()
		msg = 'New design by ' + design.designer.first_name + ' ' + design.designer.last_name + '\n\nLink: ' + 'https://garmsby.co.uk/admin/designs/design/' + str(design.id)
		send_mail('New Design Submission', msg, 'garmsby<accounts@garmsby.co.uk>', ['accounts@garmsby.co.uk'], fail_silently=False)

		subject = "your design's live!"
		d = Context({
			'SUBJECT' : subject,
			'FNAME' : design.designer.first_name,
			'CURRENT_YEAR' : datetime.now(timezone('Europe/London')).year,
			'UNSUB' : 'http://garmsby.us7.list-manage2.com/unsubscribe?u=becdeb23c196dfccca38ec1bd&id=ed61191f4e&e=&c=4f56a5e378',
			})

		text_content = get_template('email/upload_confirm.txt').render(d)
		html_content = get_template('email/upload_confirm.html').render(d)
		from_email, to = 'garmsby<accounts@garmsby.co.uk>', design.designer.email
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to, 'info@garmsby.co.uk'])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

		return HttpResponseRedirect('/designs/' + design.url)

def design(request, designurl):
	def hex_to_rgb(value):
			value = value.lstrip('#')
			lv = len(value)
			return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

	#query all designs from db
	all_designs = Design.objects.all()

	#check if design from url exists, else throw 404
	try:
		design = all_designs.get(url=designurl)
	except Design.DoesNotExist:
		raise Http404

	#get rank of design
	full_voting_query = all_designs.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14)).order_by('created').reverse()
	next_design = None
	previous_design = None
	
	if design.in_voting():
		full_voting_list = list(full_voting_query)
		index = full_voting_list.index(design)
		if index > 0:
			previous_design = full_voting_list[index - 1]
		if index < len(full_voting_list) - 1:
			next_design = full_voting_list[index + 1] # an extra -1 to convert to 0-based index

	#check if already liked
	user = request.user
	liked = None
	if user.is_authenticated():
		liked = Like.objects.filter(user=user, design=design)

	#get other design by artist
	design_list = all_designs.filter(designer=design.designer.id).exclude(name=design.name)

	#determine text colour for comments (e.g. to avoid black on black)
	rgb = hex_to_rgb(design.preview_colour)
	brightness = rgb[0] * .299 + rgb[1] * .587 + rgb[2] * .114
	if brightness < 130:
		colour = 'white'
	else:
		colour = 'black'

	#determine if user has already requesed a shop notification
	notified = False
	user = request.user
	if user.is_authenticated():
		if ReadyNotification.objects.filter(user=user, design=design).count() > 0:
			notified = True

	#get other designs in voting
	more_list = full_voting_query.order_by('likes').reverse().filter(~models.Q(designer=design.designer.id)).order_by('?')

	#get list of products for shop preview
	product_list = []
	for product in Product.objects.all():
		if product.title != '' and not any(x.title == product.title for x in product_list) and product.is_available_to_buy:
			product_list.append(product)
	shuffle(product_list)

	return render(request, 'design.html', {	'design' : design,
											'liked' : liked,
											'design_list' : design_list[:3],
											'previous_design':previous_design,
											'next_design':next_design,
											'colour' : colour,
											'notified':notified,
											'more_list':more_list[:4],
											'product_list':product_list[:4]})

def choose_summary(request):
	all_list = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14)) #db query
	popular_list = all_list.order_by('likes')[:4].reverse()
	ending_list = all_list.filter(created__lt=datetime.now(timezone('Europe/London')) - timedelta(days=11)).order_by('created')[:4]
	latest_list = all_list.order_by('created').reverse()[:4]

	return render(request, 'choose/choose-summary.html', {
		'popular_list' : popular_list,
		'ending_list' : ending_list,
		'latest_list' : latest_list
		})

def choose_popular(request):
	design_list = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14)).order_by('likes').reverse()[:12]
	return render(request, 'choose/choose-popular.html', {'design_list' : design_list, 'category':'popular' })

def choose_ending(request):
	design_list = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14)).filter(created__lt=datetime.now(timezone('Europe/London')) - timedelta(days=11)).order_by('created')[:12]
	return render(request, 'choose/choose-ending.html', {'design_list' : design_list, 'category':'ending' })

def choose_latest(request):
	design_list = Design.objects.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14)).order_by('created').reverse()[:4]
	return render(request, 'choose/choose-latest.html', {'design_list' : design_list, 'category':'latest' })

def choose_successful(request):
	store_list = Design.objects.exclude(product=None)
	production_list = Design.objects.filter(likes__gte=110).filter(product=None)
	
	return render(request, 'choose/choose-successful.html', {
		'production_list' : production_list,
		'store_list' : store_list,
		'category':'successful' })
