from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Project
from django.db import models
from pyuploadcare.dj.forms import ImageField

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UploadForm(forms.ModelForm):
    # image = ImageField(label='image')
    class Meta:
        model = Project
        fields = ('title', 'description', 'image', 'url')

class UploadProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic', 'bio', 'location')

# class RatingsForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = ['design', 'usability', 'content']