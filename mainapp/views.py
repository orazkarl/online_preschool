from django.shortcuts import render
from django.views import generic

from .models import News


class HomeView(generic.TemplateView):
    template_name = 'mainapp/home.html'


class NewsListView(generic.ListView):
    model = News
    # paginate_by = 10

class NewsDetailView(generic.DetailView):
    model = News
