from rest_framework import serializers
from .models import FitnessClass, Booking
import pytz
from booking.utils import convert_to_timezone, validate_timezone


class FitnessClassSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'start_time', 'instructor', 'available_slots']

    def get_start_time(self, obj):
        tz_name = self.context.get('timezone', 'Asia/Kolkata')
        try:
            return convert_to_timezone(obj.start_time, tz_name).isoformat()
        except Exception:
            # Fallback to IST if timezone fails
            return convert_to_timezone(obj.start_time, 'Asia/Kolkata').isoformat()
        
class BookingSerializer(serializers.ModelSerializer):
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.all())

    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booked_at']
        read_only_fields = ['id', 'booked_at']

    def validate_fitness_class(self, data):
        fitness_class = data['fitness_class']
        if fitness_class.available_slots < 1:
            raise serializers.ValidationError("No available slots for this class.")
        return data
    
    def validate_client_email(self, value):
        if not value or '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value

    def create(self, validated_data):
        fitness_class = validated_data['fitness_class']
        fitness_class.available_slots -= 1
        fitness_class.save()
        return super().create(validated_data)
