from rest_framework import viewsets
from django.contrib.auth import get_user_model

import django_filters

from ..models import Roll, CreatedBy
from mainapp.api.serializers import RollSerializer, UserSerializer, CreatedBySerializer


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


class CreatedByViewSet(viewsets.ModelViewSet):
    queryset = CreatedBy.objects.all()
    serializer_class = CreatedBySerializer


