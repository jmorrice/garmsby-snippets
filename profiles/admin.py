from django.contrib import admin
from profiles.models import UserProfile

def delete_model(modeladmin, request, queryset):
	for obj in queryset:
		obj.delete()

class UserProfileAdmin(admin.ModelAdmin):
	exclude = ()
	list_display = ('user','location','joined','avatar', 'email_confirmed', 'size')

admin.site.register(UserProfile, UserProfileAdmin)