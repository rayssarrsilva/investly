from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, user_logout, dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login2/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login2'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
]