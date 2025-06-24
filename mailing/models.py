from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class MailingRecipient(models.Model):
    """Модель получателя рассылки"""
    email = models.EmailField(verbose_name='Адрес электронной почты', unique=True)
    full_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ф. И. О.')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return f'Получатель: {self.full_name or self.email}' # Отображаем ФИО или email

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['email', 'full_name']


class Message(models.Model):
    """Модель сообщения"""
    email_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    email_body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True)

    def __str__(self):
        return f'Сообщение: {self.email_subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['email_subject']


class Mailing(models.Model):
    """Модель рассылки"""
    STATUS_CREATED = 'created'
    STATUS_LAUNCHED = 'launched'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_LAUNCHED, 'Запущена'),
        (STATUS_COMPLETED, 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки', default=timezone.now)
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')

    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(MailingRecipient, verbose_name='Получатели рассылки')
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец рассылки", null=True, blank=True)

    def __str__(self):
        return f'Рассылка "{self.message.email_subject}" (Статус: {self.get_status_display()})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['start_time', 'end_time', 'status']


class MailingAttempt(models.Model):
    """Модель попытки рассылки"""
    STATUS_SUCCESSFULLY = 'successfully'
    STATUS_NOT_SUCCESSFULLY = 'not_successfully'
    STATUS_CHOICES = [
        (STATUS_SUCCESSFULLY, 'Успешно'),
        (STATUS_NOT_SUCCESSFULLY, 'Не успешно'),
    ]

    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(null=True, blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Рассылка')

    def __str__(self):
        return f'Попытка рассылки {self.mailing.pk if self.mailing else "N/A"} - Статус: {self.get_status_display()} ({self.create_at.strftime("%Y-%m-%d %H:%M")})'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['-create_at']