from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
import datetime


def get_time_choices():
    choices = []
    start = datetime.datetime.strptime("10:00", "%H:%M")
    end = datetime.datetime.strptime("20:00", "%H:%M")
    while start <= end:
        time_str = start.time().strftime("%H:%M")
        choices.append((time_str, time_str))
        start += datetime.timedelta(minutes=30)
    return choices


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(required=False, label="Номер телефона")
    address = forms.CharField(required=False, label="Адрес", widget=forms.Textarea)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address', 'password1', 'password2']
