from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='заголовок')
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blogs/', **NULLABLE, verbose_name='изображение')
    date_is_published = models.DateField(**NULLABLE, verbose_name='дата публикации')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
