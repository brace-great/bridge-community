
from datetime import date
from django.db import models
import django.utils.timezone as timezone


class Report(models.Model):
    username = models.CharField(max_length=100)
    reporter = models.CharField(max_length=100)
    content_type = models.CharField(max_length=100)
    content_id = models.IntegerField()
    content_text = models.TextField()
    reason = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class Notify(models.Model):
    username = models.CharField(max_length=100)
    from_who = models.CharField(max_length=100)
    event_type = models.IntegerField()
    isread = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    discuss_title = models.CharField(max_length=100, default='')


class Dynamic(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100)
    discuss = models.CharField(max_length=100)
    comment = models.IntegerField(null=True)


class Discuss(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    starter = models.CharField(max_length=100)
    isshow = models.BooleanField(default=1)
    title = models.CharField(max_length=100, unique=True)


class Comment(models.Model):
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    commenter = models.CharField(max_length=100)
    discuss = models.ForeignKey(
        Discuss, on_delete=models.CASCADE, related_name='comments')
    notshow = models.BooleanField(default=0)
    replyto = models.ForeignKey(
        'self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.commenter)


class DiscussTag(models.Model):
    discuss = models.ForeignKey(
        Discuss, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=100)

    def __str__(self):
        return '%s' % (self.tag)


class DiscussWithTag(models.Model):
    tag = models.CharField(max_length=100)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    starter = models.CharField(max_length=100)
    isshow = models.BooleanField(default=1)
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'discuss_with_tag'


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
