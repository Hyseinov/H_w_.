from rest_framework.decorators import api_view
# Create your views here.
from app1.models import Post, Comment
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from app1.serializers import PostListSerializer, CommentListSerializer


@api_view(['GET'])
def post_list_views(request):
    posts = Post.objects.all()
    data = PostListSerializer(posts, many=True).data
    return Response(data={'list': data})


@api_view(['GET'])
def post_item_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound('Ни-фи-га')
    data = PostListSerializer(post, many=False).data
    return Response(data=data)


@api_view(['GET'])
def comment_list_view(request):
    comment = Comment.objects.all()
    data = CommentListSerializer(comment, many=True).data
    return Response(data={'list': data})


@api_view(['GET'])
def comment_item_view(request, id):
    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        raise NotFound('Ни-фи-га')
    data = CommentListSerializer(comment, many=False).data
    return Response(data=data)
