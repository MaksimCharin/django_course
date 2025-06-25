import secrets
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import logging

from .forms import UserRegisterForm
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Ваша учетная запись успешно создана. Пожалуйста, подтвердите свой Email."

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(32)
        user.token = token
        user.save()
        host = self.request.get_host()
        confirmation_url_path = reverse('users:email_confirm', kwargs={'token': token})
        url_for_confirm = f'{self.request.scheme}://{host}{confirmation_url_path}'
        send_mail(
            subject=f'Подтвердите вашу электронную почту.',
            message=f'Для активации вашей учетной записи пройдите по ссылке {url_for_confirm}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    try:
        user = get_object_or_404(User, token=token)
    except User.DoesNotExist:
        messages.error(request, "Неверная ссылка для активации. Возможно, токен уже использован или некорректен.")
        return redirect(reverse('users:register'))

    if user.is_active:
        messages.info(request, "Ваша учетная запись уже активна.")
        user.token = None
        user.save()
        return redirect(reverse('mailing:home'))

    user.is_active = True
    user_group, created = Group.objects.get_or_create(name='Пользователь')
    user.groups.add(user_group)
    user.token = None
    user.save()

    subject = f'Добро пожаловать в наш сервис, {user.last_name} {user.first_name}.'
    message = f'Здравствуйте {user.last_name} {user.first_name}! Спасибо, что зарегистрировались в нашем сервисе!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

    messages.success(request, "Ваша учетная запись успешно активирована!")
    return redirect(reverse('mailing:home'))