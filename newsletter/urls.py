from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import IndexView, contacts, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailListView, MailDetailView, MailCreateView, MailUpdateView, MailDeleteView, toogle_activity

app_name = NewsletterConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),

    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/view/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='edit_message'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('mail/', MailListView.as_view(), name='mail_list'),
    path('mail/view/<int:pk>/', MailDetailView.as_view(), name='view_mail'),
    path('mail/create/', MailCreateView.as_view(), name='create_mail'),
    path('mail/edit/<int:pk>/', MailUpdateView.as_view(), name='edit_mail'),
    path('mail/delete/<int:pk>/', MailDeleteView.as_view(), name='delete_mail'),
    path('mail/activity/<int:pk>/', toogle_activity, name='toogle_activity'),
]
