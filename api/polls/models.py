from django.db.models import *
from django.utils import timezone
import datetime


class Question(Model):
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    question_text = CharField(max_length=200)
    pub_date = DateTimeField('date published')


class Choice(Model):
    def __str__(self):
        return self.choice_text
    question = ForeignKey(Question, on_delete=CASCADE)
    choice_text = CharField(max_length=200)
    votes = IntegerField(default=0)
