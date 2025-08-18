from django.contrib import admin

from apps.main.models import Post, Feedback, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("uuid", "title", "content_type")
    list_display_links = ("uuid", "title")
    readonly_fields = ("uuid",)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text")
    list_display_links = ("id", "user")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post")
    list_display_links = ("id", "user")

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_active")
    list_display_links = ("id", "user")
