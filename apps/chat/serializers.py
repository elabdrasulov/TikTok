from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageSerializer(serializers.ModelSerializer):

    sender = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username', many=False
    )
    receiver = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username', many=False
    )
    class Meta:
        model = Message
        fields = [
            'id',
            'sender', 
            'receiver',
            'message', 
            'date',
            'is_readed',
        ]
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['chat_id'] = instance.chat.id
        return rep

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['messages'] = MessageSerializer(instance.messages.all(), many=True).data
        return rep