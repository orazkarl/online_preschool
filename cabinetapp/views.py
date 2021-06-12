from django.shortcuts import render
from django.views import generic


from .models import Subject, StudentGroup, Schedule, EventSchedule, Lesson, Grade

class StudentProfileView(generic.TemplateView):
    template_name = 'cabinetapp/students/profile.html'

    def get(self, request, *args, **kwargs):
        student = request.user

        self.extra_context = {
            'student': student,
        }

        return super().get(request, *args, **kwargs)


class ScheduleView(generic.TemplateView):
    template_name = 'cabinetapp/students/schedule.html'


class HomeWorkView(generic.TemplateView):
    template_name = 'cabinetapp/students/homework.html'


class GradesView(generic.TemplateView):
    template_name = 'cabinetapp/students/grades.html'
