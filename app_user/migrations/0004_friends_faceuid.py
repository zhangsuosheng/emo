# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-04 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0003_friends_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='faceuid',
            field=models.CharField(default='无', max_length=100),
        ),
    ]
