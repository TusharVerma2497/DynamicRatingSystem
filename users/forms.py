from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from users.models import profile
from PIL import Image
import os

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField()
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField(required=False)
    last_name=forms.CharField(required=False)
    class Meta:
        model=User
        fields=['first_name','last_name','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=profile
        fields=['gender','image','phone']