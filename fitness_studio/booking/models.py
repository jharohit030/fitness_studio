from django.db import models

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    available_slots = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} at {self.start_time} by {self.instructor}"

class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} booking for {self.fitness_class.name}"
