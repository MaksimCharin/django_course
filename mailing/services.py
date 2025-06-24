from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
import logging

from .models import Mailing, MailingAttempt
from config.settings import EMAIL_HOST_USER

logger = logging.getLogger(__name__)

@login_required
def run_mailing(request, pk):
    """Функция запуска рассылки по требованию"""
    mailing = get_object_or_404(Mailing, id=pk)

    if not mailing.is_active:
        messages.error(request, f'Рассылка "{mailing.message.email_subject}" заблокирована и не может быть запущена.')
        logger.warning(
            f"Попытка запуска заблокированной рассылки ID: {pk} пользователем {request.user.username} (ID: {request.user.id})"
        )
        return redirect("mailing:mailings")

    if not request.user.is_superuser and mailing.owner != request.user:
        messages.error(request, 'У вас нет прав для запуска этой рассылки.')
        logger.warning(
            f"Пользователь {request.user.username} (ID: {request.user.id}) попытался запустить чужую рассылку (ID: {pk})")
        return redirect("mailing:mailings")

    if mailing.status == Mailing.STATUS_LAUNCHED:
        messages.info(request, f'Рассылка "{mailing.message.email_subject}" уже запущена.')
        logger.info(f"Попытка запуска уже запущенной рассылки ID: {pk} пользователем {request.user.username}.")
        return redirect("mailing:mailings")

    if mailing.status == Mailing.STATUS_CREATED or \
       (mailing.status == Mailing.STATUS_COMPLETED and not mailing.end_time) or \
       (mailing.status == Mailing.STATUS_COMPLETED and mailing.end_time < timezone.now()):
        mailing.status = Mailing.STATUS_LAUNCHED
        mailing.save(update_fields=['status'])
        messages.success(request, f'Рассылка "{mailing.message.email_subject}" запущена.')
        logger.info(f"Рассылка ID: {mailing.pk} запущена вручную пользователем {request.user.username}.")
    else:

        messages.warning(request, f'Рассылка "{mailing.message.email_subject}" не может быть запущена в текущем статусе.')
        logger.warning(f"Не удалось запустить рассылку ID: {pk} в статусе {mailing.status}.")
        return redirect("mailing:mailings")


    recipients_to_send = mailing.recipients.all()
    successful_sends = 0
    failed_sends = 0

    for recipient in recipients_to_send:
        try:
            send_mail(
                subject=mailing.message.email_subject,
                message=mailing.message.email_body,
                from_email=EMAIL_HOST_USER,
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