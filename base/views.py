from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User UserForm
# Create your views here.


# rooms = [
#     {'id' : 1, 'name' : 'Lets learn python!!'},
#     {'id' : 2, 'name' : 'Lets learn design!!'},
#     {'id' : 3, 'name' : 'Lets learn Frontend!!'},
#     {'id' : 4, 'name' : 'Lets learn Backend!!'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        # Once u are logged in.. U don't have to go to login page
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
    #   username = request.POST.['username'].lower() Official doc
        password = request.POST.get('password')
    #.  password = request.POST.['password'] # official doc

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "hmmm User does not exist")

        user = authenticate(request, username=username, password=password)
        # above code is same with official doc... 
        # using Django auth !!! 

        if user is not None:
            login(request, user) # user is okay then login
            return redirect('home') # and then go to the main page
        else: # Something went wrong!!
            messages.error(request, 'Username Or Password does not exist')
    context = {
        'page': page
    }

    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request) # really simple logout !
    return redirect('home')


def registerPage(request):
    #page = 'register'

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # all lower cases!
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Error occured during registration")
    context = {

    }
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    # ?q=python
    q = request.GET('q') if request.GET.get('q') != None else ''
    # q = query result from HTTP GET Protocol

    # icontains??
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages': room_messages,

    }

    return render(request, 'base/home.html', context)
    # It means base/templates/base/home.html


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all() # All the participants in that room
    # returns all related messages
    # room.message_set.all()
    # room has no attribute of message. so we need to use
    # room.message_set.all() to find it all!

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,  # above there
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }

    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.object.get(id=pk)
    rooms = user.room_set.all()  # all rooms that current user is in...
    room_messages = user.message_set.all()  # All messages this user has
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics,

    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topics.objects.all()
    if request.method == "POST":
        # print(request.POST)
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST)
        Room.obejcts.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user # Remember we fixed the forms.py?
        #     room.save() # host is autimatically be the host
        return redirect('home')  # we have namespace so just say it's home

    context = {
        'form': form,
        'topics' : topics,

    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):  # primary key
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("U R NOT ALLOWED HERE")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.name = request.POST.get('description')
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')

    context = {
        'form': form,
        'topics' : topics,

        }

    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("U R NOT ALLOWED HERE")

    if request.method == "POST":
        room.delete()  # simply remove it
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("U R NOT ALLOWED HERE")

    if request.method == "POST":
        message.delete()  # simply remove it
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})



@login_required(login_url='login')
def updateUser(request):
    user = reuqest.user
    form = UserForm(instance = user)

    if request.method == "POST":
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {
        'form' : form
    }

    return render(request, 'base/update-user.html', context)