from django.contrib import admin

from .models import Schedule, EventSchedule, TimeLesson

admin.site.register(TimeLesson)

class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    raw_id_fields = ['schedule']
    extra = 1


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['group_student']
    inlines = [EventScheduleInline]





