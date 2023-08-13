from userapp.models import Teacher


def is_teacher(user):
    if Teacher.objects.filter(user=user).exists():
        return True
    return False
