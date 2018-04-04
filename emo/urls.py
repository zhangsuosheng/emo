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
from app_user import views,views2,views3,views4,views5,regist_login
from app_user import tests

urlpatterns = [
    url(r'^admin/', admin.site.urls,name="admin"),
    url(r'^test/$',tests.test1,name="test"),
    url(r'^accounts/login/$',regist_login.login_view,name="login"),
    url(r'^accounts/regist/',regist_login.regist_view,name="regist"),
    url(r'^accounts/logout/', regist_login.logout_view, name="logout"),
    url(r'^$',views.index,name="index"),
    url(r'^newfriends/$',views.new_friends,name="newfriends"),

    url(r'^event/$',views.event,name="event"),

    url(r'^remind/$',views.remind,name="remind"),
    url(r'^friend/$',views.friend,name="friend"),
    url(r'^onefriend/$',views2.onefriend,name="onefriend"),
    url(r'^friendlist/$',views2.friendlist,name="friendlist"),
    url(r'^alltags/$',views3.alltags,name="alltags"),
    url(r'^userhastag/$',views3.userhastag,name="userhastag"),
    url(r'^modify_friend/$',views4.modify_friend,name="modify_friend"),
    url(r'^new_friend/$',views4.new_friend,name="new_friend"),
    url(r'^getbyface/$',views5.getbyface,name="getbyface"),
    url(r'^userhastag2/(.+)/$', views3.userhastag2, name="userhastag2"),

]
