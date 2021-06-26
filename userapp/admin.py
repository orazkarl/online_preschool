from django.contrib import admin

from .models import Teacher, Student, User
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# admin.site.register(User)

class TeacherInline(admin.StackedInline):
    model = Teacher
    raw_id_fields = ['user']
    extra = 1


class TeacherUser(User):
    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учители'
        proxy = True


@admin.register(TeacherUser)
class TeacherUserAdmin(DjangoUserAdmin):
    list_display = ['first_name', 'last_name']
    inlines = [TeacherInline]
    # readonly_fields = ['username', 'email', 'last_login', 'date_joined']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(teacher=None)

    fieldsets = (
        (None,
         {'fields': ('username', 'email', 'password')}),
        (('Личная информация'),
         {'fields': (
             'first_name', 'last_name', 'avatar','dob', 'phone')}),
        (('Права доступа'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Дата и время', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'avatar',  'dob',  'phone', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

class StudentInline(admin.StackedInline):
    model = Student
    raw_id_fields = ['user']
    extra = 1


class StudentUser(User):
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        proxy = True


@admin.register(StudentUser)
class StudentUserAdmin(DjangoUserAdmin):
    list_display = ['first_name', 'last_name']
    inlines = [StudentInline]


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(student=None)

    fieldsets = (
        (None,
         {'fields': ('username', 'email', 'password')}),
        (('Личная информация'),
         {'fields': (
             'first_name', 'last_name', 'avatar','dob', 'phone')}),
        (('Права доступа'), {
            'fields': ('is_active',),
        }),
        ('Дата и время', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'avatar', 'dob',  'phone', 'password1', 'password2'),
        }),
    )



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
