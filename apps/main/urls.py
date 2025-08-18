from django.urls import path

from apps.main.views import FeedbackView, PostView, CommentView \
                            , LikeView


urlpatterns = [
    path("feedback/FeedbackList/", FeedbackView.as_view({"get": "list"}), name="feedback-list"),
    path("feedback/FeedbackCreate/", FeedbackView.as_view({"post": "create"}), name="feedback-create"),
    path("post/PostList/", PostView.as_view(), name="post-list"),
    path("comment/CommentList/", CommentView.as_view({"get": "list"}), name="comment-list"),
    path("comment/CommentCreate/", CommentView.as_view({"post": "create"}), name="comment-create"),
    path("like/LikeCreate/", LikeView.as_view(), name="like-create")
]
