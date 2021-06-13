from django.urls import path

from . import views

urlpatterns = [
    path('teacher/profile/', views.TeacherProfileView.as_view(), name='teacher_profile'),
    path('teacher/student-groups/<int:group_id>/subjects/<int:subject_id>', views.SubjectDetailView.as_view(), name='teacher_student_group'),
    # path('teacher/lesson/create', views.SubjectDetailView.as_view(), name='teacher_student_group'),
]
