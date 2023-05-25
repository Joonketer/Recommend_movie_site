from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    # 팔로잉 기능
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers')
