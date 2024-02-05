from django.contrib.auth.models import User
from django.db import models


class Question(models.Model):
    step = models.PositiveSmallIntegerField(default=0)
    question = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
