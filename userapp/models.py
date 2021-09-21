from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from teachers.models import StudentGroup, Subject, Grade


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'))
    phone = models.CharField(max_length=12, null=True, verbose_name='Телефон номер')
    dob = models.DateField(null=True,verbose_name='Дата рождение')
    avatar = models.ImageField(upload_to='avatars/', null=True)


class Teacher(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.SET_NULL, null=True, related_name='teacher',
                                   verbose_name='Предмет учителя')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', verbose_name='Учитель')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"





class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', verbose_name='Студент')
    student_group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, related_name='students', null=True)

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.get_full_name()

    def get_total_grades(self):
        student_grades = Grade.objects.filter(student=self)
        total = 0
        for grade in student_grades:
            total += grade.get_grade()
        return total

    def get_ru_status(self):
        if self.get_total_grades() >= 600:
            return 'Супермен'
        elif self.get_total_grades() >= 500:
            return 'Я отличник'
        elif self.get_total_grades() >= 400:
            return 'Я лучший'
        elif self.get_total_grades() >= 300:
            return 'Я умный'
        elif self.get_total_grades() >= 200:
            return 'Я могу'
        else:
            return 'Я стараюсь'

    def get_kk_status(self):
        if self.get_total_grades() >= 600:
            return 'Супермен'
        elif self.get_total_grades() >= 500:
            return 'Мен үздікпін'
        elif self.get_total_grades() >= 400:
            return 'Мен күштімін'
        elif self.get_total_grades() >= 300:
            return 'Мен ақылдымын'
        elif self.get_total_grades() >= 200:
            return 'Жетістікке жетемін'
        else:
            return 'Мен тырысамын'
