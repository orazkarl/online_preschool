from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),

    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>', views.NewsDetailView.as_view(), name='news_detail'),
]
