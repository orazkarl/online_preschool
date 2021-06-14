from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),
    path('schedule/', views.ScheduleView.as_view(), name='student_schedule'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('homework/', views.HomeWorkView.as_view(), name='student_homework'),
    path('grades/', views.GradesView.as_view(), name='student_grades'),
]
