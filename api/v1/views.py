from rest_framework import filters
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,
)

from api.v1.serializers import AnimalListSerializer, AnimalDetailSerializer
from store.models import Animal


class AnimalListView(ListAPIView):
    """
    Animals list api view
    """

    serializer_class = AnimalListSerializer
    queryset = Animal.objects.filter(is_active=True)
    filter_backends = [filters.OrderingFilter, ]
    ordering_fields = ['species', 'age', 'title', ]


class AnimalDetailView(RetrieveAPIView):
    """
    Animals detail api view
    """

    serializer_class = AnimalDetailSerializer
    queryset = Animal.objects.filter(is_active=True)