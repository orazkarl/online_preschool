from django.contrib import admin

from .models import Subject, StudentGroup, Lesson, HomeWork, HomeWorkStudent, Grade, MonthlyGrade


admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(HomeWork)
admin.site.register(HomeWorkStudent)
admin.site.register(Grade)
admin.site.register(MonthlyGrade)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('subjects',)




