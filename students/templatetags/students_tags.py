from django import template
from teachers.models import HomeWorkStudent


register = template.Library()

@register.filter(name='is_send_homework')
def is_send_homework(student, homework):
    if HomeWorkStudent.objects.filter(student=student, homework=homework).exists():
        return True
    return False