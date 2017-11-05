import json

from django.http import HttpResponse

#定义中间件，接收上一层中间件发来的请求并调用下一层的中间件
def decode_post_body(get_response):
    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.method == "POST":
            try:
                request.POST = json.loads(request.body.decode('UTF-8'))
            except Exception:
                return HttpResponse("", status=500)
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware