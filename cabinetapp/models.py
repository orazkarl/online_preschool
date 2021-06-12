from django.db import models
from django.contrib.auth.models import AbstractUser
from transliterate import slugify


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
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Grade(models.Model):
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


DAYS_OF_WEEK = (
    ("0", 'Monday'),
    ("1", 'Tuesday'),
    ("2", 'Wednesday'),
    ("3", 'Thursday'),
    ("4", 'Friday'),
    ("5", 'Saturday'),
    ("6", 'Sunday'),
)


class Schedule(models.Model):
    group_student = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='schedule', verbose_name='Группа')
    slug = models.SlugField(unique=True, default='', blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_student.name)
        print(slugify(self.group_student.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Расписание для группы {self.group_student.name}"

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class EventSchedule(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='event_schedules', verbose_name='Расписание')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='event_schedules', verbose_name='Предмет')
    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, verbose_name='День')
    start_lesson = models.TimeField(verbose_name='Начало занятий')
    end_lesson = models.TimeField(verbose_name='Окончание занятий')
    comment = models.CharField(max_length=100, null=True, blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Урок расписаний'
        verbose_name_plural = 'Уроки расписании'

