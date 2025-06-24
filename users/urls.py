from django.urls import path
from .views import RegisterView, confirm_email
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm_email/<str:uidb64>/<str:token>/', confirm_email, name='confirm_email'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', form_class=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mailing:home'), name='logout'),
]
