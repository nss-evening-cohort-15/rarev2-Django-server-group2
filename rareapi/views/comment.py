"""View module for handling requests about comments"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment, RareUser, Post
from django.core.exceptions import ValidationError


class CommentView(ViewSet):
    """One Comment"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        

    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments
        """
        comments = Comment.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    def create(self, request):
        """Handle POST operations for comments

        Returns:
            Response -- JSON serialized comment instance
        """
        author = RareUser.objects.get(user=request.auth.user)

        comment = Comment()
        comment.author = author
        comment.content = request.data["content"]
        # comment.created_on = request.data["created_on"]
        post = Post.objects.get(pk=request.data["postId"])
        # post = Post.objects.all().filter(id = request.data["postId"])
        # serializedPost = PostSerializer(
        #     post, many=False, context={'request': request})
        comment.post = post

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
        
    

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments

    Arguments:
        serializers
    """
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_on', 'post', 'author')
        depth = 3
        
        
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializers
    """
    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 
                  'publication_date', 'image_url', 'content', 'approved')
        # depth = 3