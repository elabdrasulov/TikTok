from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Message, Chat
from .permissions import *
from .serializers import ChatSerializer, MessageSerializer

User = get_user_model()

class CreateChatAPIView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self,request):
        sender = request.user

        try:
            receiver = User.objects.get(id=request.data.get('receiver'))
        except User.DoesNotExist:
            return Response(
                "Can't create chat. There are no users with this receiver id!", 
                400
            )
        
        name = f'{sender.username} -> {receiver.username}'

        if sender is not None and receiver is not None:
            chat = Chat.objects.create(name=name)
            chat.members.add(sender, receiver)
            serializer = ChatSerializer(chat)
            response = {
                'status': 'success',
                'message': f'Chat between {sender.username} and {receiver.username}',
                'data': serializer.data
            }
            return Response(response)
        else:
            return Response('Choose user_id to start messaging', 400)

class ChatListAPIView(ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAdminOrAuthor, ]

    def get(self, request):
        user = request.user
        chats = Chat.objects.all()
        user_chats = []
        chat_ids = []
        for chat in chats:
            if user in chat.members.all():
                chat_ids.append(chat.id)
        
        if user.is_authenticated:
            if user.is_staff and user.is_superuser:
                messages = Message.objects.all()
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data)
            else:
                for num in chat_ids:
                    messages = Message.objects.filter(chat_id=num)
                    serializer = MessageSerializer(messages, many=True)
                    user_chats.append(serializer.data)
                return Response(user_chats)

        elif not user.is_authenticated:
            return Response("Authentication credentials were not provided.", 400)

        return Response('You have not started to chat yet.')

class ChatDetailAPIView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAdminOrAuthor, ]

    def get(self, request, chat_id):
        user = request.user

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response('Chat with this id does not exist!', 400)

        messages = Message.objects.filter(chat_id=chat_id)

        users_ids = set()
        for user_ in chat.members.all():
            users_ids.add(user_.id)
        
        if user.is_authenticated:
            if user.is_staff and user.is_superuser:
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data)
            elif user.id in users_ids:
                for message in messages:
                    message.is_readed = True
                    message.save()
                serializer = MessageSerializer(messages, many=True)
                return Response(serializer.data)
            else:
                return Response('Access denied!', 400)
        else:
            return Response("Authentication credentials were not provided.", 400)


class ChatDeleteAPIView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAdminOrAuthor, ]

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response('Chat has been successfully deleted')


class CreateMessageAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, chat_id):
        sender = request.user

        try:
            receiver = User.objects.get(id=request.data.get('receiver'))
        except User.DoesNotExist:
            return Response('User with this id does not exist!', 400)

        message = request.POST.get("message")
        chat = Chat.objects.get(id=chat_id)
        users_ids = set()
        for user in chat.members.all():
            users_ids.add(user.id)
        # print(users_ids)
        
        
        if sender is not None and receiver is not None:
            if sender.id in users_ids and receiver.id in users_ids and len(users_ids) == 1:
                message = Message.objects.create(
                    sender=sender,
                    receiver=receiver, 
                    message=message,
                    chat_id=chat_id,
                )
                serializer = MessageSerializer(message)
                return Response(serializer.data)
            elif sender.id in users_ids and receiver.id in users_ids and len(users_ids) == 2:
                message = Message.objects.create(
                    sender=sender,
                    receiver=receiver, 
                    message=message,
                    chat_id=chat_id,
                )
                serializer = MessageSerializer(message)
                return Response(serializer.data)
            else:
                return Response('You are not allowed to enter this chat', 400)
        # else:
        #     return Response(
        #         """'Something went wrong, 
        #         please check your fields, they must not be empty and try again.
        #         """
        #     )
        
class MessageListAPIView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminUser, ]


class MessageDeleteAPIView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAdminUser, ]

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response('Message has been successfully deleted')




