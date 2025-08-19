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

class TelegramUser(BaseModel):
    telegram_id = models.IntegerField()
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    username = models.CharField(max_length=128, blank=True, null=True, unique=True)

    def __str__(self):
        return self.first_name

class ForwardMessage(models.Model):
    user_id = models.BigIntegerField()
    user_message_id = models.BigIntegerField()
    group_message_id = models.BigIntegerField()
    group_id = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['group_message_id', 'group_id'])
        ]