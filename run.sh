#!/bin/sh

#pip install scrapy
#pip install psycopg2
#pip install django

echo 'start redis...'
nohup redis-server &>redis.log

echo 'start celery...'
cd app_user
nohup celery -A task1 worker -l info &>celery.log

echo 'start django...'
cd ..
nohup python3 manage.py runserver 0.0.0.0:8000 &>django.log


wait
