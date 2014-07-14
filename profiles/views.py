from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from designs.models import Design, Like
from profiles.forms import EditProfileForm, EditUserForm
from sorl.thumbnail import delete
from django_comments import Comment
from django.http import Http404
from datetime import datetime, timedelta
from pytz import timezone
from uuid import uuid4
from social_auth.utils import setting, module_member
from social_auth.models import UserSocialAuth
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from urllib2 import HTTPError
from mailsnake import MailSnake
from mailsnake.exceptions import *

def index(request):
	if request.user.is_authenticated():
		return redirect ('/profiles/' + request.user.username)
	else:
		return redirect ('/')

def profile(request, uname):
	try:
		user_profile = User.objects.get(username=uname)
	except User.DoesNotExist:
		raise Http404
	design_list = Design.objects.filter(designer=user_profile.id)
	current_list = design_list.filter(created__gt=datetime.now(timezone('Europe/London')) - timedelta(days=14))
	past_list = design_list.filter(created__lte=datetime.now(timezone('Europe/London')) - timedelta(days=14))
	likes = Like.objects.filter(user=user_profile.id).count()
	design_count = design_list.count()
	stats = []

	if design_count == 0: #customer stats
		stats.append(['designs', design_count])
		stats.append(['designs liked', likes])
		stats.append(['comments', Comment.objects.filter(user=user_profile.id).count()])
		stats.append(['date joined', user_profile.profile.joined.strftime("%d. %b").lstrip('0')])
	else:
		stats.append(['designs', design_count])
		likes_received = 0
		for design in design_list:
			likes_received += Like.objects.filter(design=design).count()
		stats.append(['designs in voting', current_list.count()])
		stats.append(['total likes received', likes_received])
		stats.append(['last design submitted', design_list.order_by('created').reverse()[0].created.strftime("%d %b.").lstrip('0')])

	return render(request, 'profile.html', {
		'user_profile' : user_profile, 
		'current_list' : current_list,
		'past_list':past_list, 
		'stats' : stats 
		})

def edit_profile(request):
	user = request.user
	email = user.email
	#after submission
	if request.method == 'POST':
		edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=user.profile)
		edit_user_form = EditUserForm(request.POST, request.FILES, instance=user, request=request)
		#success
		if edit_profile_form.is_valid() and edit_user_form.is_valid():
			ms = MailSnake('f92abfa01e0a9cecc885186de4e37106-us7')
			print user.email
			ms.listUpdateMember(id='ed61191f4e', email_address=email, merge_vars={
				'FNAME':edit_user_form.cleaned_data.get('first_name'),
				'LNAME':edit_user_form.cleaned_data.get('last_name'),
				'EMAIL':edit_user_form.cleaned_data.get('email'),
				})
			edit_profile_form.save()
			edit_user_form.save()
			return redirect('/profiles/' + user.username)
	#before submission 
	else:
		edit_profile_form = EditProfileForm(instance=user.profile)
		edit_user_form = EditUserForm(instance=user, request=request)

	user_profile = user
	return render(request, 'edit_profile.html', {'edit_profile_form': edit_profile_form, 'edit_user_form': edit_user_form, 'user_profile' : user_profile })

def _ignore_field(name, is_new=False):
    return name in ('username', 'id', 'pk') or \
           (not is_new and
                name in setting('SOCIAL_AUTH_PROTECTED_USER_FIELDS', []))

#function for social_auth pipeline
def update_user_details(backend, details, uid, response, user=None, is_new=False,
                        *args, **kwargs):
    if user is None:
        return

    changed = False  # flag to track changes

    for name, value in details.iteritems():
        # configured fields if user already existed
        if not _ignore_field(name, is_new):
            if value and value != getattr(user, name, None):
                setattr(user, name, value)
                changed = True

	user.profile.activate()
	user.profile.fb_pic(uid)
	user.save()

	#add to mailchimp list
	if user.first_name:
		try:
			ms = MailSnake('f92abfa01e0a9cecc885186de4e37106-us7')
			key = ''
			ms.listSubscribe( id = 'ed61191f4e', email_address = user.email, merge_vars = { 'FNAME': user.first_name, 'LNAME': user.last_name, 'EKEY': key }, double_optin = False, send_welcome = False )
		except:
			print "Facebook login error: Couldn't add user to MailChimp list"
		else:
			user.profile.send_welcome_email(activate=False)