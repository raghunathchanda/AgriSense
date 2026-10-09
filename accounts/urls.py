from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import never_cache
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', never_cache(LoginView.as_view(template_name='accounts/login.html')), name='login'),
    path('logout/', never_cache(LogoutView.as_view()), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]