from django.urls import path
from .views import (
    MailingRecipientListView, MailingRecipientDetailView, MailingRecipientCreateView, MailingRecipientUpdateView,
    MailingRecipientDeleteView,
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView,
    MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView,
    MailingAttemptsListView, HomePageView, toggle_mailing_activity, UserListManagerView, toggle_user_active_status
)
from .services import run_mailing

app_name = 'mailing'

urlpatterns = [
    # Главная страница
    path('', HomePageView.as_view(), name='home'),

    # Пути для получателей (клиентов)
    path('recipients/', MailingRecipientListView.as_view(), name='recipients'),
    path('recipients/create/', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/<int:pk>/update/', MailingRecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='recipient_delete'),

    # Пути для сообщений
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    # Пути для рассылок
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/run/', run_mailing, name='run_mailing'),
    path('mailings/<int:pk>/toggle_activity/', toggle_mailing_activity, name='toggle_mailing_activity'),

    # Путь для статистики попыток
    path('attempts/', MailingAttemptsListView.as_view(), name='mailing_attempts'),

    path('manager/users/', UserListManagerView.as_view(), name='user_list_manager'),
    path('manager/users/<int:pk>/toggle-active/', toggle_user_active_status, name='toggle_user_active_status'),
]
