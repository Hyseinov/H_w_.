from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from .models import Post, Comment, PostLike


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "id created_date title text comments count is_like like_count".split()

    def get_comments(self, instance):
        comments = Comment.objects.filter(post_id=instance)
        return CommentListSerializer(comments, many=True).data

    def get_count(self, instance):
        return Comment.objects.filter(post=instance).count()

    def get_is_like(self, instance):
        if PostLike.objects.filter(post=instance,
                                   user=self.context['request'].user).count():
            return True
        return False

    def get_like_count(self, instance):
        return PostLike.objects.filter(post=instance).count()


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


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10000)
    password = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=100)

    def validate(self, object):
        if User.objects.filter(username=object["username"]).count() > 0:
            raise ValidationError("Такой пользоватль уже есть!")
        else:
            if object["password"] != object["password1"]:
                raise ValidationError("Пороли не совпадают!")
        return object




