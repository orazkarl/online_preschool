from django.views import generic

from .models import Schedule, EventSchedule, TimeLesson


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
        student = request.user
        time_lessons = TimeLesson.objects.all()
        monday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='0')
        tuesday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='1')
        wednesday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='2')
        thursday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='3')
        friday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='4')
        saturday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='5')
        sunday = EventSchedule.objects.filter(schedule__group_student=student.student.student_group, day='6')
        self.extra_context = {
            'student': student,
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


class HomeWorkView(generic.TemplateView):
    template_name = 'students/homework.html'


class GradesView(generic.TemplateView):
    template_name = 'students/grades.html'


