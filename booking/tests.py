from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import FitnessClass, Booking
import pytz
from datetime import timedelta


class FitnessClassBookingTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.class1 = FitnessClass.objects.create(
            name="Yoga Class",
            instructor="Alice",
            start_time=timezone.now() + timedelta(days=1),
            available_slots=5
        )

        self.class2 = FitnessClass.objects.create(
            name="Cardio Blast",
            instructor="Bob",
            start_time=timezone.now() + timedelta(days=2),
            available_slots=0
        )

    def test_get_classes_with_valid_timezone(self):
        response = self.client.get('/classes/', {'timezone': 'Asia/Kolkata'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_get_classes_with_invalid_timezone(self):
        response = self.client.get('/classes/', {'timezone': 'Invalid/Zone'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_successful_booking(self):
        data = {
            "fitness_class": self.class1.name,
            "client_name": "John Doe",
            "client_email": "john@yopmail.com"
        }
        response = self.client.post('/book/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('booking_id', response.data)

        # Check if available slots decreased
        self.class1.refresh_from_db()
        self.assertEqual(self.class1.available_slots, 4)

    def test_booking_with_no_slots_available(self):
        data = {
            "fitness_class": self.class2.name,
            "client_name": "Virat Kohli",
            "client_email": "virat@yopmail.com"
        }
        response = self.client.post('/book/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)

    def test_booking_list_for_email(self):
        # Create a booking first
        booking = Booking.objects.create(
            fitness_class=self.class1,
            client_name="Test User",
            client_email="user@yopmail.com"
        )
        response = self.client.get('/bookings/', {'email': 'user@yopmail.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertIn('data', response.data)

    def test_booking_list_without_email_param(self):
        response = self.client.get('/bookings/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
