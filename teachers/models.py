from django.db import models


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
    student_group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons')
    name = models.CharField(max_length=255, verbose_name='Название урока')
    date = models.DateField()

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

