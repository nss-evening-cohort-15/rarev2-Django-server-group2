"""View module for handling requests about posts"""
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models.category import Category
from rareapi.models import Post
from rareapi.models import RareUser


class PostView(ViewSet):
    """One Post"""

    def create(self, request):
        """Handle POST operations for posts

        Returns:
            Response -- JSON serialized post instance
        """
        author = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.author = author
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]

        category = Category.objects.get(pk=request.data["category_id"])
        post.category = category

        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        authorId = self.request.query_params.get('authorId', None)
        
        if authorId is not None:
            posts = posts.filter(author__id=authorId)
       
        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
    

    def update(self, request, pk=None):
        """Handle PUT requests for a game
        Returns:
            Response -- Empty body with 204 status code
        """
        author = RareUser.objects.get(user=request.auth.user)

        category = Category.objects.get(pk=request.data["category_id"])

        post = Post.objects.get(pk=pk)        
        post.author = author
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.category = category

        post.save()
        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(methods=['get'], detail=False, permission_classes=[IsAdminUser])
    def unapproved(self, request):
        try:
            unapprovedPosts = Post.objects.filter(approved=False)
            serializer = PostSerializer(unapprovedPosts, many=True, context={'request': request})
            return Response(serializer.data)   
        
        except Exception as ex:
                return Response({'message': ex.args[0]}) 
            
            
    @action(methods=['put'], detail=True, permission_classes=[IsAdminUser])        
    def approve(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        post.approved = True
        post.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)   
            
    
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializers
    """
    class Meta:
        model = Post
        fields = ('id', 'author', 'category', 'title', 
                  'publication_date', 'image_url', 'content', 'approved')
        depth = 3