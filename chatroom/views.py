from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

class UsernameForm(forms.Form):
    username = forms.CharField(
        label='Enter Your Username',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )



def home(request):
    if request.method == 'POST':
        room_name = request.POST.get('roomName')
        if room_name:
            return HttpResponseRedirect(reverse('chat_room',args=[room_name]))

    return render(request, 'index.html', {})


def chat_room(request, room_name):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            return render(request, 'chatroom.html', {'room_name': room_name, 'username': username})
    else:
        form = UsernameForm()

    return render(request, 'username.html', {'form': form, 'room_name': room_name})
