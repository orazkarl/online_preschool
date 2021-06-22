from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Subject, StudentGroup, Lesson, HomeWork, Grade, MonthlyGrade
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

@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class StudentGroupListView(generic.ListView):
    model = StudentGroup
    template_name = 'teachers/studentgroup_list.html'

    def get(self, request, *args, **kwargs):
        self.queryset = StudentGroup.objects.filter(subjects__teacher=request.user.teacher)
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
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


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class LessonCreateView(generic.TemplateView):
    template_name = 'teachers/lesson_create.html'

    def get(self, request, *args, **kwargs):
        subject = request.user.teacher.subject
        studentgroup = StudentGroup.objects.get(id=self.kwargs['group_id'])
        self.extra_context = {
            'studentgroup': studentgroup,
            'subject': subject,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        studentgroup = request.POST['studentgroup']
        subject = request.POST['subject']
        name = request.POST['name']
        description = request.POST['description']
        date = request.POST['date']
        homework_name = request.POST['homework_name']
        homework_description = request.POST['homework_description']
        lesson = Lesson.objects.create(subject_id=subject, student_group_id=studentgroup, name=name, description=description, date=date)
        HomeWork.objects.create(lesson=lesson, name=homework_name, description=homework_description)
        return redirect(reverse('teacher_studentgroupdetail', kwargs={'group_id': int(studentgroup), 'subject_id': int(subject)}))

@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class StudentGroupGradeView(generic.TemplateView):
    template_name = 'teachers/studentgroup_grade.html'

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs.get('lesson_id'))
        studentgroup = lesson.student_group
        self.extra_context = {
            'lesson':lesson,
            'studentgroup': studentgroup,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs.get('lesson_id'))
        studentgroup = lesson.student_group
        subject = lesson.subject

        for student in studentgroup.students.all():
            is_lesson = False
            is_homework = False
            is_behavior = False
            if str(student.id) + '__is_lesson' in request.POST:
                is_lesson = True
            if str(student.id) + '__is_homework' in request.POST:
                is_homework = True
            if str(student.id) + '__is_behavior' in request.POST:
                is_behavior = True
            Grade.objects.create(lesson=lesson, student=student, is_lesson=is_lesson, is_homework=is_homework, is_behavior=is_behavior)
        return redirect(
            reverse('teacher_studentgroupdetail', kwargs={'group_id': studentgroup.id, 'subject_id': subject.id}))


class MonthlyGradeView(generic.TemplateView):
    template_name = 'teachers/monthlygrade.html'