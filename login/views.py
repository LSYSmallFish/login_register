from django.shortcuts import render
from django.shortcuts import redirect
from .models import User
from . import models
from . import forms
import hashlib
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.

def hash_code(s, salt='mysite'):
    """hash加密"""
    h = hashlib.sha3_256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_Confirm_String(user):
    """创建确认码对象"""
    now = datetime.datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email(email, code):
    subject = '来自无奇不有的注册确认邮件'
    text_content = '''感谢注册，如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能！'''
    html_content = '''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>点击确认</a>，\
                    这里是无奇不有的邮箱注册确认邮件</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                 '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def index(request):
    """主页视图"""
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'login/index.html')


def login(request):
    """登录视图Form"""
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '用户名或密码错误'
        if login_form.is_valid():  # 使用form自带验证
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户名不存在'
                return render(request, 'login/login.html', locals())
            if not user.has_confirmed:
                message = '用户未确认邮件'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                print(username, password)
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码错误'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    """注册视图"""
    request.session.flush()
    if request.method == 'POST':
        print(1)
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            if password1 != password2:
                message = '两次输入的密码不同'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '邮箱已被注册'
                    return render(request, 'login/register.html', locals())
                new_user = models.User()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                request.session['is_register'] = True
                code = make_Confirm_String(new_user)
                send_email(email, code)
                return redirect('/registerS/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    """登出视图"""
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect("/login/")


def registerS(request):
    """登出视图"""
    if not request.session.get('is_register', None):
        return redirect('/login/')
    return render(request, 'login/registerS.html')


def user_confirm(request):
    """邮箱确认视图"""
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
        print(confirm)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'login/confirm.html', locals())
