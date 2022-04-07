from django.urls import path, include

from api.v1.search.views import SearchAnimalView
from api.v1.views import AnimalListView, AnimalDetailView

urlpatterns = [
    path('list/', AnimalListView.as_view()),
    path('detail/<int:pk>', AnimalDetailView.as_view()),
    path('search/', SearchAnimalView.as_view()), # give query in q
]