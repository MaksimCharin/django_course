from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "example@email.com"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваш пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"}
        )
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваш email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваш пароль"}
        )

        self.fields["username"].label = "Email адрес"
        self.fields["password"].label = "Пароль"


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ваш Email"}
        )
        self.fields["email"].label = "Email-адрес"


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите новый пароль"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите новый пароль"}
        )

        self.fields["new_password1"].label = "Новый пароль"
        self.fields["new_password2"].label = "Повторите пароль"


class UserProfileForm(forms.ModelForm):
    """ Форма для редактирования профиля пользователя """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'avatar', 'phone_number', 'country')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'Ваш Email', 'readonly': 'readonly'}),
            # Можно сделать только для чтения
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Например, 79XXXXXXXXX', 'pattern': '[0-9]{11}'}),
            # Добавляем паттерн для 11 цифр
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например, Россия'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone_number': 'Номер телефона',
            'country': 'Страна',
            'avatar': 'Фото профиля',
        }
        help_texts = {
            'phone_number': 'Введите 11 цифр без пробелов и символов. Например, 79123456789.',
            'avatar': 'Загрузите изображение для вашего профиля.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['email'].disabled = True

        for field_name, field in self.fields.items():
            if isinstance(field.widget, (
            forms.TextInput, forms.EmailInput, forms.NumberInput, forms.URLInput, forms.PasswordInput, forms.Textarea,
            forms.FileInput, forms.Select)):
                field.widget.attrs['class'] = 'form-control'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            if 'placeholder' not in field.widget.attrs and field.label:
                field.widget.attrs['placeholder'] = field.label
