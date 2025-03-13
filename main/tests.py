from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
import datetime

from main.models import Service, Doctor, Appointment

User = get_user_model()


class MainViewsTests(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.make_appointment_url = reverse('make_appointment')
        self.support_url = reverse('support')
        self.support_success_url = reverse('support_success')
        self.user_password = "testpassword123"

        self.doctor = Doctor.objects.create(
            name="Dr. Main",
            specialization="Cardiology"
        )
        self.service = Service.objects.create(
            title="Cardio Check-up",
            price=150.00
        )

        self.user = User.objects.create_user(
            username="mainuser",
            password=self.user_password
        )

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('services', response.context)
        self.assertIn('doctors', response.context)

    def test_make_appointment_get(self):
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.get(self.make_appointment_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_make_appointment_post(self):
        self.client.login(username=self.user.username, password=self.user_password)
        appointment_date = datetime.date.today() + datetime.timedelta(days=3)
        data = {
            'service': self.service.id,
            'doctor': self.doctor.id,
            'date': appointment_date.strftime("%Y-%m-%d"),
            'time': '10:00',
        }
        response = self.client.post(self.make_appointment_url, data)
        dashboard_url = reverse('dashboard')
        self.assertRedirects(response, dashboard_url)
        self.assertTrue(
            Appointment.objects.filter(
                user=self.user,
                date=appointment_date,
                time='10:00'
            ).exists()
        )

    def test_support_post(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'message': 'Test support message',
        }
        response = self.client.post(self.support_url, data)
        self.assertRedirects(response, self.support_success_url)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('John Doe', email.subject)
        self.assertIn('Test support message', email.body)

    def test_support_get(self):
        response = self.client.get(self.support_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
