# Generated by Django 4.1.2 on 2023-03-18 06:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('seller', '0002_followingmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='follower',
            field=models.ManyToManyField(related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FollowingModel',
        ),
    ]
