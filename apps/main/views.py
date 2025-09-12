from django.db.models import Count, Q, Exists, OuterRef, Sum

from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.main.models import Post, Like, Comment, Feedback
from apps.main.serializers import FeedbackSerializer, PostSerializer \
                                    ,CommentSerializer, LikeSerializer, LiderBoardSerializer


class FeedbackView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user if self.request and self.request.user.is_authenticated else None
        
        qs = super().get_queryset()
        qs = qs.annotate(
            likes_count=Count('like', filter=Q(like__is_active=True))
            )

        if user:
            qs = qs.annotate(
                is_liked=Exists(
                    Like.objects.filter(
                        feedback=OuterRef('pk'),
                        user=user,
                        is_active=True
                    )
                )
            )
        else:
            qs = qs.annotate(is_liked=Exists(Like.objects.none()))
        
        qs = qs.order_by('-created_at')
        return qs

class PostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user if self.request.user and self.request.user.is_active else None

        qs = super().get_queryset()
        qs = qs.annotate(likes_count=Count('like', filter=Q(like__is_active=True)))
        
        if user:
            qs = qs.annotate(
                is_liked=Exists(
                    Like.objects.filter(
                        post=OuterRef('pk'),
                        user=user,
                        is_active=True
                    )
                )
            )
        else:
            qs = qs.annotate(is_liked=Exists(Like.objects.none()))

        qs = qs.order_by('-created_at')
        return qs

class LikeView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    
class CommentView(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user if self.request.user and self.request.user.is_active else None

        qs = super().get_queryset()
        qs = qs.annotate(likes_count=Count('like', filter=Q(like__is_active=True)))
        
        if user:
            qs = qs.annotate(
                is_liked=Exists(
                    Like.objects.filter(
                        comment=OuterRef('pk'),
                        user=user,
                        is_active=True
                    )
                )
            )
        else:
            qs = qs.annotate(is_liked=Exists(Like.objects.none()))
        
        
        post_id = self.request.query_params.get('post')
        if post_id:
            qs = qs.filter(post__uuid=post_id)
        
        qs = qs.order_by('-created_at')
        return qs
    
class LiderBoardView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LiderBoardSerializer

    def get_queryset(self):
        from apps.user.models import User

        qs = User.objects.filter(is_staff=False, is_superuser=False)
        qs = qs.annotate(
            likes_count=Count(
                "feedback__like",
                filter=Q(feedback__like__is_active=True),
                distinct=True
            ),
            feedbacks_count=Count(
                "feedback",
                distinct=True
            )
        )

        qs = qs.order_by("-likes_count", "-feedbacks_count", "created_at")
        return qs
        