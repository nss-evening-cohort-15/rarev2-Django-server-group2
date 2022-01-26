"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser


class RareUserView(ViewSet):
    """One RareUser"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single rareuser

        Returns:
            Response -- JSON serialized rareuser
        """
        try:
            rareuser = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rareuser, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all rareusers

        Returns:
            Response -- JSON serialized list of rareusers
        """
        rareusers = RareUser.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = RareUserSerializer(
            rareusers, many=True, context={'request': request})
        return Response(serializer.data)
    

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for rareusers

    Arguments:
        serializers
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'created_on', 'active', 'profile_image_url')