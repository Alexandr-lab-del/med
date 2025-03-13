from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login

from main.forms import AppointmentForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Appointment


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required(login_url='/login/')
def dashboard(request):
    appointments = request.user.appointments.all().order_by('date', 'time')
    return render(request, 'accounts/dashboard.html', {'appointments': appointments})


@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Запись успешно отменена.')
        return redirect('dashboard')
    return render(request, 'accounts/cancel_appointment.html', {'appointment': appointment})


@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Время записи успешно изменено.')
            return redirect('dashboard')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'accounts/update_appointment.html', {'form': form, 'appointment': appointment})
