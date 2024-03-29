from django.db import models
from django.contrib.auth.models import AbstractUser

from students import DAYS_OF_WEEK
from teachers.models import StudentGroup, Subject


class Schedule(models.Model):
    group_student = models.ForeignKey(
        StudentGroup, on_delete=models.CASCADE, related_name='schedule', verbose_name='Группа'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Расписание для группы {self.group_student.name}"

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class TimeLesson(models.Model):
    start_lesson = models.TimeField(verbose_name='Начало занятий')
    end_lesson = models.TimeField(verbose_name='Окончание занятий')

    class Meta:
        verbose_name = 'Время урока'
        verbose_name_plural = 'Время урока'
        ordering = ['start_lesson']

    def get_time(self):
        return (f"{self.start_lesson.strftime('%H')}:{self.start_lesson.strftime('%M')} - "
                f"{self.end_lesson.strftime('%H')}:{self.end_lesson.strftime('%M')}")

    def __str__(self):
        return self.get_time()


class EventSchedule(models.Model):
    day = models.CharField(max_length=127, choices=DAYS_OF_WEEK, verbose_name='День')
    time_lesson = models.ForeignKey(
        TimeLesson, on_delete=models.SET_NULL, null=True, verbose_name='Время урока', related_name='event_schedules'
    )
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, related_name='event_schedules', verbose_name='Расписание'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        related_name='event_schedules',
        verbose_name='Предмет',
        null=True, blank=True,
        default=''
    )
    comment = models.CharField(max_length=100, null=True, blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Урок расписаний'
        verbose_name_plural = 'Уроки расписании'
        unique_together = [['day', 'time_lesson', 'subject']]
