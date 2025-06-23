from django import forms
from .models import MailingRecipient


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

