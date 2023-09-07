from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    text = models.CharField(max_length=240)
    date = models.DateTimeField(auto_now=True)
    auther = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    objects = models.Manager()
    def __str__(self):
        return self.text
