from django.http import HttpResponse
import json

from app_user.models import Friends

#新增某一个好友的某一条信息
def new_friend(request):
    if request.method=='POST':
    # if True:
        userid=1
        name=request.POST.get('name')
        common=request.POST.get('intimacy')
        # name = "zhangsuosheng"
        # common = 100
        if request.POST.get('faceuid') is None:
            newfriend = Friends.objects.create(realname=name, usrid_id=userid, intimacy=common)
        else:
            print(request.POST.get('faceuid'))
            newfriend=Friends.objects.create(realname=name,usrid_id=userid,intimacy=common,faceuid=request.POST.get('faceuid'))
        response = {'state': '1', 'friend_id': newfriend.friend_id}
        print(response)
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse(u'请使用POST访问该接口')

#修改某一个好友的某一条信息
def modify_friend(request):
    if request.method=='POST':
    # if True:
        userid=1
        friendid=request.POST.get('friend_id')
        edit_message=request.POST.get('edit_message')#获取要修改的变量的名字
        value= request.POST.get(edit_message)
        # friendid='1'
        # edit_message='realname'
        # value='e瞳网'
        try:
            friend=Friends.objects.get(friend_id=friendid)
        except Friends.DoesNotExist:
            response={'state':'0'}
            return HttpResponse()
        if friend.usrid_id==userid:
            # 使用setattr修改属性值，适用于要用变量的值来代表要修改的属性名时
            friend.__setattr__(edit_message,value)
            friend.save()
            response={'state':'1'}
            return HttpResponse(json.dumps(response),content_type="application/json")
        else:
            response={'state':'0'}
            return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        return HttpResponse(u'请使用POST方法访问该接口')