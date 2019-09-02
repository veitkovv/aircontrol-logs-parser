from rest_framework import routers, serializers, viewsets
from .models import Roll
from django.contrib.auth import get_user_model


class RollSerializer(serializers.HyperlinkedModelSerializer):
    duration = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    class Meta:
        model = Roll
        fields = '__all__'


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'email', 'is_staff']
