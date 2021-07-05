from django.db.models import F, OuterRef, Subquery, Exists
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Subject, StudentGroup, Lesson, Grade, MonthlyGrade
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
        Lesson.objects.create(subject_id=subject, student_group_id=studentgroup, name=name, description=description, date=date)
        return redirect(reverse('teacher_studentgroupdetail', kwargs={'group_id': int(studentgroup), 'subject_id': int(subject)}))


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class StudentGroupGradeView(generic.TemplateView):
    template_name = 'teachers/studentgroup_grade.html'

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs.get('lesson_id'))
        studentgroup = lesson.student_group
        students = studentgroup.students.all()
        grades = Grade.objects.filter(student=OuterRef('pk'), lesson=lesson)
        students = studentgroup.students.all().annotate(
            is_lesson=Subquery(grades.values('is_lesson')),
            is_homework=Subquery(grades.values('is_homework')),
            is_behavior=Subquery(grades.values('is_behavior')),
        )
        self.extra_context = {
            'lesson':lesson,
            'studentgroup': studentgroup,
            'students': students,
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
            Grade.objects.update_or_create(lesson=lesson,
                                           student=student,
                                           defaults={
                                               'is_lesson': is_lesson,
                                               'is_homework': is_homework,
                                                'is_behavior': is_behavior}
                                           )
        return redirect(
            reverse('teacher_studentgroupdetail', kwargs={'group_id': studentgroup.id, 'subject_id': subject.id}))


class MonthlyGradeView(generic.TemplateView):
    template_name = 'teachers/monthlygrade.html'

    def get(self, request, *args, **kwargs):
        studentgroup = StudentGroup.objects.get(id=self.kwargs['group_id'])
        subject = Subject.objects.get(id=self.kwargs['subject_id'])
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
            'studentgroup': studentgroup,
            'subject': subject,
            'students': students,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        studentgroup = StudentGroup.objects.get(id=self.kwargs['group_id'])
        subject = Subject.objects.get(id=self.kwargs['subject_id'])

        for student in studentgroup.students.all():
            month1 = request.POST['student_' + str(student.id) + '_month1']
            month2 = request.POST['student_' + str(student.id) + '_month2']
            month3 = request.POST['student_' + str(student.id) + '_month3']
            month4 = request.POST['student_' + str(student.id) + '_month4']
            month5 = request.POST['student_' + str(student.id) + '_month5']
            month6 = request.POST['student_' + str(student.id) + '_month6']
            month7 = request.POST['student_' + str(student.id) + '_month7']
            month8 = request.POST['student_' + str(student.id) + '_month8']
            month9 = request.POST['student_' + str(student.id) + '_month9']
            month10 = request.POST['student_' + str(student.id) + '_month10']
            month11 = request.POST['student_' + str(student.id) + '_month11']
            month12 = request.POST['student_' + str(student.id) + '_month12']
            if month1:
                MonthlyGrade.objects.update_or_create(
                    month='1',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month1
                    }
                )
            if month2:
                MonthlyGrade.objects.update_or_create(
                    month='2',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month2
                    }
                )
            if month3:
                MonthlyGrade.objects.update_or_create(
                    month='3',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month3
                    }
                )
            if month4:
                MonthlyGrade.objects.update_or_create(
                    month='4',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month4
                    }
                )
            if month5:
                MonthlyGrade.objects.update_or_create(
                    month='5',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month5
                    }
                )
            if month6:
                MonthlyGrade.objects.update_or_create(
                    month='6',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month6
                    }
                )
            if month7:
                MonthlyGrade.objects.update_or_create(
                    month='7',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month7
                    }
                )
            if month8:
                MonthlyGrade.objects.update_or_create(
                    month='8',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month8
                    }
                )
            if month9:
                MonthlyGrade.objects.update_or_create(
                    month='9',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month9
                    }
                )
            if month10:
                MonthlyGrade.objects.update_or_create(
                    month='10',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month10
                    }
                )
            if month11:
                MonthlyGrade.objects.update_or_create(
                    month='11',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month11
                    }
                )
            if month12:
                MonthlyGrade.objects.update_or_create(
                    month='12',
                    subject=subject,
                    student=student,
                    defaults={
                        'grade': month12
                    }
                )

        return redirect(reverse('teacher_studentgroupdetail', kwargs={'group_id': studentgroup.id, 'subject_id': subject.id}))