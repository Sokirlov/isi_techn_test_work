from django.db import models
from django.contrib.auth.models import User, Group

class Thread(models.Model):
    name = models.CharField('Name of Thread', max_length=100, default='room')
    participants = models.ManyToManyField(User, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_set')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_set', blank=True)
    text = models.TextField('Message text')
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}'
