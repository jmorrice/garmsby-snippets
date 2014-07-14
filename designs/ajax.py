from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from designs.models import Design, Like, ReadyNotification
from django.contrib.auth import login, authenticate, logout
from requests import get
from social_auth.models import UserSocialAuth
from urllib import quote
from json import loads
from django.core.mail import send_mail
from designs.models import Design
from datetime import datetime
from pytz import timezone

def update_likes(design):
	design.likes = Like.objects.filter(design=design).count()
	design.save()

@dajaxice_register
def toggle_like(request, design_url):
	dajax = Dajax()
	user = request.user
	design = Design.objects.get(url=design_url)
	if not user.is_authenticated():
		dajax.script('please_login(".%s_container");' % design.url)
	elif not user.profile.email_confirmed:
		dajax.script('confirm_email(".%s_container");' % design.url)
	else:
		new_like = Like.objects.filter(user=user, design=design)
		#unlike
		if new_like: #list not empty -> already liked 
			new_like.delete()
			update_likes(design=design)
			dajax.script('show_unlike();')

		else:
			new_like = Like(user=user, design=design)
			new_like.save()
			update_likes(design=design)
			dajax.script('show_like();')

	return dajax.json()

@dajaxice_register
def notify(request, design_name):
	dajax = Dajax()
	user = request.user
	design = Design.objects.get(name=design_name)
	notification = ReadyNotification(user=user, design=design)
	notification.save()
	dajax.assign('#notify_me', 'innerHTML', "<p class='apple_medium'>we'll let you know when it's in store!</p>")

	#add mailchimp stuff
	return dajax.json()

@dajaxice_register
def fb_like(request, design_url):
	dajax = Dajax()
	user = request.user
	design = Design.objects.get(url=design_url)
	#get fb token for like activity
	try:
		instance = UserSocialAuth.objects.filter(provider='facebook').get(user=user.id)
		access_token = instance.tokens['access_token']
	except:
		pass
	else:
		fb_string = quote('https://garmsby.co.uk/designs/'+design.url+'/', '')
		response = get('https://graph.facebook.com/me/og.likes?access_token='+access_token+'&method=POST&object=' + fb_string)
		print fb_string
		print 'https://graph.facebook.com/me/og.likes?access_token='+access_token+'&method=POST&object=' + fb_string
		print response.text

	return dajax.json()

@dajaxice_register
def fb_share(request, design_name):
	dajax = Dajax()
	user = request.user
	if user.is_authenticated():
		design = Design.objects.get(name=design_name)
		#get fb token for like activity
		try:
			instance = UserSocialAuth.objects.filter(provider='facebook').get(user=user.id)
			access_token = instance.tokens['access_token']
		except:
			dajax.script('fb_share_popup();')
		else:
			fb_string = quote('https://garmsby.co.uk/designs/'+design.url+'/', '')
			response = get('https://graph.facebook.com/me/garmsby:share?access_token='+access_token+'&method=POST&design='+fb_string+'&fb:explicitly_shared=true')
			print response.text

			try:
				#check for auth exception
				is_autherror = (json.loads(response.content)['error']['type'] == 'OAuthException')
			except:
				is_autherror = False

			if is_autherror or response.status_code != 200:
				print 'caught auth error and showing poopup'
				dajax.script('fb_share_popup();')
	else:
		dajax.script('fb_share_popup();')

	return dajax.json()

@dajaxice_register
def resubmit(request, design_url):
	dajax = Dajax()
	user = request.user
	design = Design.objects.get(url=design_url)

	if design.designer == user:
		new_design = Design()
		new_design.designer = design.designer
		new_design.name = design.name
		new_design.story = design.story
		new_design.price = design.price
		new_design.garment = design.garment
		new_design.tee_colour = design.tee_colour
		new_design.preview_colour = design.preview_colour
		new_design.design_pic = design.design_pic
		new_design.tee_pic = design.tee_pic
		new_design.url = design.url
		new_design.user_agreement_accepted = design.user_agreement_accepted
		new_design.created = datetime.now(timezone('Europe/London'))

		new_design.resubmitted = True
		previous_likes = design.likes
		new_design.save()

		design.delete()

		#send email notification
		msg = 'Design resubmission by ' + new_design.designer.first_name + ' ' + new_design.designer.last_name + '\n\nPrevious Likes: ' + str(previous_likes) + '\n\nInitially submitted: ' + str(new_design.created) + '\n\nLink: https://garmsby.co.uk/admin/designs/design/' + str(new_design.id)
		send_mail('Design Resubmission', msg, 'garmsby<accounts@garmsby.co.uk>', ['accounts@garmsby.co.uk'], fail_silently=False)
		
	return dajax.json()