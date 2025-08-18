from rest_framework import serializers

from apps.main.models import Like, Feedback, Comment, Post
from apps.user.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)

    class Meta:
        model = Feedback
        fields = (
            "id",
            "user",
            "text",
            "likes_count",
            "is_liked",
        )
        read_only_fields = ("user",)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer()
        return super().to_representation(instance)


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Post
        fields = (
            "uuid",
            "title",
            "cover_image",
            "file",
            "body",
            "content_type",
            "likes_count",
            "is_liked",
        )
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "post",
            "feedback",
            "comment",
            "is_active",
        )
        read_only_fields = ("is_active",)

    
    def create(self, validated_data):
        user = self.context['request'].user

        like, created = Like.objects.get_or_create(
            user=user,
            post=validated_data.get("post"),
            feedback=validated_data.get("feedback"),
            comment=validated_data.get("comment"),
            defaults={"is_active": True}
        )
        if not created:
            like.is_active = not like.is_active
            like.save()
        
        return like

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = "liked" if instance.is_active else "unliked"
        return data

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "user",
            "text",
        )
        read_only_fields = ("user", )
        write_only_fields = ("post",)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer()
        return super().to_representation(instance)