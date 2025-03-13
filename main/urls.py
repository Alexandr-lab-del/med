from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('services/', views.services, name='services'),
    path('make_appointment/', views.make_appointment, name='make_appointment'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('doctors/', views.doctors, name='doctors'),
    path('support/', views.support, name='support'),
    path('support/success/', views.support_success, name='support_success'),
]
