from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment, name='update_appointment'),
]
