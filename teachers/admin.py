from django.contrib import admin

from .models import Subject, StudentGroup


admin.site.register(Subject)


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('subjects',)




