# Generated by Django 4.0.4 on 2022-09-05 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_users', '0003_remove_profile_is_banned_profile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friend_offer',
            field=models.ManyToManyField(blank=True, related_name='friend_offer', to=settings.AUTH_USER_MODEL, verbose_name='friend_offer'),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
