from ckeditor.fields import RichTextField
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


class Grade(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='grades', verbose_name='Урок')
    student = models.ForeignKey(
        'userapp.Student', on_delete=models.CASCADE, related_name='grades', verbose_name='Студент'
    )
    is_lesson = models.BooleanField(default=False, verbose_name='Успеваемость')
    is_homework = models.BooleanField(default=False, verbose_name='ДЗ')
    is_behavior = models.BooleanField(default=False, verbose_name='Воспитание')

    def __str__(self):
        return f"{self.lesson.name} - {self.student.get_full_name()}"

    def get_grade(self):
        grade = 0
        if self.is_lesson:
            grade += 1
        if self.is_homework:
            grade += 1
        if self.is_behavior:
            grade += 1
        return grade

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        unique_together = ('lesson', 'student')


MONTH_CHOICES = (
    ('1', 'Январь'),
    ('2', 'Февраль'),
    ('3', 'Март'),
    ('4', 'Апрель'),
    ('5', 'Май'),
    ('6', 'Июнь'),
    ('7', 'Июль'),
    ('8', 'Август'),
    ('9', 'Сентябрь'),
    ('10', 'Октябрь'),
    ('11', 'Ноябрь'),
    ('12', 'Декабрь'),
)


class MonthlyGrade(models.Model):
    month = models.CharField(max_length=255, choices=MONTH_CHOICES, verbose_name='Месяц')
    subject = models.ForeignKey(
        Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='monthly_grades'
    )
    student = models.ForeignKey(
        'userapp.Student', on_delete=models.CASCADE, related_name='monthly_grades', verbose_name='Студент'
    )
    grade = models.PositiveIntegerField(verbose_name='Оценка')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.subject.name}"

    class Meta:
        verbose_name = 'Месячная оценка'
        verbose_name_plural = 'Месячная оценка'


class HomeWork(models.Model):
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name='Предмет', related_name='homeworks'
    )
    student_group = models.ForeignKey(
        StudentGroup, on_delete=models.CASCADE, verbose_name='Группа', related_name='homeworks'
    )
    date = models.DateField(verbose_name='Дата')
    content = RichTextField(verbose_name='ДЗ')

    class Meta:
        unique_together = ('subject', 'student_group')
        verbose_name = 'Дом задание'
        verbose_name_plural = 'Дом задании'

    def __str__(self):
        return f"ДЗ группы {self.student_group.name} для предмета {self.subject}"
