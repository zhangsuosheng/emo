from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import json
import datetime

from app_user.models import User,Friends,Remind
from django.contrib.auth.decorators import login_required

#主页
@login_required
def index(request):
    userid=1
    user = Friends.objects.filter(usrid=userid)
    tags = []
    for elem in user:
        if elem.tag is None:
            pass
        else:
            for elem2 in elem.tag.split(","):
                tags.append(elem2)
    print(tags)
    tags = list(set(tags))
    print(tags)

    return render(request,"index.html",locals())
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