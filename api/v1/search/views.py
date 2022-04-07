from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
# from django.contrib.postgres.search import SearchVector, SearchQuery
from api.v1.serializers import AnimalListSerializer, AnimalDetailSerializer
from api.v1.search.get_query import get_query
from store.models import Animal


class SearchAnimalView(generics.ListAPIView):
    """
    Search animal api
    """

    serializer_class = AnimalDetailSerializer
    filter_backends = [filters.OrderingFilter,]
    ordering_fields = ['species', 'age']

    def get_queryset(self):
        q = self.request.query_params.get('q')
        products = Animal.objects.filter(is_active=True)
        if q:
            search_fields = ['title', 'category__title', 'description', 'age', 'species']
            query = get_query(q, search_fields)
            products = Animal.objects.filter(query)
        return products
