from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json

from app_user.models import User, Friends, Remind
from django.contrib.auth.decorators import login_required

###################
from django.conf import settings
import datetime


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
        return HttpResponse('elastic search 服务器查询出错，请联系管理员')
    hits = result['hits']['hits']

    all_data = {}
    for elem_dict in hits:
        all_data[elem_dict['_id']] = elem_dict['_source']
    # print(hits)  # 所有可用数据
    # print("#########################################")
    # print(all_data)  # 要返回的数据
    return render(request, "index.html",
                  {'all_data': all_data, 'username': username, 'KEY_OF_FRIEND_NAME': settings.KEY_OF_FRIEND_NAME})


@login_required
def new_friends(request):
    if request.method == 'POST':
        username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)

        query_dict = {}
        num_text = eval(request.POST['num_text'])
        for i in range(0, num_text):
            key = request.POST['texttitle' + str(i)]
            value = request.POST['textcontent' + str(i)]
            query_dict[key] = value

        num_num = eval(request.POST['num_num'])
        for i in range(0, num_num):
            key = request.POST['numtitle' + str(i)]
            value = eval(request.POST['numcontent' + str(i)])
            query_dict[key] = value

        num_date = eval(request.POST['num_date'])
        for i in range(0, num_date):
            key = request.POST['datetitle' + str(i)]
            value = datetime.datetime.strptime(request.POST['datecontent' + str(i)], "%Y-%m-%d")
            query_dict[key] = value

        num_tag = eval(request.POST['num_tag'])
        query_dict["标签"] = []
        for i in range(0, num_tag):
            query_dict["标签"].append(request.POST['tag' + str(i)])
        query_dict[settings.KEY_OF_FRIEND_NAME] = request.POST.get(settings.KEY_OF_FRIEND_NAME)
        try:
            settings.ELASTIC_OPTER.insert_friend_docu(username, [query_dict])
        except Exception as e:
            print(e)
            return HttpResponse('elastic search服务出错，请联系管理员')
        return HttpResponseRedirect('/')


@login_required
def search_by_tag(request):
    if request.method == "POST":
        username = request.get_signed_cookie('username', salt=settings.COOKIE_SALT)
        fuzzy=request.POST.get('fuzzy')
        print(fuzzy)
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
        print(result)
        result_id=[]
        result_score=[]
        for elem in result['hits']['hits']:
            result_id.append([elem['_id'],elem['_score']])
            # result_score.append(elem['_id'])
        return HttpResponse(json.dumps({'fuzzy':fuzzy,'result_id':result_id}))
        # return HttpResponse(json.dumps(result_id))#json.dumps可以发送list格式的数据！
    return HttpResponse


# event页
def event(request):
    userid = 1
    user = Remind.objects.filter(usrid_id=userid)
    return render(request, "event.html", locals())


# 给app返回当前事件列表
def remind(request):
    userid = 1
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
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")


# 返回所有好友所有信息
def friend(request):
    userid = 1
    user = Friends.objects.filter(usrid=userid)
    list = []
    for elem in user:
        print(elem.birthday)
        list.append({"friend_id": elem.friend_id, "realname": elem.realname, "nickname": elem.nickname,
                     "relation": elem.relation, "development": elem.development,
                     "record": elem.record, "couple": elem.couple, "phone": elem.phone,
                     "email": elem.email, "birthplace": elem.birthplace,
                     "company": elem.company, "position": elem.position,
                     "politic": elem.politic, "skill": elem.skill,
                     "interest": elem.interest, "remark": elem.remark, "face": elem.face,

                     "intimacy": elem.intimacy, "sex": elem.sex,
                     "birthday": str(elem.birthday.year) + str(elem.birthday.month) + str(elem.birthday.day),
                     "age": elem.age, "marriage": elem.marriage,
                     "qualification": elem.qualification, "salary": elem.salary
                     })
    response = {'status': '1', 'data': list}
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")
