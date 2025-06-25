from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .forms import MailingRecipientForm, MessageForm, MailingForm
from .models import MailingRecipient, Message, Mailing, MailingAttempt
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from config.settings import LOGIN_URL, EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class ManagerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser and not request.user.groups.filter(name='Менеджер').exists():
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('mailing:home')
        return super().dispatch(request, *args, **kwargs)


def manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(LOGIN_URL)
        if not request.user.is_superuser and not request.user.groups.filter(name='Менеджер').exists():
            messages.error(request, 'У вас нет прав для доступа к этой странице.')
            return redirect('mailing:home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Контроллеры для управления получателями рассылки
class MailingRecipientListView(LoginRequiredMixin, ListView):
    model = MailingRecipient
    template_name = 'mailing/recipients_list.html'
    context_object_name = 'recipients'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return MailingRecipient.objects.all()
        return MailingRecipient.objects.filter(owner=self.request.user)


class MailingRecipientDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = MailingRecipient
    template_name = 'mailing/recipient.html'

    def test_func(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return True
        obj = self.get_object()
        return obj.owner == self.request.user


class MailingRecipientCreateView(LoginRequiredMixin, CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingRecipientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_superuser


class MailingRecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MailingRecipient
    context_object_name = 'recipient'
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipients')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_superuser


# Контроллеры для управления сообщениями
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'mailing/message.html'

    def test_func(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return True
        obj = self.get_object()
        return obj.owner == self.request.user


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_superuser


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    context_object_name = 'message'
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_superuser


# Контроллеры для управления рассылкой
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailings.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing.html'

    def test_func(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return True
        obj = self.get_object()
        return obj.owner == self.request.user


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = Mailing.STATUS_CREATED
        form.instance.is_active = True
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_superuser


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.is_superuser


# Контроллеры для управления попыткой рассылки
class MailingAttemptsListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_list_statistics.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            return MailingAttempt.objects.all().select_related('mailing__message')

        user_mailings = Mailing.objects.filter(owner=self.request.user)
        return MailingAttempt.objects.filter(mailing__in=user_mailings).select_related('mailing__message')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
            filtered_attempts = MailingAttempt.objects.all()
            context['is_manager_view'] = True
        else:
            user_mailings = Mailing.objects.filter(owner=self.request.user)
            filtered_attempts = MailingAttempt.objects.filter(mailing__in=user_mailings)
            context['is_manager_view'] = False

        context["successful"] = filtered_attempts.filter(status=MailingAttempt.STATUS_SUCCESSFULLY).count()
        context["failed"] = filtered_attempts.filter(status=MailingAttempt.STATUS_NOT_SUCCESSFULLY).count()

        context["mailings_with_successful_attempts"] = filtered_attempts.filter(status=MailingAttempt.STATUS_SUCCESSFULLY).values('mailing').distinct().count()
        context["total_mailing_attempts"] = filtered_attempts.count()

        return context


class HomePageView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        count_mailing = 0
        active_mailings_count = 0
        unique_recipients_count = 0

        if self.request.user.is_authenticated:
            if self.request.user.groups.filter(name='Менеджер').exists() or self.request.user.is_superuser:
                all_mailings = Mailing.objects.all()
                unique_recipients_count = MailingRecipient.objects.count()
            else:
                all_mailings = Mailing.objects.filter(owner=self.request.user)
                unique_recipients_count = MailingRecipient.objects.filter(owner=self.request.user).count()

            count_mailing = all_mailings.count()
            active_mailings_count = all_mailings.filter(is_active=True).count()

        context_data["count_mailing"] = count_mailing
        context_data["active_mailings_count"] = active_mailings_count
        context_data["unique_recipients_count"] = unique_recipients_count

        return context_data


@manager_required
def toggle_mailing_activity(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_superuser:
        if mailing.owner != request.user:
            messages.error(request, 'У вас нет прав для изменения активности этой рассылки.')
            logger.warning(
                f"Пользователь {request.user.username} (ID: {request.user.id}) попытался изменить активность чужой рассылки (ID: {pk})")
            return redirect(reverse('mailing:mailings'))


    mailing.is_active = not mailing.is_active
    mailing.save()
    status_text = "отключена" if not mailing.is_active else "включена"
    messages.success(request, f'Рассылка "{mailing.message.email_subject}" успешно {status_text}.')
    logger.info(f"Менеджер {request.user.username} {status_text} рассылку ID: {mailing.id}.")
    return redirect(reverse('mailing:mailings'))

@manager_required
def run_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    if not request.user.groups.filter(name='Менеджер').exists() and not request.user.is_superuser:
        if mailing.owner != request.user:
            messages.error(request, 'У вас нет прав для запуска этой рассылки.')
            logger.warning(
                f"Пользователь {request.user.username} (ID: {request.user.id}) попытался запустить чужую рассылку (ID: {pk})")
            return redirect("mailing:mailings")

    if not mailing.is_active:
        messages.error(request, f'Рассылка "{mailing.message.email_subject}" заблокирована и не может быть запущена.')
        logger.warning(
            f"Попытка запуска заблокированной рассылки ID: {pk} пользователем {request.user.username} (ID: {request.user.id})"
        )
        return redirect("mailing:mailings")

    if mailing.status == Mailing.STATUS_LAUNCHED:
        messages.info(request, f'Рассылка "{mailing.message.email_subject}" уже запущена.')
        logger.info(f"Попытка запуска уже запущенной рассылки ID: {pk} пользователем {request.user.username}.")
        return redirect("mailing:mailings")

    if mailing.status == Mailing.STATUS_CREATED or \
       (mailing.status == Mailing.STATUS_COMPLETED and (mailing.end_time is None or mailing.end_time < timezone.now())):
        mailing.status = Mailing.STATUS_LAUNCHED
        mailing.save(update_fields=['status'])
        messages.success(request, f'Рассылка "{mailing.message.email_subject}" запущена.')
        logger.info(f"Рассылка ID: {mailing.pk} запущена вручную пользователем {request.user.username}.")
    else:
        messages.warning(request, f'Рассылка "{mailing.message.email_subject}" не может быть запущена в текущем статусе ({mailing.get_status_display()}).')
        logger.warning(f"Не удалось запустить рассылку ID: {pk} в статусе {mailing.status}.")
        return redirect("mailing:mailings")

    recipients_to_send = mailing.recipients.all()
    successful_sends = 0
    failed_sends = 0

    if not recipients_to_send:
        messages.info(request, f'Рассылка "{mailing.message.email_subject}" не имеет получателей. Отправка не произведена.')
        mailing.status = Mailing.STATUS_COMPLETED
        mailing.save(update_fields=['status'])
        logger.info(f"Рассылка ID: {mailing.pk} не имеет получателей. Завершена немедленно.")
        return redirect("mailing:mailings")


    email_from = EMAIL_HOST_USER

    for recipient in recipients_to_send:
        try:
            send_mail(
                subject=mailing.message.email_subject,
                message=mailing.message.email_body,
                from_email=email_from,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                status=MailingAttempt.STATUS_SUCCESSFULLY,
                server_response="Сообщение успешно отправлено.",
                mailing=mailing,
            )
            logger.info(f"Письмо успешно отправлено для {recipient.email} (рассылка ID: {mailing.pk})")
            successful_sends += 1

        except Exception as e:
            error_message = f"Ошибка при отправке письма для {recipient.email}: {str(e)}"
            logger.error(error_message, exc_info=True)
            MailingAttempt.objects.create(
                status=MailingAttempt.STATUS_NOT_SUCCESSFULLY,
                server_response=error_message,
                mailing=mailing,
            )
            failed_sends += 1

    mailing.status = Mailing.STATUS_COMPLETED
    mailing.save(update_fields=['status'])
    messages.success(request, f'Отправка писем для рассылки "{mailing.message.email_subject}" завершена. Успешно: {successful_sends}, Ошибок: {failed_sends}.')
    logger.info(f"Рассылка ID: {mailing.pk} завершена после ручного запуска. Успешно: {successful_sends}, Ошибок: {failed_sends}.")

    return redirect("mailing:mailings")


class UserListManagerView(ManagerRequiredMixin, ListView):
    model = User
    template_name = 'mailing/user_list_manager.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(is_superuser=False).exclude(pk=self.request.user.pk).order_by('email')


@manager_required
def toggle_user_active_status(request, pk):
    user_to_toggle = get_object_or_404(User, pk=pk)

    if user_to_toggle.is_superuser:
        messages.error(request, 'Невозможно заблокировать/разблокировать суперпользователя.')
        return redirect('mailing:user_list_manager')

    if request.user == user_to_toggle:
        messages.error(request, 'Невозможно заблокировать/разблокировать самого себя.')
        return redirect('mailing:user_list_manager')

    user_to_toggle.is_active = not user_to_toggle.is_active
    user_to_toggle.save(update_fields=['is_active'])

    status_text = "заблокирован" if not user_to_toggle.is_active else "разблокирован"
    messages.success(request, f'Пользователь "{user_to_toggle.email}" успешно {status_text}.')
    logger.info(f"Менеджер {request.user.username} {status_text} пользователя {user_to_toggle.email} (ID: {user_to_toggle.id}).")

    return redirect('mailing:user_list_manager')