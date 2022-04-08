from django.urls import path, include

from api.v1.search.views import SearchAnimalView
from api.v1.views import AnimalListView, AnimalDetailView
from store.views import AnimalTemplateListView

urlpatterns = [
    path('list/', AnimalTemplateListView.as_view(), name='animal_list'),
]