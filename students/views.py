from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from teachers.models import Lesson, Subject, HomeWorkStudent, HomeWork, Grade
from .models import Schedule, EventSchedule, TimeLesson, StudentGroup
from .utils import is_student


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class StudentProfileView(generic.TemplateView):
    template_name = 'students/profile.html'

    def get(self, request, *args, **kwargs):
        student = request.user
        self.extra_context = {
            'student': student,
        }
        return super().get(request, *args, **kwargs)


class ScheduleView(generic.TemplateView):
    template_name = 'students/schedule.html'

    def get(self, request, *args, **kwargs):
        student_group = StudentGroup.objects.get(id=self.kwargs.get('group_id'))
        time_lessons = TimeLesson.objects.all()
        monday = EventSchedule.objects.filter(schedule__group_student=student_group, day='0')
        tuesday = EventSchedule.objects.filter(schedule__group_student=student_group, day='1')
        wednesday = EventSchedule.objects.filter(schedule__group_student=student_group, day='2')
        thursday = EventSchedule.objects.filter(schedule__group_student=student_group, day='3')
        friday = EventSchedule.objects.filter(schedule__group_student=student_group, day='4')
        saturday = EventSchedule.objects.filter(schedule__group_student=student_group, day='5')
        sunday = EventSchedule.objects.filter(schedule__group_student=student_group, day='6')
        self.extra_context = {
            'student_group': student_group,
            'time_lessons': time_lessons,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
        }
        return super().get(request, *args, **kwargs)

@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class SubjectListView(generic.ListView):
    model = Subject
    template_name = 'students/subject_list.html'

    def get(self, request, *args, **kwargs):
        self.queryset = request.user.student.student_group.subjects.all()
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = 'students/subject_detail.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class SendHomeWorkView(generic.TemplateView):
    template_name = 'students/homework.html'

    def get(self, request, *args, **kwargs):
        homework = HomeWork.objects.get(id=self.kwargs.get('pk'))
        self.extra_context = {
            'homework': homework,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        homework = HomeWork.objects.get(id=self.kwargs.get('pk'))
        student = request.user.student
        file = request.FILES['file']
        HomeWorkStudent.objects.create(homework=homework, student=student, file=file)
        subject = homework.lesson.subject
        return redirect(reverse('student_subject_detail', kwargs={'pk': subject.id}))


class GradesView(generic.TemplateView):
    template_name = 'students/grades.html'
