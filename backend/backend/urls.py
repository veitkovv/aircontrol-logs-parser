from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from mainapp.api.views import RollViewSet, UserViewSet, CreatedByViewSet

router = routers.DefaultRouter()
router.register(r'rolls', RollViewSet)
router.register(r'users', UserViewSet)
router.register(r'created-by', CreatedByViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
