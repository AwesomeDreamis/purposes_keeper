from django.contrib import admin
from .models import Profile, FriendRequest
from django.contrib.auth.models import User


# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'goals_count', 'is_active', 'profile_img',]
    list_filter = ['is_active', ]
    actions = ['mark_as_active', 'mark_as_not_active']


    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)

    def mark_as_not_active(self, request, queryset):
        queryset.update(is_active=False)

    mark_as_active.short_description = 'activate'
    mark_as_not_active.short_description = 'not activate'


@admin.register(FriendRequest)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'from_user', 'to_user']
