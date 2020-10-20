from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

from .definitions import Gender
# Create your models here.


class User(AbstractUser):
    gender = models.PositiveSmallIntegerField(default=Gender.Unset.value[0])
    phone = models.CharField(max_length=15, unique=True, null=True, blank=False)
    birthday = models.DateField(null=True, auto_now=False)
    updated_time = models.DateTimeField(auto_now=True)
    introduction = models.TextField()


class Box(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}'s Box".format(self.owner.username)
