from django.views import generic

from .models import Subject, StudentGroup, Lesson


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
