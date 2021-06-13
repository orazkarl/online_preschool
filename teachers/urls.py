from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.TeacherProfileView.as_view(), name='teacher_profile'),
    path('studentgroups/<int:group_id>/subjects/<int:subject_id>', views.SubjectDetailView.as_view(), name='teacher_studentgroup'),
    path('studentgroups/<int:group_id>/lesson/create', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>', views.LessonDetailView.as_view(), name='lesson_detail'),
]
