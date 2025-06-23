from django.urls import reverse_lazy

from .forms import MailingRecipientForm, MessageForm, MailingForm
from .models import MailingRecipient, Message, Mailing
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


#Контроллеры для управления получателями рассылки (список, детали, создание, обновление, удаление)
class MailingRecipientListView(ListView):
    model = MailingRecipient
    template_name = 'mailing/recipients_list.html'
    context_object_name = 'recipients'


class MailingRecipientDetailView(DetailView):
    model = MailingRecipient
    template_name = 'mailing/recipient.html'


class MailingRecipientCreateView(CreateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def form_valid(self, form):
        recipient = form.save()
        recipient.owner = self.request.user
        recipient.save()
        return super().form_valid(form)


class MailingRecipientUpdateView(UpdateView):
    model = MailingRecipient
    form_class = MailingRecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')


class MailingRecipientDeleteView(DeleteView):
    model = MailingRecipient
    context_object_name = 'recipient'
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipients')


#Контроллеры для управления сообщениями (список, детали, создание, обновление, удаление)
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/messages.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message.html'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(DeleteView):
    model = Message
    context_object_name = 'message'
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages')


#Контроллеры для управления рассылкой (список, детали, создание, обновление, удаление)
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailings.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')


class MailingDeleteView(DeleteView):
    model = Mailing
    context_object_name = 'mailing'
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')