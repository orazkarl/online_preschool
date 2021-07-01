from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from teachers.models import Lesson, Subject, HomeWorkStudent, HomeWork, Grade, MonthlyGrade
from .models import Schedule, EventSchedule, TimeLesson, StudentGroup
from .utils import is_student


@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class StudentProfileView(generic.TemplateView):
    template_name = 'students/profile.html'

    def get(self, request, *args, **kwargs):
        student = request.user
        student_grades = Grade.objects.filter(student=student.student)
        student_grades_dict = dict()
        total = 0
        for grade in student_grades:
            if not grade.lesson.subject.name in student_grades_dict:
                student_grades_dict[grade.lesson.subject.name] = 0
            student_grades_dict[grade.lesson.subject.name] += grade.get_grade()
            total += grade.get_grade()
        self.extra_context = {
            'student': student,
            'student_grades_dict': student_grades_dict,
            'total': total
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

@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class MonthlyGradesView(generic.TemplateView):
    template_name = 'students/monthlygrades.html'

    def get(self, request, *args, **kwargs):
        studentgroup = request.user.student.student_group
        subject = Subject.objects.get(id=self.kwargs['pk'])
        monthly_grades = MonthlyGrade.objects.filter(student=OuterRef('pk'), subject=subject)
        students = studentgroup.students.all().annotate(
            month1=Subquery(monthly_grades.filter(month='1').values('grade')),
            month2=Subquery(monthly_grades.filter(month='2').values('grade')),
            month3=Subquery(monthly_grades.filter(month='3').values('grade')),
            month4=Subquery(monthly_grades.filter(month='4').values('grade')),
            month5=Subquery(monthly_grades.filter(month='5').values('grade')),
            month6=Subquery(monthly_grades.filter(month='6').values('grade')),
            month7=Subquery(monthly_grades.filter(month='7').values('grade')),
            month8=Subquery(monthly_grades.filter(month='8').values('grade')),
            month9=Subquery(monthly_grades.filter(month='9').values('grade')),
            month10=Subquery(monthly_grades.filter(month='10').values('grade')),
            month11=Subquery(monthly_grades.filter(month='11').values('grade')),
            month12=Subquery(monthly_grades.filter(month='12').values('grade')),
        )
        self.extra_context = {
            'subject': subject,
            'students': students,
        }
        return super().get(request, *args, **kwargs)

@method_decorator([login_required, user_passes_test(is_student, login_url='/')], name='dispatch')
class SettingsView(generic.TemplateView):
    template_name = 'students/settings.html'

