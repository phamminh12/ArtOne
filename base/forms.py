from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Picture, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['genre', 'name', 'image', 'description']
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']