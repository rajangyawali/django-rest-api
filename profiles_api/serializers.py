from rest_framework.serializers import ModelSerializer
from . models import UserProfile

class UserProfileSerializer(ModelSerializer):
    """Serializer for UserProfile Model"""

    class Meta:
        model = UserProfile
        fields = ['id','email','name','password']

        extra_kwargs = {'password':{'write_only':True}}