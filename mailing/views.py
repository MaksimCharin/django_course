from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .forms import MailingRecipientForm, MessageForm, MailingForm
from .models import MailingRecipient, Message, Mailing, MailingAttempt
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def check_object_ownership(obj, user):
    """Проверяет, владеет ли пользователь объектом или является суперюзером"""
    if user.is_superuser:
        return True
    return obj.owner == user


# Контроллеры для управления получателями рассылки
class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailing/recipients_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MailingRecipient.objects.all()
        return MailingRecipient.objects.filter(owner=self.request.user)


class MailingRecipientDetailView(LoginRequiredMixin, DetailView):
    model = MailingRecipient
    template_name = 'mailing/recipient.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingRecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MailingRecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingRecipient
    context_object_name = 'recipient'
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipients')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


# Контроллеры для управления сообщениями
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    context_object_name = 'message'
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


# Контроллеры для управления рассылкой
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailings.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = Mailing.STATUS_CREATED
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(owner=self.request.user)


class MailingAttemptsListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_list_statistics.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MailingAttempt.objects.all().select_related('mailing__message')
        user_mailings = Mailing.objects.filter(owner=self.request.user)
        return MailingAttempt.objects.filter(mailing__in=user_mailings).select_related('mailing__message')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        if self.request.user.is_superuser:
            filtered_attempts = MailingAttempt.objects.all()
        else:
            user_mailings = Mailing.objects.filter(owner=self.request.user)
            filtered_attempts = MailingAttempt.objects.filter(mailing__in=user_mailings)

        context["successful"] = filtered_attempts.filter(status=MailingAttempt.STATUS_SUCCESSFULLY).count()
        context["failed"] = filtered_attempts.filter(status=MailingAttempt.STATUS_NOT_SUCCESSFULLY).count()

        context["mailings_successful"] = filtered_attempts.values('mailing').distinct().count()
        context["mailing_attempts_count"] = filtered_attempts.count()

        return context


class HomePageView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            all_mailings = Mailing.objects.all()
            unique_recipients_count = MailingRecipient.objects.count()
        else:
            all_mailings = Mailing.objects.filter(owner=self.request.user)

            unique_recipients_count = MailingRecipient.objects.filter(mailing__owner=self.request.user).distinct().count()


        context_data["count_mailing"] = all_mailings.count()

        context_data["active_mailings_count"] = all_mailings.filter(is_active=True).count()

        context_data["unique_recipients_count"] = unique_recipients_count

        return context_data


def toggle_mailing_activity(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    mailing.is_active = not mailing.is_active
    mailing.save()
    return redirect(reverse('mailing:mailings'))