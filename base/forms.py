from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # fields = '__all__'  # If we set it to all, It's easy to see it in web
        # but when we create the Room... I want the 'host' automatically be the logged in
        # user.. so we need to change the fields
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
