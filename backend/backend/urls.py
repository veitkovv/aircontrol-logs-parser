from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from mainapp.views import RollViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'rolls', RollViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
