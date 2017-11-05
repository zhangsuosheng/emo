from django.http import HttpResponse
import json

from app_user.models import Friends,User

def onefriend(request):
    if request.method == 'POST':
    # if True:
        friendid=request.POST.get('id')
        userid=1
        # friendid=1
        friend=Friends.objects.get(friend_id=friendid)
        response = {'status': '1', 'data':{"friend_id":friend.friend_id,"realname":friend.realname,"nickname":friend.nickname,
                     "relation":friend.relation,"development":friend.development,
                     "record":friend.record,"couple":friend.couple,"phone":friend.phone,
                     "email": friend.email, "birthplace": friend.birthplace,
                     "company": friend.company, "position": friend.position,
                     "politic": friend.politic, "skill": friend.skill,
                     "interest": friend.interest, "remark": friend.remark,"face": friend.face,

                     "intimacy": friend.intimacy,"sex": friend.sex, "birthday": str(friend.birthday.year)+str(friend.birthday.month)+str(friend.birthday.day),
                     "age": friend.age, "marriage": friend.marriage,
                     "qualification": friend.qualification, "salary": friend.salary
                     }}
        return HttpResponse(json.dumps(response),content_type="application/json")
    return HttpResponse(u'请使用POST访问该接口')

def friendlist(request):
    userid = 1
    user = Friends.objects.filter(usrid=userid)
    list = []
    for elem in user:
        print(elem.birthday)
        list.append({"realname": elem.realname,"id": elem.friend_id,"intimacy": elem.intimacy})
    response = {'status': '1', 'data': list}
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")
