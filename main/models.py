from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='services/', verbose_name="Фотография услуги", blank=True, null=True)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    photo = models.ImageField(upload_to='doctors/', verbose_name="Фотография доктора", blank=True, null=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    date = models.DateField(verbose_name="Дата приёма")
    time = models.TimeField(verbose_name="Время приёма")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.doctor.name} | {self.date} {self.time}"
