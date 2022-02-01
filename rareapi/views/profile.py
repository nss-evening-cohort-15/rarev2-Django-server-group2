from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import RareUser


@api_view(['GET'])
def get_rareuser_profile(request):
    rareuser = RareUser.objects.get(user=request.auth.user)

    serializer = RareUserSerializer(rareuser, context={'request': request})
    
    profile = {}
    profile["rareuser"] = serializer.data

    return Response(profile)


class RareUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'created_on', 'active', 'profile_image_url')
        depth = 2
