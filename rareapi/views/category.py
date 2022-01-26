"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Category


class CategoryView(ViewSet):
    """Category types"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category
        """
        try:
            category_type = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        category_types = Category.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = CategorySerializer(
            category_types, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')