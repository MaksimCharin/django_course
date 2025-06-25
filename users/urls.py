from django.urls import path
from .views import RegisterView, email_verification
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'users'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html', form_class=CustomAuthenticationForm),
         name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/<str:token>/', email_verification, name='email_confirm'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mailing:home'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        form_class=CustomPasswordResetForm,
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        form_class=CustomSetPasswordForm,
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
