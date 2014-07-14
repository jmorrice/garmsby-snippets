from django.forms import ModelForm
from profiles.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from garmsby_app.forms import validate_email, validate_pw, validate_username

class EditProfileForm(ModelForm):
	about = forms.CharField(widget=forms.TextInput(attrs={'class' : 'box'}))
	location = forms.CharField(widget=forms.TextInput(attrs={'class' : 'box'}))
	avatar = forms.CharField(widget=forms.TextInput(attrs={'type' : 'hidden'}))

	class Meta:
		model = UserProfile
		fields = ('about', 'location', 'avatar')

class EditUserForm(ModelForm):
	username = forms.CharField(validators=[validate_username], widget=forms.TextInput(attrs={'class' : 'box'}))
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'box'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'box'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'box'}))

	#store request for user object
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EditUserForm, self).__init__(*args, **kwargs)

	def clean_email(self):
		email = self.cleaned_data.get('email').lower()
		if self.request.user.email != email:
			validate_email(email)
		return email

	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email')