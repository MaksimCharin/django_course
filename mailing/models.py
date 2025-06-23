from django.db import models


class MailingRecipient(models.Model):
    """Получатель рассылки"""
    email = models.EmailField(verbose_name='Адрес электронной почты')
    full_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='Ф. И. О.')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f'Получатель рассылки: {self.full_name}, email: {self.email}'

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['email', 'full_name']


class Message(models.Model):
    """Сообщение"""
    email_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    email_body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'Тема письма: {self.email_subject}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['email_subject']


class Mailing(models.Model):
    """Рассылка"""
    STATUS = {'CREATED': 'Создана', 'LAUNCHED': 'Запущена', 'COMPLETED': 'Завершена'}
    first_sending = models.DateField(auto_now_add=True, verbose_name='Дата и время первой отправки')
    last_sending = models.DateField(auto_now=True, verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=9, choices=STATUS, default="Создана", verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сообщение')
    recipients = models.ManyToManyField(MailingRecipient, verbose_name='Получатели рассылки')
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    def __str__(self):
        return f'Статус: {self.status}, Получатели: {self.recipients}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['first_sending', 'last_sending', 'status']


class MailingAttempt(models.Model):
    """Попытка рассылки"""
    STATUS = {'SUCCESSFULLY': 'Успешно', 'NOT_SUCCESSFULLY': 'Не успешно'}
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='Статус')
    server_response = models.TextField(null=True, blank=True, verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Рассылка')

    def __str__(self):
        return f'Статус: {self.status}, Ответ почтового сервера: {self.server_response}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'
        ordering = ['create_at', 'status', 'server_response']