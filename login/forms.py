from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={'placeholder': "Username", 'autofocus': ''}))
    password1 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'placeholder': "Password"}))
    password2 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "email"}))
    sex = forms.ChoiceField(choices=gender)
    captcha = CaptchaField(label='验证码')

