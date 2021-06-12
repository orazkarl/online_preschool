from django.db import models
from django.contrib.auth.models import AbstractUser

from cabinetapp.models import StudentGroup, Subject


class User(AbstractUser):
    phone = models.CharField(max_length=12, blank=True, verbose_name='Телефон номер')
    dob = models.DateField(null=True, blank=True,  verbose_name='Дата рождение')

class Teacher(models.Model):
    subject = models.OneToOneField(Subject, on_delete=models.SET_NULL, null=True, related_name='teacher',
                                   verbose_name='Предмет учителя')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher', verbose_name='Учитель')

    def __str__(self):
        return f"{self.user.first_name} {self.user.first_name}"


class Student(models.Model):
    student_group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, related_name='students', null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', verbose_name='Студент')

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.first_name}"

    def __str__(self):
        return self.get_full_name()


