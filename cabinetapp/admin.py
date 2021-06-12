from django.contrib import admin

from cabinetapp.models import Subject, StudentGroup, Schedule, EventSchedule, TimeLesson

admin.site.register(Subject)
admin.site.register(TimeLesson)
# admin.site.register(StudentGroup)

@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ('subjects',)



class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    raw_id_fields = ['schedule']
    extra = 1


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['group_student']
    inlines = [EventScheduleInline]





from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from allauth.account.admin import EmailAddress
from allauth.socialaccount.admin import SocialApp, SocialAccount, SocialToken

admin.site.unregister(SocialApp)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)
admin.site.unregister(Group)
admin.site.unregister(Site)
