from django.db import models
from django.urls import reverse


class Subject(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название предмета')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class StudentGroup(models.Model):
    subjects = models.ManyToManyField(Subject, related_name='student_groups')
    name = models.CharField(max_length=250, verbose_name='Название группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons')
    student_group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='lessons')
    name = models.CharField(max_length=255, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', null=True, blank=True)

    date = models.DateField()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def get_absolute_url(self):
        return reverse('teacher_studentgroup',
                       kwargs={'group_id': self.student_group.id, 'subject_id': self.subject.id})

    def __str__(self):
        return self.name


class HomeWork(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='homework', verbose_name='Урок')
    name = models.CharField(max_length=255, verbose_name='Название дом задание')
    description = models.TextField(verbose_name='Описание дом задание', null=True, blank=True)

    class Meta:
        verbose_name = 'Дом. задание'
        verbose_name_plural = 'Дом. задании'

    def __str__(self):
        return self.name


class HomeWorkStudent(models.Model):
    from userapp.models import Student
    homework = models.ForeignKey(HomeWork, on_delete=models.CASCADE, related_name='homework_students', verbose_name='ДЗ')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_students', verbose_name='Студент')
    file = models.FileField(upload_to='homework_students')

    def __str__(self):
        return f"{self.homework.name} - {self.student.get_full_name()}"

    class Meta:
        verbose_name = 'ДЗ Студента'
        verbose_name_plural = 'ДЗ Студента'