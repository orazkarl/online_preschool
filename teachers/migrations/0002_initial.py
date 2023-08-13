# Generated by Django 4.2 on 2023-08-12 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlygrade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_grades', to='userapp.student', verbose_name='Студент'),
        ),
        migrations.AddField(
            model_name='monthlygrade',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monthly_grades', to='teachers.subject'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='student_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='teachers.studentgroup'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lessons', to='teachers.subject'),
        ),
        migrations.AddField(
            model_name='homework',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='teachers.studentgroup', verbose_name='Группа'),
        ),
        migrations.AddField(
            model_name='homework',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='teachers.subject', verbose_name='Предмет'),
        ),
        migrations.AddField(
            model_name='grade',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='teachers.lesson', verbose_name='Урок'),
        ),
        migrations.AddField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='userapp.student', verbose_name='Студент'),
        ),
        migrations.AlterUniqueTogether(
            name='homework',
            unique_together={('subject', 'student_group')},
        ),
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together={('lesson', 'student')},
        ),
    ]
