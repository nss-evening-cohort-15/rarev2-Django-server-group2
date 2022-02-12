"""View module for handling requests about rareusers"""
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from rareapi.models import RareUser, rareuser


class RareUserView(ViewSet):
    """One RareUser"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single rareuser

        Returns:
            Response -- JSON serialized rareuser
        """
        try:
            rareuser = RareUser.objects.get(pk=pk)
            login_rareuser = RareUser.objects.get(user=request.auth.user)
            
            rareuser.subscribed = login_rareuser in rareuser.subscribe_by.all()
            
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

        # Note the additional `many=True` argument to the serializer. 
        # It's needed when you are serializing a list of objects instead of a single object.
        serializer = RareUserSerializer(
            rareusers, many=True, context={'request': request})
        return Response(serializer.data)
    
    
    # ⭕️⭕️⭕️ Custom Action for the specific url '/subscription'
    @action(methods=['post', 'delete'], detail=True)
    def subscription(self, request, pk=None): 
    
        login_rareuser = RareUser.objects.get(user=request.auth.user)
        rareuser = RareUser.objects.get(pk=pk)

        # A rareuser wants to subscribe to another rareuser
        if request.method == "POST":
            try:
                # Using the attendees field on the event makes it simple to add a gamer to the event
                # .add(gamer) will insert into the join table a new row the gamer_id and the event_id
                rareuser.subscribe_by.add(login_rareuser)
                
                return Response({'done': True}, status=status.HTTP_201_CREATED)
            
            except Exception as ex:
                return Response({'message': ex.args[0]})

        elif request.method == "DELETE":
            try:
                rareuser.subscribe_by.remove(login_rareuser)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            
            except Exception as ex:
                return Response({'message': ex.args[0]})
            

class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for rareusers

    Arguments:
        serializers
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'created_on', 'active', 'profile_image_url', 'subscribed')
        depth = 2