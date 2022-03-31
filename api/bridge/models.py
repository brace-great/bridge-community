
from datetime import date
from django.db import models
import django.utils.timezone as timezone


class Notify(models.Model):
    username = models.CharField(max_length=100)
    text = models.TextField()
    isread = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)


# class Chat(models.Model):
#     from_who = models.CharField(max_length=100)
#     to_who = models.CharField(max_length=100)

#     class Meta:
#         unique_together = (("from_who", "to_who"))
class ChatMessage(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    isshow_sender = models.BooleanField(default=1)
    isshow_receiver = models.BooleanField(default=1)
    isread_receiver = models.BooleanField(default=0)


class UserInfo(models.Model):
    birthday = models.DateField()
    avatar = models.TextField(null=True)
    introduce = models.TextField(null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()

    class Meta:
        ordering = ['birthday']


# Create your models here.
