from django.db import models

from ckeditor.fields import RichTextField


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название')
    image = models.ImageField(upload_to='news/', verbose_name='Изоброжение')
    content = RichTextField(verbose_name='Контент')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-created']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
