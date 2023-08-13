from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from students import DAYS_OF_WEEK
from students.models import EventSchedule
from students.utils import is_student
from teachers.models import Subject, Grade, MonthlyGrade, HomeWork, StudentGroup


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class StudentProfileView(generic.TemplateView):
    template_name = 'students/profile.html'

    def get_context_data(self, **kwargs):
        student = self.request.user
        student_grades = Grade.objects.filter(student=student.student)
        student_grades_dict = {}

        for grade in student_grades:
            subject_name = grade.lesson.subject.name
            student_grades_dict[subject_name] = student_grades_dict.get(subject_name, 0) + grade.get_grade()

        total = sum(student_grades_dict.values())

        context = super().get_context_data(**kwargs)
        context.update({
            'student': student,
            'student_grades_dict': student_grades_dict,
            'total': total,
        })
        return context


class ScheduleView(generic.TemplateView):
    template_name = 'students/schedule.html'

    def get(self, request, *args, **kwargs):
        student_group = get_object_or_404(StudentGroup, id=self.kwargs.get('group_id'))
        days = [day[1] for day in DAYS_OF_WEEK]
        day_schedules = {
            day: EventSchedule.objects.filter(
                schedule__group_student=student_group, day=day
            ).select_related('time_lesson', 'subject')
            for day in days
        }
        self.extra_context = {
            'student_group': student_group,
            'day_schedules': day_schedules,
        }
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class SubjectListView(generic.ListView):
    model = Subject
    template_name = 'students/subject_list.html'

    def get_queryset(self):
        return self.request.user.student.student_group.subjects.all()


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class MonthlyGradesView(generic.TemplateView):
    template_name = 'students/monthlygrades.html'

    def get(self, request, *args, **kwargs):
        studentgroup = request.user.student.student_group
        subject = Subject.objects.get(id=self.kwargs['pk'])
        monthly_grades = MonthlyGrade.objects.filter(student=OuterRef('pk'), subject=subject)
        students = studentgroup.students.all().annotate(
            **{
                f'month{i}': Subquery(monthly_grades.filter(month=str(i)).values('grade'))
                for i in range(1, 13)
            }
        )
        self.extra_context = {
            'subject': subject,
            'students': students,
        }
        return super().get(request, *args, **kwargs)


class HomeWorksView(generic.ListView):
    model = HomeWork
    template_name = 'students/homeworks.html'

    def get_queryset(self):
        student_group = self.request.user.student.student_group
        return HomeWork.objects.filter(student_group=student_group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'studentgroup': self.request.user.student.student_group,
        })
        return context


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class SettingsView(generic.TemplateView):
    template_name = 'students/settings.html'
