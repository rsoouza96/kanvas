from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    user_set = models.ManyToManyField(User, related_name="course")


class Activity(models.Model):
    repo = models.CharField(max_length=255)
    grade = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)