from django.shortcuts import render, redirect
from django.views import generic

from userapp.models import Student, Teacher
from .models import News


class HomeView(generic.TemplateView):
    template_name = 'mainapp/home.html'

    def get(self, request, *args, **kwargs):
        if str(request.user) != 'AnonymousUser':
            if Student.objects.filter(user=request.user).exists():
                return redirect('student_profile')
            elif Teacher.objects.filter(user=request.user).exists():
                return redirect('teacher_profile')
            elif request.user.is_superuser:
                return redirect('/admin')
        return redirect('account_inactive')

class NewsListView(generic.ListView):
    model = News
    # paginate_by = 10

class NewsDetailView(generic.DetailView):
    model = News
