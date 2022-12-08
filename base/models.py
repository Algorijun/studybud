from django.db import models
from django.contrib.auth import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Room(models.Model): # inherit from django 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.charField(max_length=200)
    description = models.TextField(null=True , blank=True) # When form submit happens, It can be blank
    # participants = 
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True) # 
    # Diff between auto_now and auto_now_add
    # auto_now makes snapshot on every time we hit the save
    # auto_now_add only only add a time stamp??

    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return str(self.name) 

class Message(models.Model):
    # Django already has great user model for us..
    # for me like a noob!
    user = models.Foreignkey(User, on_delete=models.CASCADE)
    room = models.Foreignkey(Room, on_delete=models.CASCADE) # If parents instance is deleted, then this one also
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True) # 

    def __str__(self):
        return self.body[0:50] 

