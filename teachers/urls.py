from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.TeacherProfileView.as_view(), name='teacher_profile'),
    path('studentgroups', views.StudentGroupListView.as_view(), name='teacher_studentgroups'),
    path('studentgroups/<int:group_id>/subjects/<int:subject_id>', views.SubjectDetailView.as_view(), name='teacher_studentgroupdetail'),
    path('studentgroups/<int:group_id>/lesson/create', views.LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:lesson_id>/grade/', views.StudentGroupGradeView.as_view(), name='teacher_studentgroupgrade'),
    path('studentgroups/<int:group_id>/monthlygrade/<int:subject_id>/', views.MonthlyGradeView.as_view(), name='teacher_monthlygrade'),

]
