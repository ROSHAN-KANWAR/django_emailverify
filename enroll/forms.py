from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms
class profile_user(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','first_name','last_name']
class profile_admin(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name','last_name',]

class Profileimage(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_img']