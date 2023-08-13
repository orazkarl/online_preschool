from userapp.models import Student


def is_student(user):
    if Student.objects.filter(user=user).exists():
        return True
    return False
