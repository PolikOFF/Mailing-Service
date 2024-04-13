import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from newsletter.forms import ClientForm, MessageForm, MailForm
from newsletter.models import Client, Message, Mail
from newsletter.services import get_cache_for_mailings


class IndexView(TemplateView):
    template_name = 'newsletter/index.html'
    extra_context = {
        'title': 'Главная',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mail_count'] = get_cache_for_mailings()
        context_data['active_mail_count'] = len(Mail.objects.filter(is_active=True))
        context_data['client_count'] = len(Client.objects.all())
        context_data['object_list'] = random.sample(list(Blog.objects.all()), 3)

        return context_data


def contacts(request):
    context = {
        'title': "Контакты",
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name} ({phone}, {email}): {message}")

    return render(request, 'newsletter/contacts.html', context)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    extra_context = {
        'title': "Клиенты сервиса ",
    }

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    extra_context = {
        'title': "Сообщения для рассылки ",
    }

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')


class MailListView(LoginRequiredMixin, ListView):
    model = Mail
    extra_context = {
        'title': "Рассылки ",
    }

    def get_queryset(self, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Mail.objects.all()
        p_view_mail = Permission.objects.get(codename='view_mail')
        p_change_mail = Permission.objects.get(codename='change_mail')
        p_delete_mail = Permission.objects.get(codename='delete_mail')
        self.request.user.user_permissions.set([p_view_mail, p_change_mail, p_delete_mail])
        return Mail.objects.filter(owner=self.request.user)


class MailDetailView(PermissionRequiredMixin, DetailView):
    model = Mail
    permission_required = 'newsletter.view_mail'


class MailCreateView(CreateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('newsletter:mail_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailUpdateView(PermissionRequiredMixin, UpdateView):
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('newsletter:mail_list')
    permission_required = 'newsletter.change_mail'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailDeleteView(PermissionRequiredMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('newsletter:mail_list')
    permission_required = 'newsletter.delete_mail'


def toogle_activity(request, pk):
    mail_item = get_object_or_404(Mail, pk=pk)
    if mail_item.is_active:
        mail_item.is_active = False
    else:
        mail_item.is_active = True
    mail_item.save()
    return redirect('newsletter:mail_list')