from django.shortcuts import render

# Create your views here.
from django.views import generic
import requests
from django.conf import settings
from django.views.generic.base import View
from store.models import Animal


class AnimalTemplateListView(generic.ListView):
    template_name = 'list.html'
    context_object_name = 'animals'

    def get_queryset(self):
        print(self.kwargs)
        base_url = settings.WEB_URL
        url = f'{base_url}/api/v1/list/'
        payload = {'limit': 5, 'offset': 0}
        request = requests.get(url=url, params=payload)
        if request.status_code == 200:
            return request.json()
        return []


class AnimalTemplateDetailView(generic.TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs.get('pk', 0)
        base_url = settings.WEB_URL
        url = f'{base_url}/api/v1/detail/{pk}'
        request = requests.get(url=url)
        context = super(AnimalTemplateDetailView, self).get_context_data(**kwargs)
        if request.status_code == 200:
            context['animal'] = request.json()
        return context