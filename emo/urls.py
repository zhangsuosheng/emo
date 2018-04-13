"""emo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.contrib import auth

from app_user import views, regist_login
from app_user import tests

from django.conf import settings

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls, name="admin"),
    url(r'^accounts/login/$', regist_login.login_view, name="login"),
    url(r'^accounts/regist/$', regist_login.regist_view, name="regist"),
    url(r'^accounts/logout/$', regist_login.logout_view, name="logout"),

    url(r'^$', views.index, name="index"),
    url(r'^newfriends/$', views.new_friends, name="newfriends"),

    url(r'^deletefriends/$',views.delete_friends,name="deletefriends"),

    # 搜索
    url(r'^searchbytag/$', views.search_by_tag, name="searchbytag"),
    url(r'^searchbyfeature_text/$', views.search_by_feature_text, name="searchbyfeature_text"),
    url(r'^searchbyfeature_num_or_date/$', views.search_by_feature_num_or_date, name="searchbyfeature_num_or_date"),

    url(r'^gettypes/$', views.get_types, name="gettypes"),

    url(r'^sendemail/$',views.send_email,name="sendemail"),

    url(r'^waiting/$',TemplateView.as_view(template_name="waiting.html"),name="waiting"),


]
