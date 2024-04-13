from datetime import datetime, timedelta
from smtplib import SMTPException

import pytz
from django.core.cache import cache

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from newsletter.models import Mail, Log


def my_job():
    day = timedelta(days=1, hours=0, minutes=0)
    week = timedelta(days=7, hours=0, minutes=0)
    month = timedelta(days=30, hours=0, minutes=0)

    mails = Mail.objects.all().filter(status='создана') \
        .filter(is_active=True) \
        .filter(date_next__lte=datetime.now(pytz.timezone('Europe/Moscow'))) \
        .filter(date_end__gte=datetime.now(pytz.timezone('Europe/Moscow')))

    for mail in mails:
        mail.status = 'запущена'
        mail.save()
        emails_list = [client.email for client in mail.clients.all()]

        result = send_mail(
            subject=mail.message.title,
            message=mail.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails_list,
            fail_silently=False,
        )

        if result == 1:
            status = 'отправлено'
        else:
            status = 'Ошибка отправки'

        log = Log(mail=mail, status=status)
        log.save()

        if mail.period == 'раз в день':
            mail.next_date = log.last_time_mail + day
        elif mail.period == 'раз в неделю':
            mail.next_date = log.last_time_mail + week
        elif mail.period == 'раз в месяц':
            mail.next_date = log.last_time_mail + month

        if mail.next_date < mail.end_date:
            mail.status = 'создана'
        else:
            mail.status = 'завершена'
        mail.save()


def get_cache_for_mailings():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mail.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mail.objects.all().count()
    return mailings_count


def send_mailing():
    current_time = timezone.localtime(timezone.now())
    mailing_list = Mail.objects.all()
    for mailing in mailing_list:
        if mailing.date_end < current_time:
            mailing.status = Mail.DONE
            continue
        if mailing.time_start <= current_time < mailing.date_end:
            mailing.status = Mail.STARTED
            mailing.save()
            for client in mailing.client.all():
                try:
                    send_mail(
                        subject=mailing.message.title,
                        message=mailing.message.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )

                    log = Log.objects.create(
                        date=mailing.time_start,
                        status=Log.SENT,
                        mailing=mailing,
                        client=client
                    )
                    log.save()
                    return log

                except SMTPException as error:
                    log = Log.objects.create(
                        date=mailing.time_start,
                        status=Log.FAILED,
                        mailling=mailing,
                        client=client,
                        response=error
                    )
                    log.save()

                    return log

        else:
            mailing.status = Mail.DONE
            mailing.save()
