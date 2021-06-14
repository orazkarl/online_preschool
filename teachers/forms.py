from django import forms

from .models import Lesson, HomeWork


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'


class HomeWorkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HomeWorkForm, self).__init__(*args, **kwargs)

    class Meta:
        model = HomeWork
        # fields = '__all__'
        exclude = ['lesson']