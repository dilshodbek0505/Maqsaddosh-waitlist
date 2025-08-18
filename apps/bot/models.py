from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

from apps.main.models import BaseModel

User = get_user_model()


class SmsPenndingBot(BaseModel):
    uuid = models.UUIDField(unique=True)
    code = models.CharField(max_length=4, blank=True, null=True)
    phone = models.CharField(max_length=20)
    
    class Meta:
        ordering = ['-created_at']