#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms


from django.contrib.auth.models import User #django自带注册
from django.contrib.auth import authenticate #django自带登陆
from django.contrib.auth import login #login向session中添加SESSION_KEY, 便于对用户进行跟踪
from django.contrib.auth import logout



# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=50)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='邮箱')

def regist_view(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']
            try:
                user = User.objects.create_user(username=username,password=password,email=email)
            except Exception:
                return HttpResponse('该账号已被注册')
            user.save()
            return HttpResponse('regist success!!!')
    else:
        userform = UserForm()
    return render_to_response('regist.html',{'userform':userform})

def login_view(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        del userform.fields['email']
        if userform.is_valid():
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('index.html', {'userform': userform})
                else:
                    return HttpResponse('您的账户已被冻结')
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
        else:
            return HttpResponse('表单输入不合法')
    else:
        help(UserForm)
        userform = UserForm()
        del userform.fields['email']
        return render_to_response('login.html',{'userform':userform})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')