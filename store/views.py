from django.shortcuts import render

# Create your views here.
from django.views import generic

from store.models import Animal


class AnimalTemplateListView(generic.ListView):
    model = Animal
    queryset = Animal.objects.filter(is_active=True)
    template_name = 'list.html'
