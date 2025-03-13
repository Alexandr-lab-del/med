from django.contrib import admin
from .models import Service, Doctor


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    fields = ('title', 'description', 'price', 'image')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    fields = ('name', 'specialization', 'photo')
