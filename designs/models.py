from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from datetime import datetime, timedelta
from oscar.apps.catalogue.models import Product
from pytz import timezone

def upload_to_design(instance, filename):
    return 'designs/%s/%s_design.png' % (instance.designer.username, instance.name)

def upload_to_tee(instance, filename):
    return 'designs/%s/%s_tee.png' % (instance.designer.username, instance.name)

class Design(models.Model):
	designer = models.ForeignKey(User, default=User.objects.get(username='admin').id)
	created = models.DateTimeField(auto_now=False, auto_now_add=True, default=datetime.now())

	#status
	likes = models.IntegerField(default=0)
	resubmitted = models.BooleanField(default=False)
	product = models.ForeignKey(Product, blank=True, null=True)
	
	#design details
	garment = models.CharField(max_length=50, default="garment_tshirt")
	tee_colour = models.CharField(max_length=50, default="colour_white")
	preview_colour = models.CharField(max_length=50, default="#ffffff")
	design_pic = models.URLField()
	tee_pic = models.URLField()
	price = models.IntegerField(default=15)
	name = models.CharField(max_length=50)
	url = models.CharField(max_length=50)
	story = models.TextField(max_length=250)

	#legal stuff
	user_agreement_version = models.CharField(max_length=10, default="v1.1")
	user_agreement_accepted = models.BooleanField(default=False)

	def delete(self):
		Like.objects.filter(design=self).delete()
		super(Design, self).delete()

	def in_voting(self):
		if self.created >= datetime.now(timezone('Europe/London')) - timedelta(days=14):
			return True
		else:
			return False

	def past_voting(self):
		if self.created < datetime.now(timezone('Europe/London')) - timedelta(days=14):
			return True
		else:
			return False

	def in_production(self):
		if self.likes >= 110 and self.product == None:
			return True
		else:
			return False

	def in_store(self):
		if self.product:
			return True
		else:
			return False

	def __unicode__(self):
		return self.name

class Like(models.Model):
	user = models.ForeignKey(User, default=1)
	design = models.ForeignKey(Design, default=None)
	created = models.DateTimeField(auto_now=True, default=datetime.now())

	def delete(self):
		self.design.likes -= 1
		self.design.save()
		super(Like, self).delete()

class ReadyNotification(models.Model):
	user = models.ForeignKey(User, default=1)
	design = models.ForeignKey(Design, default=None)

	def __unicode__(self):
		return self.user.first_name + ' - ' + self.design.name