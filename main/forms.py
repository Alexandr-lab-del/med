from django import forms
from django.core.exceptions import ValidationError
from .models import Appointment
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


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(choices=get_time_choices()),
        }

    def __init__(self, *args, **kwargs):
        preselected_service = kwargs.pop('preselected_service', None)
        super().__init__(*args, **kwargs)
        if preselected_service:
            self.fields['service'].initial = preselected_service.pk
            self.fields['service'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        service = cleaned_data.get('service')
        doctor = cleaned_data.get('doctor')

        if date and time and service:
            qs = Appointment.objects.filter(date=date, time=time, service=service, doctor=doctor)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("Запись на данное время уже существует. Пожалуйста, выберите другой слот.")
        return cleaned_data


class SupportForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=50)
    last_name = forms.CharField(label="Фамилия", max_length=50)
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)
