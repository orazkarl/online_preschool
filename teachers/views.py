from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from teachers.models import Subject, StudentGroup, Lesson, Grade, MonthlyGrade
from teachers.utils import is_teacher


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class TeacherProfileView(generic.TemplateView):
    template_name = 'teachers/profile.html'

    def get(self, request, *args, **kwargs):
        self.extra_context = {
            'teacher': request.user,
        }
        return super().get(request, *args, **kwargs)


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class StudentGroupListView(generic.ListView):
    model = StudentGroup
    template_name = 'teachers/studentgroup_list.html'

    def get_queryset(self):
        return StudentGroup.objects.filter(subjects__teacher=self.request.user.teacher)


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class SubjectDetailView(generic.DetailView):
    model = Subject
    template_name = 'teachers/subject_detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'subject_id'

    def get_context_data(self, **kwargs):
        group = StudentGroup.objects.get(id=self.kwargs['group_id'])
        lessons = self.object.lessons.filter(student_group=group)
        self.extra_context = {
            'studentgroup': group,
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
        Lesson.objects.create(
            subject_id=subject, student_group_id=studentgroup, name=name, description=description, date=date
        )
        return redirect(reverse(
            'teacher_studentgroupdetail',
            kwargs={'group_id': int(studentgroup), 'subject_id': int(subject)}
        ))


@method_decorator([login_required, user_passes_test(is_teacher, login_url='/')], name='dispatch')
class StudentGroupGradeView(generic.TemplateView):
    template_name = 'teachers/studentgroup_grade.html'

    def get(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs.get('lesson_id'))
        studentgroup = lesson.student_group
        grades = Grade.objects.filter(student=OuterRef('pk'), lesson=lesson)
        students = studentgroup.students.all().annotate(
            is_lesson=Subquery(grades.values('is_lesson')),
            is_homework=Subquery(grades.values('is_homework')),
            is_behavior=Subquery(grades.values('is_behavior')),
        )
        self.extra_context = {
            'lesson': lesson,
            'studentgroup': studentgroup,
            'students': students,
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lesson = Lesson.objects.get(id=self.kwargs.get('lesson_id'))
        studentgroup = lesson.student_group
        subject = lesson.subject

        for student in lesson.student_group.students.all():
            is_lesson = str(student.id) + '__is_lesson' in request.POST
            is_homework = str(student.id) + '__is_homework' in request.POST
            is_behavior = str(student.id) + '__is_behavior' in request.POST
            Grade.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={'is_lesson': is_lesson, 'is_homework': is_homework, 'is_behavior': is_behavior}
            )
        return redirect(reverse(
            'teacher_studentgroupdetail',
            kwargs={'group_id': studentgroup.id, 'subject_id': subject.id})
        )


class MonthlyGradeView(generic.TemplateView):
    template_name = 'teachers/monthlygrade.html'

    def get(self, request, *args, **kwargs):
        studentgroup = StudentGroup.objects.get(id=self.kwargs['group_id'])
        subject = Subject.objects.get(id=self.kwargs['subject_id'])
        monthly_grades = MonthlyGrade.objects.filter(student=OuterRef('pk'), subject=subject)
        students = studentgroup.students.all().annotate(
            **{
                f'month{i}': Subquery(monthly_grades.filter(month=str(i)).values('grade'))
                for i in range(1, 13)
            }
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
            for month in range(1, 13):
                grade = request.POST.get(f'student_{student.id}_month{month}')
                if grade:
                    MonthlyGrade.objects.update_or_create(
                        month=str(month),
                        subject=subject,
                        student=student,
                        defaults={
                            'grade': grade
                        }
                    )

        return redirect(reverse(
            'teacher_studentgroupdetail', kwargs={'group_id': studentgroup.id, 'subject_id': subject.id}
        ))
