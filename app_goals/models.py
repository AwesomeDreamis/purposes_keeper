from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Goal(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('author'))
    title = models.CharField(max_length=30, verbose_name=_('title'))
    value = models.IntegerField(verbose_name=_('value'))
    deadline = models.DateField(default=date(2000, 1, 1))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    participants = models.ManyToManyField(User, related_name='participants', blank=True, verbose_name=_('participants'))
    is_done = models.BooleanField(null=True, default=False, verbose_name=_('done'))

    def __str__(self) -> str:
        return self.title


class UserImpact(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name=_('goal'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    impact = models.IntegerField(verbose_name=_('impact'))


class Operation(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name=_('goal'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    impact = models.IntegerField(verbose_name=_('impact'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

