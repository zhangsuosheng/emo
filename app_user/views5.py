from django.http import HttpResponse
import json

from app_user.models import Friends,Remind

#根据faceuid查询好友
def getbyface(request):
    if request.method == "POST":
        userid = 1
        faceid=request.POST.get('faceuid')
        print(faceid)
        friends=Friends.objects.filter(faceuid=faceid,usrid_id=userid)
        if len(friends)==0:
            response={'state':'0'}
        else:
            response={'state':'1','friend_id':friends[0].friend_id,'friend_name':friends[0].realname,'friend_intimacy':friends[0].intimacy}
        print(response)
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        return HttpResponse(u'请使用POST访问该接口')

#根据性别查询好友
def getbysex(request):
    if request.method == 'POST':
        sex=request.POST.get('sex')

    else:
        return HttpResponse(u'请使用POST调用该接口')

def addremind(request):
    if request.method =="POST":

        name=request.POST.get('eventName')
        time=request.POST.get('eventTime')
        content=request.POST.get('eventContent')
        Remind.objects.create(time=time,content=content)
    else:
        return HttpResponse(u'请使用POST方法访问该接口')