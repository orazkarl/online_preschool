# Generated by Django 4.2 on 2023-08-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=1, verbose_name='День')),
                ('comment', models.CharField(blank=True, max_length=100, null=True, verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Урок расписаний',
                'verbose_name_plural': 'Уроки расписании',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
            },
        ),
        migrations.CreateModel(
            name='TimeLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_lesson', models.TimeField(verbose_name='Начало занятий')),
                ('end_lesson', models.TimeField(verbose_name='Окончание занятий')),
            ],
            options={
                'verbose_name': 'Время урока',
                'verbose_name_plural': 'Время урока',
                'ordering': ['start_lesson'],
            },
        ),
    ]
