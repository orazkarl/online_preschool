from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='student_profile'),

    path('schedule/<int:group_id>/', views.ScheduleView.as_view(), name='student_schedule'),
    path('subjects/', views.SubjectListView.as_view(), name='student_subjects'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='student_subject_detail'),
    path('homework/<int:pk>/', views.SendHomeWorkView.as_view(), name='student_homework'),
    path('settings/', views.SettingsView.as_view(), name='student_settings'),

    path('subjects/<int:pk>/monthly-grades/', views.MonthlyGradesView.as_view(), name='student_monthly_grades'),
]
