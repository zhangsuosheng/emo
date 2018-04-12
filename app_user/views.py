from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json

from app_user.models import User, Friends, Remind
from django.contrib.auth.decorators import login_required

###################
from django.conf import settings
from task1 import sendEmail
import datetime
import time

from django.core.urlresolvers import reverse

# 主页

@login_required
def index(request):
    username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)  # 仅使用了加盐的cookie来保持登陆
    query_dict = {
        'query': {
            'match_all': {},
        },
        'size': 100,
    }
    try:
        result = settings.ELASTIC_OPTER.query_friend_docu(username, query_dict)
    except Exception as e:
        print(e)
        return HttpResponse(settings.ELASTIC_ERROR_MESSAGE)
    hits = result['hits']['hits']

    all_data = {}
    for elem_dict in hits:
        all_data[elem_dict['_id']] = elem_dict['_source']
    # print(hits)  # 所有可用数据
    # print("#########################################")
    # print(all_data)  # 要返回的数据
    return render(request, "index.html",
                  {'all_data': all_data, 'username': username, 'KEY_OF_FRIEND_NAME': settings.KEY_OF_FRIEND_NAME,'ELASTIC_ERROR_MESSAGE':settings.ELASTIC_ERROR_MESSAGE})


@login_required
def new_friends(request):
    if request.method == 'POST':
        username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)

        query_dict = {}
        # {"usage": "features_type", "message": {}}
        type_dict={"doc":{"message":{}}}
        num_text = eval(request.POST['num_text'])

        for i in range(0, num_text):
            key = request.POST['texttitle' + str(i)]
            value = request.POST['textcontent' + str(i)]
            query_dict[key] = value
            type_dict['doc']['message'][key]='text'


        num_num = eval(request.POST['num_num'])
        for i in range(0, num_num):
            key = request.POST['numtitle' + str(i)]
            value = eval(request.POST['numcontent' + str(i)])
            query_dict[key] = value
            type_dict['doc']['message'][key]='num'

        num_date = eval(request.POST['num_date'])
        for i in range(0, num_date):
            key = request.POST['datetitle' + str(i)]
            value = datetime.datetime.strptime(request.POST['datecontent' + str(i)], "%Y-%m-%d")
            query_dict[key] = value
            type_dict['doc']['message'][key]='date'

        num_tag = eval(request.POST['num_tag'])
        query_dict["标签"] = []
        for i in range(0, num_tag):
            query_dict["标签"].append(request.POST['tag' + str(i)])

        query_dict[settings.KEY_OF_FRIEND_NAME] = request.POST.get(settings.KEY_OF_FRIEND_NAME)

        try:
            # 更新features类型信息文件
            settings.ELASTIC_OPTER.query_update(username=username,query_dict=type_dict,doc_type=settings.MESSAGE_TYPE_NAME,id=settings.FEATURES_TYPE_MESSAGE_ID)
            # 把新建的好友添加为friens type中的一个document
            settings.ELASTIC_OPTER.insert_friend_docu(username, [query_dict])
        except Exception as e:
            print(e)
            return HttpResponse(settings.ELASTIC_ERROR_MESSAGE)

        return HttpResponseRedirect(reverse('waiting'))


@login_required
def search_by_tag(request):
    if request.method == "POST":
        username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)
        fuzzy=request.POST.get('fuzzy')
        if fuzzy=="true":
            fuzzy=True
            query_str = {
                "query": {
                    "match": {
                        "标签": request.POST.get('keyword'),
                    }
                }
            }
        else:
            fuzzy=False
            query_str = {
                "query": {
                    "match_phrase": {
                        "标签": request.POST.get('keyword'),
                    }
                }
            }
        result = settings.ELASTIC_OPTER.query_friend_docu(username, query_str)
        result_id=[]
        for elem in result['hits']['hits']:
            result_id.append([elem['_id'],elem['_score']])
        return HttpResponse(json.dumps({'fuzzy':fuzzy,'result_id':result_id}))
    return HttpResponse

@login_required
def search_by_feature_text(request):
    username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)
    featurename = request.POST.get('featurevalue')
    keyword = request.POST.get('keyword')
    query_str = {
        "query": {
            "match_phrase": {
                featurename: keyword,
            }
        }
    }
    result = settings.ELASTIC_OPTER.query_friend_docu(username, query_str)
    result_id = []
    for elem in result['hits']['hits']:
        result_id.append(elem['_id'])
    return HttpResponse(json.dumps(result_id))

@login_required
def search_by_feature_num_or_date(request):
    username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)
    featurename = request.POST.get('featurevalue')
    top = request.POST.get('top')
    bottom=request.POST.get('bottom')
    query_str = {
        "query": {
            "range": {
                featurename:{
                    "gte":bottom,
                    "lte":top,
                }
            }
        }
    }
    result = settings.ELASTIC_OPTER.query_friend_docu(username, query_str)
    result_id=[]
    for elem in result['hits']['hits']:
        result_id.append(elem['_id'])
    return HttpResponse(json.dumps(result_id))


@login_required
def get_types(request):
    username=request.get_signed_cookie('username',salt=settings.COOKIE_SALT)
    # 获取features类型信息文件
    result=settings.ELASTIC_OPTER.query_by_id(username=username,doc_type=settings.MESSAGE_TYPE_NAME,id=settings.FEATURES_TYPE_MESSAGE_ID)
    data=result['_source']['message']
    return HttpResponse(json.dumps(data))

@login_required
def send_email(request):
    if request.method=="POST":
        username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)
        ids=request.POST.get('ids').split(',')
        if ids==['']:
            return HttpResponse('并没有要发送邮件的好友。。')
        title=request.POST.get('title')
        content=request.POST.get('content')
        time_send_str=request.POST.get('date')
        print(request.POST)

        try:
            time_send=datetime.datetime.strptime(time_send_str,'%Y-%m-%dT%H:%M')
            time_now = datetime.datetime.now()
            second_now = time.mktime(time_now.timetuple())
            second_send = time.mktime(time_send.timetuple())
            second_delay = second_send - second_now
            if second_delay < 0:
                return HttpResponse('发送日期已过')
        except ValueError as e:
            print(e)
            return HttpResponse('输入日期格式错误，请重新输入')

        message_list = []
        for id in ids:
            result = settings.ELASTIC_OPTER.query_by_id(username, doc_type=settings.FRIENDS_TYPE_NAME, id=id)
            name_friend=result['_source'][settings.KEY_OF_FRIEND_NAME]
            title_friend=title.replace('【'+settings.KEY_OF_FRIEND_NAME+'】',name_friend)
            content_friend=content.replace('【'+settings.KEY_OF_FRIEND_NAME+'】',name_friend)
            if '邮箱' in result['_source']:
                email_friend=result['_source']['邮箱']
                message={"email":email_friend,"title":title_friend,"content":content_friend,"id":id,"name":name_friend}
                message_list.append(message)

        print(message_list)

        try:
            for message in message_list:
                # (receivers, title, content, second_delay)
                sendEmail.delay(receivers=[message['email']], title=message['title'], content=message['content'],second_delay=second_delay)
        except Exception as e:
            print(e)
            return HttpResponse('redis/celery服务出错，请联系管理员')

        responsestr='发送任务已加入消息队列，将要给以下用户发送邮件：<br>'
        responsestr+="发送时间："+str(time_send)+"<br><br>"
        for message in message_list:
            responsestr+=message['name']+"："+message['email']+"<br>标题："+message['title']+"<br>内容："+message['content']+"<br><br>"

        return HttpResponse(responsestr)

@login_required
def delete_friends(request):
    if request.method=="POST":
        username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)
        friend_id = request.POST.get('friend_id')
        try:
            result=settings.ELASTIC_OPTER.delete_by_id(username=username,doc_type=settings.FRIENDS_TYPE_NAME,id=friend_id)
            print(result)
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status':0}))
        return HttpResponse(json.dumps({'status':1}))









# event页
def event(request):
    username=request.get_signed_cookie('username',salt=settings.COOKIE_SALT)
    return render(request, "event.html", locals())


# 给app返回当前事件列表
def remind(request):
    username=request.get_signed_cookie('username',salt=settings.COOKIE_SALT)
    user = Remind.objects.filter(usrid=userid)
    list = []
    for elem in user:
        year = str(elem.time.year)
        month = str(elem.time.month)
        day = str(elem.time.day)
        hour = str(elem.time.hour)
        minute = str(elem.time.minute)
        friend = Friends.objects.get(friend_id=elem.friend_id_id)
        list.append({'event_id': elem.id, 'friend_id': friend.friend_id, 'friend_name': friend.realname,
                     'content': elem.content, 'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute})
    response = {'status': '1', 'data': list}
    return HttpResponse(json.dumps(response), content_type="application/json")

