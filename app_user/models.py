from django.db import models
import datetime

#登陆信息表
class User(models.Model):
    usrid=models.AutoField(unique=True,primary_key=True)#用户id,自增
    usrname=models.CharField(max_length=50,unique=True)#用户名，非空
    usrpassword=models.CharField(max_length=50)#密码，非空
    usrphone=models.CharField(max_length=50)#手机，非空
    usremail=models.CharField(max_length=50)#邮箱，非空



# 好友信息表
class Friends(models.Model):
    # def __eq__(self, other):
    #     return self.friend_id==other.friend_id
    usrid=models.ForeignKey(User,to_field="usrid")#用户id，外键
    friend_id=models.AutoField(unique=True,primary_key=True)#好友id，自增
    realname=models.CharField(max_length=50)#姓名，非空
    nickname=models.CharField(max_length=50,default="无")#称呼
    relation=models.CharField(max_length=50,default="无")#关系
    development=models.CharField(max_length=500,default="无")#发展情况
    record=models.CharField(max_length=500,default="无")#来往记录
    couple=models.CharField(max_length=50,default="无")#配偶（对象）姓名
    phone=models.CharField(max_length=50,default="无")#手机
    email=models.CharField(max_length=50,default="无")#邮箱
    birthplace=models.CharField(max_length=50,default="无")#所在地
    company=models.CharField(max_length=50,default="无")#单位
    position=models.CharField(max_length=50,default="无")#职位
    politic=models.CharField(max_length=50,default="无")#政治面貌
    skill=models.CharField(max_length=50,default="无")#特长
    interest=models.CharField(max_length=50,default="无")#兴趣
    remark=models.CharField(max_length=500,default="无")#备注
    face=models.CharField(max_length=500,default="无")#人脸图片的绝对路径

    tag=models.CharField(max_length=2000,null=True)#标签，形式为“阳光，开朗，热情”


    faceuid=models.CharField(max_length=100,default="无")#faceuid，人脸识别所得该人的身份id

    intimacy=models.IntegerField()#亲密度，非空
    sex = models.IntegerField(default=1)# 性别,1为男，0为女
    birthday = models.DateTimeField(default=datetime.datetime(year=1990,month=1,day=1))# 生日
    age = models.IntegerField(default=0)# 年龄
    marriage = models.IntegerField(default=0)# 婚姻状况,1为已婚，0为未婚
    qualification=models.IntegerField(default=6)#学历，0为博士，1为硕士，2为本科，3为高中，4为初中，5为小学,6为其他
    salary=models.IntegerField(default=0)#年薪

#提醒表
class Remind(models.Model):
    usrid=models.ForeignKey(User,to_field="usrid")#用户id，外键
    friend_id=models.ForeignKey(Friends,to_field="friend_id")#好友id，外键
    content=models.CharField(max_length=500)#提醒内容，非空
    time=models.DateTimeField()#提醒时间，非空

# 标签表
class Tags(models.Model):
    tag_id=models.AutoField(unique=True,primary_key=True)#标签id，自增
    tag_text=models.CharField(max_length=100)#标签内容，不能为空

# 好友&标签关系表
class Tags_Friends(models.Model):
    tag_friend_id=models.AutoField(unique=True,primary_key=True)# 关系号，自增
    friend_id=models.ForeignKey(Friends,to_field="friend_id")# 好友id，外键
    tag_id=models.ForeignKey(Tags,to_field="tag_id")# 标签id，自增
