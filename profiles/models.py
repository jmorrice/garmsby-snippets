from django.db import models
from sorl.thumbnail import ImageField
from cms.models.pluginmodel import CMSPlugin
from django.contrib.auth.models import User
from datetime import datetime
from uuid import uuid4
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from social_auth.models import UserSocialAuth

def make_uuid():
    return str(uuid4())

def upload_to(instance, filename):
    return 'avatars/%s/%s_avatar.png' % (instance.user.username, instance.user.username)

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	about = models.CharField(max_length=350, default="No description added yet.")
	location = models.CharField(max_length=100, default="Not specified")
	joined = models.DateField(auto_now=False, auto_now_add=True, default=datetime.now())
	avatar = models.URLField(default="https://s3-eu-west-1.amazonaws.com/garmsby/media/avatars/default_avatar.png")
	email_key = models.CharField(max_length=36, default=make_uuid)
	email_confirmed = models.BooleanField(default=False)
	tc_version = models.CharField(max_length=10, default="v1.0")
	tc_accepted = models.BooleanField(default=True)
	size = models.CharField(max_length=2, null=True)

	def send_welcome_email(self, activate=True):		
		user = self.user
		plaintext = get_template('welcome_email.txt')
		htmly     = get_template('welcome_email.html')

		#generate and store activation key
		self.email_key = make_uuid()
		self.save()
		link = 'https://garmsby.co.uk/activate/key/' + self.email_key

		d = Context({ 
			'SUBJECT' : 'welcome to garmsby',
			'FNAME' : user.first_name,
			'ACTIV' : activate,
			'ACTIV_LINK' : link,
			'CURRENT_YEAR' : datetime.now().year,
			'UNSUB' : 'http://garmsby.us7.list-manage2.com/unsubscribe?u=becdeb23c196dfccca38ec1bd&id=ed61191f4e&e=&c=4f56a5e378',
			})

		subject, from_email, to = 'welcome to garmsby', 'garmsby<accounts@garmsby.co.uk>', user.email
		text_content = plaintext.render(d)
		html_content = htmly.render(d)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

	def resend_activation_email(self):
		key = make_uuid()
		self.email_key = key
		self.save()
		user = self.user
		link = 'https://www.garmsby.co.uk/activate/key/' + key
		subject, from_email = 'Activate your garmsby account', 'accounts@garmsby.co.uk'
		to_email = user.email
		text_content = 'Hey ' + user.first_name + ',\r\nPlease activate your account by clicking on the following link: ' + link + '\r\n Thanks for joining us!'
		html_content = '<h1>Hey ' + user.first_name + ',</h1>Please activate your account by clicking on the following link: ' + link + '<br/><br/>Thanks for joining us!'
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

	def fb_pic(self, id):
		url = "https://graph.facebook.com/%s/picture?type=large" % id
		self.avatar = url
		self.save()

	def set_size(self, size):
		self.size = size
		self.save()

	def activate(self):
		self.email_confirmed = True
		self.save()

	def is_fb_user(self):
		user = self.user
		is_fb_user = False
		try:
			instance = UserSocialAuth.objects.filter(provider='facebook').get(user=user.id)
			is_fb_user = True
		except:
			pass
		return is_fb_user

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])