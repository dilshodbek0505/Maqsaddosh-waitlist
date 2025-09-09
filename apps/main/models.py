from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    class PostContentType(models.TextChoices):
        IMAGE = ("image", "Image")
        VIDEO = ("video", "Video")

    uuid = models.UUIDField(unique=True, default=uuid4, primary_key=True)
    title = models.CharField(max_length=128)
    cover_image = models.ImageField(upload_to="cover_images/", blank=True, null=True)
    file = models.FileField(upload_to="files/", blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    body = models.TextField()
    content_type = models.CharField(max_length=20, choices=PostContentType.choices)
    
    def __str__(self):
        return self.title

class Feedback(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


class Comment(BaseModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.post.title

class Like(BaseModel):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             blank=True, null=True,)
    feedback = models.ForeignKey(Feedback,
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE,
                                blank=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    is_active = models.BooleanField(default=True)

    