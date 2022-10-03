from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    return f'profile_images/{instance.user.id}/{filename}'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    profile_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default='profile_images/defaultuser.png', verbose_name=_('image'))
    profile_head_img = models.ImageField(upload_to=user_directory_path, null=True, blank=True, default='profile_images/defaulthead.png', verbose_name=_('head image'))
    is_active = models.BooleanField(null=True, default=False, verbose_name=_('active'))
    goals_count = models.IntegerField(default=0, verbose_name=_('goals_count'))

    friends = models.ManyToManyField(User, related_name='friends', blank=True, verbose_name=_('friends'))

    class Meta:
        verbose_name_plural = _('profiles')
        verbose_name = _('profile')

    def __str__(self) -> str:
        """
        Возвращает имя пользователя (владельца профиля)
        :return: Имя пользователя
        :rtype: str
        """
        return self.user.username

    def increment_goals_count(self):
        """
        Увеличивает количество новостей пользователя на 1"""
        self.goals_count += 1
        self.save()

    def friends_count(self) -> int:
        """
        Возвращает количество друзей
        :return: количество подписчиков
        :rtype: int
        """
        return self.friends.all().count()


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)

