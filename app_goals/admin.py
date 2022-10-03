from django.contrib import admin
from .models import Goal, UserImpact, Operation


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', ]


@admin.register(UserImpact)
class UserImpactAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'user', 'impact', ]


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['id', 'goal', 'user', 'impact', 'created_at', ]

