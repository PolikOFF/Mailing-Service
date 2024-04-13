from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.CharField(max_length=150, verbose_name='email', unique=True)
    last_name = models.CharField(max_length=150, verbose_name="фамилия")
    first_name = models.CharField(max_length=150, verbose_name='имя')
    father_name = models.CharField(max_length=150, verbose_name='отчество')
    comment = models.TextField(verbose_name='содержимое', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f' {self.last_name} {self.first_name} {self.father_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    title = models.CharField(max_length=250, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Mail(models.Model):
    PERIOD_CHOICES = [
        ('раз в день', 'раз в день'),
        ('раз в неделю', 'раз в неделю'),
        ('раз в месяц', 'раз в месяц'),
    ]
    STATUS_CHOICES = [
        ('создана', 'создана'),
        ('завершена', 'завершена'),
        ('запущена', 'запущена'),
    ]
    name = models.CharField(max_length=100, verbose_name='Название рассылки', default='рассылка')
    clients = models.ManyToManyField(Client, verbose_name='кому (клиенты сервиса)')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="сообщение")
    date_start = models.DateField(verbose_name='дата начала рассылки', default=timezone.now)
    date_next = models.DateTimeField(verbose_name="следующая дата рассылки",default=timezone.now)
    date_end = models.DateField(verbose_name='дата окончания рассылки', default=timezone.now)
    start_time = models.TimeField(verbose_name='время рассылки', default=timezone.now)
    period = models.CharField(max_length=50, choices=PERIOD_CHOICES, verbose_name='периодичность рассылки',
                              default='раз в день')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='статус рассылки',
                              default='создана')
    is_active = models.BooleanField(default=True, verbose_name='активация рассылки')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.name}: Дата начала: {self.date_start}, Дата окончания: {self.date_end}. Статус: {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            ("set_is_active", "Активация рассылки")
        ]


class Log(models.Model):
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='рассылка')
    last_time_mail = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=50, verbose_name='статус попытки')
    response = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    def __str__(self):
        return (f'Дата и время последней попытки: {self.last_time_mail}.'
                f' Статус попытки:{self.status}')

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
