from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Subject, StudentGroup, Lesson, HomeWork
from .forms import LessonForm, HomeWorkForm
from .utils import is_teacher


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class TeacherProfileView(generic.TemplateView):
    template_name = 'teachers/profile.html'

    def get(self, request, *args, **kwargs):
        teacher = request.user
        self.extra_context = {
            'teacher': teacher,
        }
        return super().get(request, *args, **kwargs)


class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = 'teachers/subject_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'subject_id'

    def get_context_data(self, **kwargs):
        studentgroup = StudentGroup.objects.get(id=self.kwargs['group_id'])
        lessons = self.object.lessons.filter(student_group=studentgroup)
        self.extra_context = {
            'studentgroup': studentgroup,
            'lessons': lessons,
        }
        return super().get_context_data(**kwargs)


class LessonCreateView(generic.CreateView):
    model = Lesson
    template_name = 'teachers/lesson_create.html'
    form_class = LessonForm

    def get(self, request, *args, **kwargs):
        subject = request.user.teacher.subject
        studentgroup = StudentGroup.objects.get(id=self.kwargs['group_id'])
        self.extra_context = {
            'studentgroup': studentgroup,
            'subject': subject,
        }
        return super().get(request, *args, **kwargs)


class LessonDetailView(generic.DetailView, generic.FormView):
    model = Lesson
    template_name = 'teachers/lesson_detail.html'
    form_class = HomeWorkForm

    def get_success_url(self):
        lesson = Lesson.objects.get(id=self.get_object().id)
        return lesson.get_absolute_url()

    def form_valid(self, form):
        form.instance.lesson = self.get_object()
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        try:
            form = HomeWorkForm(instance=self.get_object().homework)
        except:
            print('error')
        else:
            self.extra_context = {
                'form': form
            }
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

