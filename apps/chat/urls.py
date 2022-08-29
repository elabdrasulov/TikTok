from django.urls import path
from django.urls.conf import re_path
from .views import *

urlpatterns = [
    path('create/', CreateChatAPIView.as_view()),
    path('list/', ChatListAPIView.as_view()),
    path('list/<int:chat_id>/', ChatDetailAPIView.as_view()),
    path('delete/', ChatDeleteAPIView.as_view()),
    path('messages/create/<int:chat_id>/', CreateMessageAPIView.as_view()),
    path('messages/', MessageListAPIView.as_view()),
    path('messages/<int:pk>/', MessageDeleteAPIView.as_view()),
]
