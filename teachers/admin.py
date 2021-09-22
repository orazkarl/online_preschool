from django.contrib import admin

from .models import Subject, StudentGroup, HomeWork, Lesson


admin.site.register(Subject)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('subjects',)


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ['student_group', 'subject', 'date']
    list_filter = ('subject', 'student_group__name',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['subject', 'student_group', 'name', 'description', 'date']
    list_filter = ('subject', 'student_group__name',)
    readonly_fields = ('subject', 'student_group__name')
   
