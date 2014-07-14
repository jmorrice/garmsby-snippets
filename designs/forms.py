from django.forms import ModelForm
from designs.models import Design
from django.core.exceptions import ValidationError
from PIL import Image
import urllib, cStringIO
import re

class UploadForm(ModelForm):
	class Meta:
		model = Design
		exclude = ('designer', 'likes')

class AgreementForm(ModelForm):
	class Meta:
		model = Design
		fields = ('user_agreement_accepted', )

	def clean_user_agreement_accepted(self):
		val = self.cleaned_data['user_agreement_accepted']
		if not val:
			raise ValidationError("You must agree to our user agreement to continue")
		return val

class FileForm(ModelForm):
	class Meta:
		model = Design
		fields = ('design_pic', 'tee_pic')

	def clean_design_pic(self):
		img_url = self.cleaned_data['design_pic']

		#load image
		file = cStringIO.StringIO(urllib.urlopen(img_url).read())

		#check file is a valid image
		try:
			img = Image.open(file)
		except:
			raise ValidationError("Please upload a valid image file")

		#check image is square and has the required min. resolution
		width, height = img.size[0], img.size[1]
		if width != height:
			raise ValidationError("Please upload a square image (see specs)")

		if width > 2000:
			raise ValidationError("Please upload an image with a lower resolution (see specs)")

		return img_url

	def clean_tee_pic(self):
		img_url = self.cleaned_data['tee_pic']

		#load image
		file = cStringIO.StringIO(urllib.urlopen(img_url).read())

		#check file is a valid image
		try:
			img = Image.open(file)
		except:
			raise ValidationError("Please upload a valid image file")

		#check image is square and has the required min. resolution
		width, height = img.size[0], img.size[1]
		if width != height:
			raise ValidationError("Please upload a square image (see specs)")

		if width > 2000:
			raise ValidationError("Please upload an image with a lower resolution (see specs)")

		return img_url

class StyleForm(ModelForm):
	class Meta:
		model = Design
		fields = ('tee_colour', 'preview_colour', 'price', 'garment')

	def clean_price(self):
		price = self.cleaned_data['price']

		#validate price is an integer and in range
		if re.match('^[\d]+$', str(price)) is None:
			raise ValidationError("The price must be a number")
		if price < 15 or price > 1000:
			raise ValidationError("Please enter a price between 15 and 1000 GBP")
		return price

class InfoForm(ModelForm):
	class Meta:
		model = Design
		fields = ('name', 'story')

	def clean_name(self):
		name = self.cleaned_data['name']

		#check name for special characters
		for c in name:
			if not (c.isalnum() or c.isspace()):
				raise ValidationError("Design titles can't contain any special characters (e.g. * - !)")

		#check if name already used
		try:
			design = Design.objects.get(name=name)
			raise ValidationError("A design with that name already exists!")
		except Design.DoesNotExist:
			pass
			
		return name