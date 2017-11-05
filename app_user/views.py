from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import json
import datetime

from app_user.models import User,Friends,Remind

# 登陆
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        try:
            user=User.objects.get(usrname=name)
            print(user.usrpassword)
            print(password)
            if user.usrpassword is password:
                print("good")
                response = {'status': '1', 'data': {'userid': user.usrid}}
                return HttpResponse(json.dumps(response),content_type="application/json")
            else:
                response = {'status': '0', 'data': {'error': '密码错误'}}
                return HttpResponse(json.dumps(response),content_type="application/json")
        except User.DoesNotExist:
            response = {'status': '0', 'data': {'error': '找不到用户名'}}
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse(u'请使用POST方法调用该接口')

#注册
def reg(request):
    if request.method=="POST":
        username=request.POST.get('name')
        userpassword=request.POST.get('password')
        userphone=request.POST.get('phone')
        useremail=request.POST.get('email')
        try:
            newuser=User.objects.create(usrname=username,usrpassword=userpassword,usrphone=userphone,usremail=useremail)
            response={'state':'1','user_id':newuser.usrid}
            return HttpResponse(json.dumps(response),content_type="application/json")
        except Exception:
            response={'state':'0'}
            return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        return HttpResponse(u'请使用POST调用该接口')

#主页
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