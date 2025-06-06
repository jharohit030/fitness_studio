from django.contrib import admin
from booking.models import FitnessClass, Booking

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'instructor', 'available_slots', 'created_at')
    search_fields = ('name', 'instructor')
    list_filter = ('start_time', 'instructor')
    ordering = ('-start_time',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'fitness_class', 'booked_at')
    search_fields = ('client_name', 'client_email', 'fitness_class__name')
    list_filter = ('fitness_class', 'booked_at')
    ordering = ('-booked_at',)
