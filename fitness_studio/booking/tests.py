from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from booking.models import FitnessClass, Booking
from django.utils import timezone
import pytz

class BookingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fitness_class = FitnessClass.objects.create(
            name='Yoga',
            start_time=timezone.now() + timezone.timedelta(days=1),
            instructor='Karan',
            available_slots=5
        )

    def test_get_classes_default_timezone(self):
        response = self.client.get(reverse('classes-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)

    def test_book_class_successfully(self):
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Rohit Jha",
            "client_email": "Rohit@yopmail.com"
        }
        response = self.client.post(reverse('book-class'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

    def test_book_class_when_full(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Rajat Singh",
            "client_email": "rajat@yopmail.com"
        }
        response = self.client.post(reverse('book-class'), data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("No slots available", str(response.data))
