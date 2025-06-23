from django.urls import reverse_lazy

from .forms import MailingRecipientForm
from .models import MailingRecipient
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

