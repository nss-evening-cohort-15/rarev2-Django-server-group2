"""View module for handling requests about comments"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment


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
    

class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments

    Arguments:
        serializers
    """
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_on', 'post', 'author')