# users/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
import logging

from .forms import UserRegisterForm
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

class RegisterView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html' # Создадим этот шаблон
    success_url = reverse_lazy('users:login') # Куда перенаправить после успешной регистрации
    success_message = "Ваша учетная запись успешно создана. Пожалуйста, подтвердите свой Email."

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False # Пользователь неактивен до подтверждения email
        user.save()

        # Отправка письма для подтверждения email
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link = self.request.build_absolute_uri(
            reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        )

        subject = "Подтверждение регистрации на сайте Django-project"
        message = render_to_string('users/email_confirmation.html', {
            'user': user,
            'confirm_link': confirm_link,
        })
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER, # От кого
                [user.email], # Кому
                fail_silently=False,
            )
            logger.info(f"Письмо подтверждения отправлено для {user.email}")
        except Exception as e:
            messages.error(self.request, f"Ошибка при отправке письма подтверждения: {e}")
            logger.error(f"Ошибка при отправке письма подтверждения для {user.email}: {e}", exc_info=True)
            # Возможно, стоит удалить пользователя или пометить его как требующего повторной отправки

        return super().form_valid(form)

def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш email успешно подтвержден! Теперь вы можете войти.')
        logger.info(f"Email пользователя {user.username} (ID: {user.id}) успешно подтвержден.")
        return redirect(reverse_lazy('users:login'))
    else:
        messages.error(request, 'Ссылка для подтверждения недействительна или срок ее действия истек.')
        logger.warning(f"Недействительная или просроченная ссылка подтверждения для uid={uidb64}, token={token}.")
        return redirect(reverse_lazy('users:register')) # Или на другую страницу с ошибкой