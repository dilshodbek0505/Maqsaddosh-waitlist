from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models

from apps.user.models import User
from apps.main.models import Like, Feedback


@receiver(post_save, sender=Feedback)
def increment_feedback_count(sender, instance, created, **kwargs):
    if created:
        User.objects.filter(pk=instance.user_id).update(
            feedbacks_count=models.F("feedbacks_count") + 1
        )

@receiver(post_delete, sender=Feedback)
def decrement_feedback_count(sender, instance, **kwagrs):
    User.objects.filter(pk=instance.user_id).update(
        feedbacks_count=models.F("feedbacks_count") - 1
    )

@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    if created and instance.feedback_id and instance.is_active:
        feedback_owner = instance.feedback.user
        User.objects.filter(pk=feedback_owner.pk).update(
            likes_count=models.F("likes_count") + 1
        )
    
    if not created and instance.feedback_id and not instance.is_active:
        print("feedback_update")
        feedback_owner = instance.feedback.user
        User.objects.filter(pk=feedback_owner.pk).update(
            likes_count=models.F("likes_count") - 1
        )
        

@receiver(post_delete, sender=Like)
def decrement_likes_count(sender, instance, **kwargs):
    if instance.feedback_id:
        feedback_owner = instance.feedback.user
        User.objects.filter(pk=feedback_owner.pk).update(
            likes_count=models.F("likes_count") - 1
        )