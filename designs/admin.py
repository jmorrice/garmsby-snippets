from django.contrib import admin
from designs.models import Design, Like, ReadyNotification
from datetime import datetime, timedelta
from pytz import timezone

def delete_model(modeladmin, request, queryset):
	for obj in queryset:
		obj.delete()

def restart_voting(modeladmin, request, queryset):
	for obj in queryset:
		obj.created = datetime.now(timezone('Europe/London'))
		obj.save()

def remove_from_voting(modeladmin, request, queryset):
	for obj in queryset:
		obj.created = datetime.now(timezone('Europe/London')) - timedelta(days=15)
		obj.save()

def extend_voting_by_1_day(modeladmin, request, queryset):
	for obj in queryset:
		obj.created = obj.created + timedelta(days=1)
		obj.save()

def shorten_voting_by_1_day(modeladmin, request, queryset):
	for obj in queryset:
		obj.created = obj.created - timedelta(days=1)
		obj.save()

def extend_voting_by_7_days(modeladmin, request, queryset):
	for obj in queryset:
		obj.created = obj.created + timedelta(days=7)
		obj.save()

def shorten_voting_by_7_days(modeladmin, request, queryset):
	for obj in queryset:
		obj.created = obj.created - timedelta(days=7)
		obj.save()

class DesignAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('name','created','designer','likes', 'product')
    actions = [ delete_model, restart_voting, remove_from_voting, extend_voting_by_1_day, shorten_voting_by_1_day, extend_voting_by_7_days, shorten_voting_by_7_days ]

admin.site.register(Design, DesignAdmin)

class LikeAdmin(admin.ModelAdmin):
	def user_size(self, instance):
		return instance.user.profile.size
	exclude = ()
	list_display = ('user', 'user_size','created', 'design')
	list_filter = ('design',)
	actions = [ delete_model ]

admin.site.register(Like, LikeAdmin)

class NotifyAdmin(admin.ModelAdmin):
	exclude = ()
	list_display = ('user', 'design')

admin.site.register(ReadyNotification, NotifyAdmin)