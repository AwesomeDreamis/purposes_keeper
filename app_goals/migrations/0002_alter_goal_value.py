# Generated by Django 4.0.4 on 2022-09-05 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='value',
            field=models.IntegerField(verbose_name='value'),
        ),
    ]
