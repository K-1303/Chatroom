from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    if request.method == 'POST':
        room_name = request.POST.get('roomName')
        if room_name:
            return HttpResponseRedirect(reverse('chat_room',args=[room_name]))

    return render(request, 'index.html', {})


def chat_room(request, room_name):
    return render(request, 'chatroom.html', {
        'room_name': room_name
    })
