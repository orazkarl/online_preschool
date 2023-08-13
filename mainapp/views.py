from django.shortcuts import redirect
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from students.utils import is_student
from userapp.models import Student, Teacher
from .models import News


@method_decorator(login_required(login_url='/accounts/login/'), name='dispatch')
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


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class NewsListView(generic.ListView):
    model = News


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class NewsDetailView(generic.DetailView):
    model = News
