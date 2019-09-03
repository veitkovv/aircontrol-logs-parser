from rest_framework import viewsets
from rest_framework.views import APIView, Response
from django.conf import settings
from django.contrib.auth import get_user_model

import django_filters

from .utils import scan_logs, start_roll_fabric
from .models import Roll
from .serializers import RollSerializer, UserSerializer


class RollFilterSet(django_filters.rest_framework.FilterSet):
    start = django_filters.DateTimeFromToRangeFilter(label='Datetime Range')

    class Meta:
        model = Roll
        fields = {
            'start': ['exact', 'contains', 'gt', 'lt', 'gte', 'lte'],
            'name': ['exact', 'icontains'],
            'uuid': ['exact', ]
        }


class RollViewSet(viewsets.ModelViewSet):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer
    filterset_class = RollFilterSet


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class ScanLogsView(APIView):
    def post(self, request, *args, **kwargs):
        my_result = scan_logs(settings.LOGS_PATH)  # Скан файловой системы
        start_roll_fabric(my_result)
        return Response(data={"status": "done"})
