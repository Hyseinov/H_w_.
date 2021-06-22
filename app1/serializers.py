from rest_framework import serializers
from .models import Post, Comment


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "id created_date title text comments count".split()

    def get_comments(self, instance):
        comments = Comment.objects.filter(post_id=instance)
        return CommentListSerializer(comments, many=True).data

    def get_count(self, instance):
        return Comment.objects.filter(post=instance).count()

class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "id text".split()
