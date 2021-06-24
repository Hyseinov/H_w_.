import self as self
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class PostsValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    text = serializers.CharField(min_length=5)

    def validate(self, object):
        object = object["title"]
        if Post.objects.filter(title=object).count() > 0:
            raise ValidationError("Такой пост уже есть!")
        else:
            return object


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "id text".split()


class CommentsValidateSerializer(serializers.Serializer):
    comment = serializers.CharField(min_length=2, max_length=100)

    def validated_comment(self, object):
        if Comment.objects.filter(name=object).count() > 0:
            raise ValidationError("Такой коммент уже есть!")
        else:
            return object