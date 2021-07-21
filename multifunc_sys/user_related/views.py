from django.shortcuts import render
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser

# Create your views here.
# 自定义user类的manage
class userManage(BaseUserManager):
    # 自定义创建用户规则
    def _create_user(self, username, password, **kwargs):
        # 这里可以自定义一些字段限制，比如用户名限制，密码规则限制等
        if not username:
            raise ValueError("用户名不能为空")
        if not password:
            raise ValueError("密码不能为空")
        user = self.model(username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    # 创建普通用户
    def create_user(self,username, password, **kwargs):
        kwargs["is_superuser"] = False
        return self._create_user(username, password, **kwargs)

    # 创建超级管理员
    def create_super_user(self,username, password, **kwargs):
        kwargs["is_superuser"] = True
        kwargs["is_staff"] = True
        return self._create_user(username, password, **kwargs)


# 重写django自带user类
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=50,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=255,default="12345678.",verbose_name="密码")
    telnumber = models.CharField(max_length=22,verbose_name="电话号",null=True,blank=True)
    is_staff = models.BooleanField(default=True, verbose_name="是否是员工")
    user_create_time = models.DateTimeField(auto_now_add=True,verbose_name="用户创建时间")
    user_session_key = models.CharField(max_length=100,verbose_name="session_key")
    email = models.EmailField(null=True,blank=True,verbose_name="邮箱")
    tel_code = models.CharField(max_length=20,verbose_name="电话验证码",null=True,blank=True)
    tel_code_time = models.DateTimeField(auto_now=True,verbose_name="电话验证码入库时间")
    email_code = models.CharField(max_length=20,verbose_name="邮箱验证码",null=True,blank=True)
    email_code_time = models.DateTimeField(auto_now=True,verbose_name="邮箱验证码入库时间",blank=True,null=True)
    is_ban = models.BooleanField(default=False,verbose_name="是否封禁")
    de_active_time = models.DateTimeField(null=True, blank=True, verbose_name="禁用截止时间")
    de_active_reason = models.CharField(null=True, blank=True, max_length=100,verbose_name="禁用用户原因")

    USERNAME_FIELD = 'username'

    class Mete:
        db_table = "tiktokuser"

    objects = userManage()

    def __str__(self):
        return self.username

