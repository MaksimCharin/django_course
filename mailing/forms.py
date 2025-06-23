from django import forms
from .models import MailingRecipient, Message, Mailing


class MailingRecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['email', 'full_name', 'comment']

    def __init__(self, *args, **kwargs):
        super(MailingRecipientForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите Ф.И.О. клиента'})
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'placeholder': 'example@email.com'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                    'rows': "4", 'placeholder':
                                                        'Введите комментарий (описание) по данному клиенту'})


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['email_subject', 'email_body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['email_subject'].widget.attrs.update({'class': 'form-control',
                                                            'placeholder': 'Введите тему сообщения '})
        self.fields['email_body'].widget.attrs.update({'class': 'form-control', 'id': "exampleFormControlTextarea1",
                                                         'rows': "4", 'placeholder': 'Введите текст сообщения'})



class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients']

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-select form-select-sm',
                                                    'aria-label': 'Small select example'})
        self.fields['recipients'].widget.attrs.update({'class': 'form-select form-select-sm',
                                                      'aria-label': 'Small select example'})