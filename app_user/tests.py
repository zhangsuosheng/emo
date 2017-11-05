from django.test import TestCase
from django.http import HttpResponse
import json

# django 与 vue 测试类
def test1(request):
    # 后端接收前端json请求
    name=request.POST.get('name')
    password=request.POST.get('password')
    print(name)
    print(password)



    #前端给后端发送json结果
    response={'status':'1','data':{'out':'数据来了'}}
    return HttpResponse(json.dumps(response),content_type="application/json")
# , header = {
#         'Access-Control-Allow-Origin': '*'
#     }