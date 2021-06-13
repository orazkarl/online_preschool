from django.urls import path

from . import views

urlpatterns = [
    path('student/profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('student/schedule/', views.ScheduleView.as_view(), name='student_schedule'),
    path('student/homework/', views.HomeWorkView.as_view(), name='student_homework'),
    path('student/grades/', views.GradesView.as_view(), name='student_grades'),
]
