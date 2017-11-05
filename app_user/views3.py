from django.http import HttpResponse
import json

from app_user.models import Friends,User

#所有标签（单个list去重）
def alltags(request):
    userid=1
    user=Friends.objects.filter(usrid=userid)
    tags=[]
    for elem in user:
        if elem.tag is None:
            pass
        else:
            for elem2 in elem.tag.split(","):
                tags.append(elem2)
    print(tags)
    tags=list(set(tags))
    print(tags)
    response={'state':'1','tag':tags}
    return HttpResponse(json.dumps(response),content_type="application/json")

#取不同标签用户的并集（多个list去重）
def userhastag(request):
    print("using userhastag...")
    if request.method == 'POST':
    # if True:
        userid=1
        tags=request.POST.get('tag_list')
        # tags=['middle','阳光']
        print(tags)
        result=[]
        #如果标签集合为空，则所有用户都返回
        if len(tags)==0:
            print("hello")
            allfriend = Friends.objects.filter(usrid_id=userid)
            for elem in allfriend:
                result.append({'id':elem.friend_id,'name':elem.realname,'intimacy':elem.intimacy})
            response={'state':'1','data':result}
            return HttpResponse(json.dumps(response),content_type="application/json")
        #如果标签信息不为空，则返回有这些标签的用户的并集
        friend_list=[]
        results=[]
        for elem in tags:
            friends_has_this_tag=Friends.objects.filter(tag__contains=elem,usrid_id=userid)
            for elem2 in friends_has_this_tag:
                friend_list.append(elem2)
        print(friend_list)
        friend_list=list(set(friend_list))#将查出来的friend数据条对象的数组去重（将这句注释掉可以查看效果）
        for elem in friend_list:
            results.append({'id':elem.friend_id,'name':elem.realname,'intimacy':elem.intimacy})
        response={'state':'1','data':results}
        print(response)
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        return HttpResponse(u'请用POST方法调用该接口')

#取不同标签用户的交集（多个list取在每个list中都有的元素）
# def userhastag(request):
#     if request.method == "POST":
#         userid=1
#         tags=request.POST.get('tag_list')
#         list=[]
#         result=[]
#         for elem in tags:
#             type(Friends.objects.filter(tag__contains=elem))
#             list.append(Friends.objects.filter(tag__contains=elem))
#         print(list)
#         if len(list) == 1:
#             for elem2 in list[0]:
#                 result.append({'id':elem2.})
#             print(list[0])
#             print(list[0][0])
#             response={'state':'1','data':list[0]}
#     else:
#         return HttpResponse(u'请使用POST调用该接口')

#取不同标签用户的并集（多个list去重）
def userhastag2(request,tags):
    userid = 1
    print(tags)
    result = []
    # 如果标签集合为空，则所有用户都返回
    if len(tags) == 0:
        print("hello")
        allfriend = Friends.objects.filter(usrid_id=userid)
        for elem in allfriend:
            result.append({'id': elem.friend_id, 'name': elem.realname, 'intimacy': elem.intimacy})
        response = {'state': '1', 'data': result}
        return HttpResponse(json.dumps(response), content_type="application/json")
    # 如果标签信息不为空，则返回有这些标签的用户的并集
    friend_list = []
    results = []
    for elem in tags:
        friends_has_this_tag = Friends.objects.filter(tag__contains=elem, usrid_id=userid)
        for elem2 in friends_has_this_tag:
            friend_list.append(elem2)
    print(friend_list)
    friend_list = list(set(friend_list))  # 将查出来的friend数据条对象的数组去重（将这句注释掉可以查看效果）
    for elem in friend_list:
        results.append({'id': elem.friend_id, 'name': elem.realname, 'intimacy': elem.intimacy})
    response = {'state': '1', 'data': results}
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")