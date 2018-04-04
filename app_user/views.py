from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import json

from app_user.models import User,Friends,Remind
from django.contrib.auth.decorators import login_required

###################
from django.conf import  settings
#主页
@login_required
def index(request):
    # 仅使用了加盐的cookie来保持登陆
    username=request.get_signed_cookie('username',salt='abc')
    query_dict={
        'query':{
            'match_all':{}
        }
    }
    result=settings.ELASTIC_OPTER.query_friend_docu('haha',query_dict)

    friends=result['hits']['hits']

    tags=[]
    for elem_dict in friends:
        tag_dict=elem_dict['_source']
        # print(len(elem_dict))
        for key in tag_dict.keys():
            if key == "username":
                pass
            elif type(tag_dict[key]) is type('str'):
                tags.append(tag_dict[key])
            elif type(tag_dict[key]) is type(0):
                tags.append(key)
    tags=list(set(tags))

    # print(friends)
    # print(username)
    return render(request,"index.html",{'friends':friends,'username':username,'tags':tags})



#event页
def event(request):
    userid=1
    user=Remind.objects.filter(usrid_id=userid)
    return render(request,"event.html",locals())

#给app返回当前事件列表
def remind(request):
    userid=1
    user=Remind.objects.filter(usrid=userid)
    list=[]
    for elem in user:
        year=str(elem.time.year)
        month=str(elem.time.month)
        day=str(elem.time.day)
        hour=str(elem.time.hour)
        minute=str(elem.time.minute)
        friend = Friends.objects.get(friend_id=elem.friend_id_id)
        list.append({'event_id':elem.id,'friend_id':friend.friend_id,'friend_name':friend.realname,'content':elem.content,'year':year,'month':month,'day':day,'hour':hour,'minute':minute})
    response = {'status': '1', 'data':list}
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")

#返回所有好友所有信息
def friend(request):
    userid=1
    user=Friends.objects.filter(usrid=userid)
    list=[]
    for elem in user:
        print(elem.birthday)
        list.append({"friend_id":elem.friend_id,"realname":elem.realname,"nickname":elem.nickname,
                     "relation":elem.relation,"development":elem.development,
                     "record":elem.record,"couple":elem.couple,"phone":elem.phone,
                     "email": elem.email, "birthplace": elem.birthplace,
                     "company": elem.company, "position": elem.position,
                     "politic": elem.politic, "skill": elem.skill,
                     "interest": elem.interest, "remark": elem.remark,"face": elem.face,

                     "intimacy": elem.intimacy,"sex": elem.sex, "birthday": str(elem.birthday.year)+str(elem.birthday.month)+str(elem.birthday.day),
                     "age": elem.age, "marriage": elem.marriage,
                     "qualification": elem.qualification, "salary": elem.salary
                     })
    response = {'status': '1', 'data': list}
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")