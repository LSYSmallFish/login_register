from django.db import models


# Create your models here.
class User(models.Model):
    """用户模型类"""
    gender = (
        ('male', "男"),
        ('female', "女")
    )
    name = models.CharField(max_length=128, unique=True)  # 用户名
    password = models.CharField(max_length=256)  # 密码
    email = models.EmailField(unique=True)  # 邮箱
    sex = models.CharField(max_length=32, choices=gender, default="男")  # 性别
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirmed = models.BooleanField(default=False)  # 这是个布尔值，默认为False，也就是未进行邮件注册

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"


class ConfirmString(models.Model):
    """邮箱确认码模型类"""
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name + ": " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "邮箱确认码"
        verbose_name_plural = "邮箱确认码"
