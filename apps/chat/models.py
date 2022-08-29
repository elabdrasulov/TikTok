from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True)

    def get_members_count(self):
        return self.members.count()

    def join(self, user):
        self.members.add(user)
        self.save()

    def leave(self, user):
        self.members.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} -> members: {self.get_members_count()} - id:{self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='from_message', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='to_message', on_delete=models.CASCADE)
    message = models.TextField()
    # date = models.DateTimeField(default=datetime.now)
    date = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'From {self.sender} to {self.receiver} ({self.message})'
    


