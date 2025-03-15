from .models import Service, Doctor, AboutPage, ContactInfo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm, SupportForm
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    services = Service.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'main/home.html', {'services': services, 'doctors': doctors})


def about(request):
    about_items = AboutPage.objects.all().order_by('id')
    doctors = Doctor.objects.all()
    return render(request, 'main/about.html', {
        'about_items': about_items,
        'doctors': doctors,
    })


def contacts(request):
    contact = ContactInfo.objects.first()
    return render(request, 'main/contacts.html', {'contact': contact})


def services(request):
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'main/service_detail.html', {'service': service})


def doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'main/doctors.html', {'doctors': doctors})


@login_required
def make_appointment(request):
    preselected_service = None
    service_id = request.GET.get('service')
    if service_id:
        preselected_service = get_object_or_404(Service, pk=service_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, preselected_service=preselected_service)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('dashboard')
    else:
        form = AppointmentForm(preselected_service=preselected_service)
    return render(request, 'main/make_appointment.html', {'form': form})


def support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            message = form.cleaned_data['message']

            subject = f"Сообщение поддержки от {first_name} {last_name}"
            message_body = f"Пользователь: {first_name} {last_name}\n\nСообщение:\n{message}"

            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.SUPPORT_EMAIL]
            )
            return redirect('support_success')
    else:
        form = SupportForm()
    return render(request, 'main/support.html', {'form': form})


def support_success(request):
    return render(request, 'main/support_success.html')
