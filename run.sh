#!/bin/sh

echo 'start els...'
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.161-0.b14.el7_4.x86_64
export ES_JAVA_OPTS='-Xms200m -Xmx200m'
nohup /home/emo/elasticsearch-5.5.1/bin/elasticsearch &>/home/emo/emo/log/els.log &

echo 'start redis...'
nohup redis-server &>/home/emo/emo/log/redis.log &

echo 'start celery...'
cd app_user/
nohup celery -A task1 worker -l info --concurrency=10 &>/home/emo/emo/log/celery.log &

echo 'start django...'
cd ..
export PYTHONPATH=/home/emo/emo/app_user/
nohup python3 manage.py runserver 0.0.0.0:8000 &>/home/emo/emo/log/django.log &


