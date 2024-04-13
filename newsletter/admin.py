from django.contrib import admin

from newsletter.models import Client, Message, Mail, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'last_name', 'first_name', 'father_name', 'comment','owner',)
    list_filter = ('email', 'last_name','owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body','owner',)
    search_fields = ('title', 'body',)
    list_filter = ('title','owner',)


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'message', 'date_start', 'date_end', 'start_time', 'period', 'status', 'is_active','owner',)
    search_fields = ('message',)
    list_filter = ('is_active','owner',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mail', 'last_time_mail', 'status', 'response',)
