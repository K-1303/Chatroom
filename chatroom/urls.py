from django.urls import path
from .views import home, chat_room

urlpatterns = [
    path('', home, name='home'),
    path('<str:room_name>/', chat_room, name='chat_room'),

]
