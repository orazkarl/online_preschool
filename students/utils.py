from userapp.models import Student
from teachers.models import HomeWorkStudent

def is_student(user):
    if Student.objects.filter(user=user).exists():
        return True
    return False

def is_send_homework(student, homework):
    if HomeWorkStudent.objects.filter(student=student, homework=homework).exists():
        return True
    return False