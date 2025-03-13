from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
import datetime

from main.models import Appointment, Doctor, Service

User = get_user_model()


class AccountsViewsTests(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.dashboard_url = reverse('dashboard')
        self.password = 'testpassword123'

        self.doctor = Doctor.objects.create(
            name="Dr. Test",
            specialization="General"
        )
        self.service = Service.objects.create(
            title="Test Service",
            price=100.00
        )

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=self.password
        )
        self.appointment_date = datetime.date.today() + datetime.timedelta(days=1)
        self.appointment_time = datetime.time(hour=10, minute=0)
        self.appointment = Appointment.objects.create(
            user=self.user,
            doctor=self.doctor,
            service=self.service,
            date=self.appointment_date,
            time=self.appointment_time,
        )

    def test_register_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_register_post_valid_data(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '1234567890',
            'address': 'Test address',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, self.dashboard_url)
        new_user = User.objects.get(username='newuser')
        self.assertIsNotNone(new_user)
        self.assertTrue(new_user.check_password('strongpassword123'))

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, '/login/?next=' + self.dashboard_url)

    def test_cancel_appointment(self):
        self.client.login(username=self.user.username, password=self.password)
        cancel_url = reverse('cancel_appointment', kwargs={'appointment_id': self.appointment.id})

        response_get = self.client.get(cancel_url)
        self.assertEqual(response_get.status_code, 200)
        self.assertContains(response_get, '<form')

        response_post = self.client.post(cancel_url)
        self.assertRedirects(response_post, self.dashboard_url)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())

    def test_update_appointment(self):
        self.client.login(username=self.user.username, password=self.password)
        update_url = reverse('update_appointment', kwargs={'appointment_id': self.appointment.id})
        new_date = datetime.date.today() + datetime.timedelta(days=2)
        data = {
            'service': self.service.id,
            'doctor': self.doctor.id,
            'date': new_date.strftime("%Y-%m-%d"),
            'time': '10:30',
        }
        response = self.client.post(update_url, data)
        self.assertRedirects(response, self.dashboard_url)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.date, new_date)
        self.assertEqual(self.appointment.time.strftime("%H:%M"), "10:30")
