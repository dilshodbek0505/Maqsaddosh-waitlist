from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.user.managers import CustomUserManager


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=20,
                             unique=True)
    image = models.ImageField(
        upload_to="profile_image/",
        blank=True, null=True,
    )
    region = models.CharField(max_length=128,
                              blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone

    class Meta:
        swappable = "AUTH_USER_MODEL"