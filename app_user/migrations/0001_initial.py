# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-04 02:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('friend_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('realname', models.CharField(max_length=50)),
                ('nickname', models.CharField(default='无', max_length=50)),
                ('relation', models.CharField(default='无', max_length=50)),
                ('development', models.CharField(default='无', max_length=500)),
                ('record', models.CharField(default='无', max_length=500)),
                ('couple', models.CharField(default='无', max_length=50)),
                ('phone', models.CharField(default='无', max_length=50)),
                ('email', models.CharField(default='无', max_length=50)),
                ('birthplace', models.CharField(default='无', max_length=50)),
                ('company', models.CharField(default='无', max_length=50)),
                ('position', models.CharField(default='无', max_length=50)),
                ('politic', models.CharField(default='无', max_length=50)),
                ('skill', models.CharField(default='无', max_length=50)),
                ('interest', models.CharField(default='无', max_length=50)),
                ('remark', models.CharField(default='无', max_length=500)),
                ('face', models.CharField(default='无', max_length=500)),
                ('tag', models.CharField(max_length=2000, null=True)),
                ('faceuid', models.CharField(default='无', max_length=100)),
                ('intimacy', models.IntegerField()),
                ('sex', models.IntegerField(default=1)),
                ('birthday', models.DateTimeField(default=datetime.datetime(1990, 1, 1, 0, 0))),
                ('age', models.IntegerField(default=0)),
                ('marriage', models.IntegerField(default=0)),
                ('qualification', models.IntegerField(default=6)),
                ('salary', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Remind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('time', models.DateTimeField()),
                ('friend_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.Friends')),
            ],
        ),
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
        migrations.CreateModel(
            name='User',
            fields=[
                ('usrid', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('usrname', models.CharField(max_length=50, unique=True)),
                ('usrpassword', models.CharField(max_length=50)),
                ('usremail', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='remind',
            name='usrid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.User'),
        ),
        migrations.AddField(
            model_name='friends',
            name='usrid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_user.User'),
        ),
    ]
