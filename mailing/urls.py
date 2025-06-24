from django.urls import path
from mailing.apps import MailingConfig
from .views import (
    MailingRecipientListView, MailingRecipientDetailView, MailingRecipientCreateView,
    MailingRecipientUpdateView, MailingRecipientDeleteView,
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    HomePageView, MailingAttemptsListView, toggle_mailing_activity
)
from .services import run_mailing

app_name = MailingConfig.name

urlpatterns = [
    # URL-адреса для получателей
    path('recipients/', MailingRecipientListView.as_view(), name='recipients'),
    path('recipient/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient'),
    path('recipients/create/', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/update/', MailingRecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='recipient_delete'),

    # URL-адреса для сообщений
    path('messages/', MessageListView.as_view(), name='messages'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # URL-адреса для рассылок
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    # URL-адрес для запуска рассылки по требованию
    path('mailing/<int:pk>/run/', run_mailing, name='run_mailing'),

    # Главная страница
    path('home/', HomePageView.as_view(), name='home'),
    # URL-адрес для статистики попыток рассылок
    path('mailing-attempts/', MailingAttemptsListView.as_view(), name='mailing_attempts'),
path('toggle_activity/<int:pk>/', toggle_mailing_activity, name='toggle_mailing_activity'),
]