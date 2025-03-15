from django.contrib import admin
from .models import Service, Doctor, Appointment, AboutPage, ContactInfo


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    fields = ('title', 'description', 'price', 'image')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    fields = ('name', 'specialization', 'photo')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'service', 'date', 'time', 'created_at')
    list_filter = ('date', 'doctor')
    search_fields = ('user__username', 'doctor__name')


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    fields = ('title', 'content', 'image')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'address')
    fields = ('phone', 'email', 'address', 'map_embed')
