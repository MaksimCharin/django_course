import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from mailing.models import Mailing, MailingAttempt

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Отправляет рассылку"""

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS("Начинаю поиск запланированных рассылок...")
        )
        now = timezone.now()

        mailings_to_send = Mailing.objects.filter(
            is_active=True,
            start_time__lte=now,
            status__in=[Mailing.STATUS_CREATED, Mailing.STATUS_COMPLETED],
        ).exclude(status=Mailing.STATUS_LAUNCHED)

        if not mailings_to_send.exists():
            self.stdout.write(
                self.style.INFO("Нет запланированных рассылок для отправки.")
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Найдено {mailings_to_send.count()} рассылок для отправки."
            )
        )

        for mailing in mailings_to_send:
            self.stdout.write(
                f'Обработка рассылки "{mailing.message.email_subject}" (ID: {mailing.pk})...'
            )

            mailing.status = Mailing.STATUS_LAUNCHED
            mailing.save(update_fields=["status"])
            logger.info(f"Рассылка ID: {mailing.pk} запущена по расписанию.")
            self.stdout.write(
                self.style.WARNING(
                    f'Статус рассылки "{mailing.message.email_subject}" изменен на "Запущена".'
                )
            )

            recipients_to_send = mailing.recipients.all()
            if not recipients_to_send.exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Рассылка "{mailing.message.email_subject}" (ID: {mailing.pk}) не имеет получателей. '
                        f'Пропускаю отправку.'
                    )
                )
                mailing.status = Mailing.STATUS_COMPLETED
                mailing.save(update_fields=["status"])
                logger.info(
                    f"Рассылка ID: {mailing.pk} завершена без отправки из-за отсутствия получателей."
                )
                continue

            successful_sends = 0
            failed_sends = 0
            email_from = settings.EMAIL_HOST_USER

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
                    logger.info(
                        f"Письмо успешно отправлено для {recipient.email} (рассылка ID: {mailing.pk})"
                    )
                    successful_sends += 1

                except Exception as e:
                    error_message = (
                        f"Ошибка при отправке письма для {recipient.email}: {str(e)}"
                    )
                    logger.error(error_message, exc_info=True)
                    MailingAttempt.objects.create(
                        status=MailingAttempt.STATUS_NOT_SUCCESSFULLY,
                        server_response=error_message,
                        mailing=mailing,
                    )
                    failed_sends += 1

            mailing.status = Mailing.STATUS_COMPLETED
            mailing.save(update_fields=["status"])
            self.stdout.write(
                self.style.SUCCESS(
                    f'Рассылка "{mailing.message.email_subject}" (ID: {mailing.pk}) завершена. '
                    f'Успешно: {successful_sends}, Ошибок: {failed_sends}.'
                )
            )
            logger.info(
                f"Рассылка ID: {mailing.pk} завершена после автоматического запуска. "
                f"Успешно: {successful_sends}, Ошибок: {failed_sends}."
            )

        self.stdout.write(
            self.style.SUCCESS("Завершение обработки запланированных рассылок.")
        )
