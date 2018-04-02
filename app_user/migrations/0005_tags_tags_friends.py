# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 05:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_user', '0004_friends_faceuid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('tag_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('tag_text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tags_Friends',
            fields=[
                ('tag_friend_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('friend_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.Friends')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.Tags')),
            ],
        ),
    ]
