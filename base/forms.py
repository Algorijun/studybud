from django.forms import ModelForm 
from .model import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields =  '__all__' #('')