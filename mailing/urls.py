from django.urls import path
from mailing.apps import MailingConfig
from .views import (MailingRecipientListView,MailingRecipientDetailView, MailingRecipientCreateView,
                    MailingRecipientUpdateView, MailingRecipientDeleteView, MessageListView, MessageDetailView,
                    MessageCreateView, MessageUpdateView, MessageDeleteView)

app_name = MailingConfig.name

urlpatterns = [
    path('recipients/', MailingRecipientListView.as_view(), name='recipients'),
    path('recipient/<int:pk>/', MailingRecipientDetailView.as_view(), name='recipient'),
    path('recipients/create/', MailingRecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/update/', MailingRecipientUpdateView.as_view(), name='recipient_update'),
    path('recipients/<int:pk>/delete/', MailingRecipientDeleteView.as_view(), name='recipient_delete'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),


]
