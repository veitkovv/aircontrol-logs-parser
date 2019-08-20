from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from mainapp.views import ScanLogsView
from mainapp.models import Roll


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RollSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Roll
        fields = '__all__'


class RollViewSet(viewsets.ModelViewSet):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'rolls', RollViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('scan-logs/', ScanLogsView.as_view(), name='scan_logs'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
