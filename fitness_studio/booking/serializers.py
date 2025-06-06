from rest_framework import serializers
from .models import FitnessClass, Booking
from booking.utils import convert_to_timezone


class FitnessClassSerializer(serializers.ModelSerializer):
    start_time = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'start_time', 'instructor', 'available_slots']

    def get_start_time(self, obj):
        tz_name = self.context.get('timezone', 'Asia/Kolkata')
        dt = convert_to_timezone(obj.start_time, tz_name)
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z')


class BookingSerializer(serializers.ModelSerializer):
    fitness_class = serializers.SlugRelatedField(
        slug_field='name',
        queryset=FitnessClass.objects.all()
    )
    class Meta:
        model = Booking
        fields = ['id', 'fitness_class', 'client_name', 'client_email', 'booked_at']
        read_only_fields = ['id', 'booked_at']

    def validate(self, data):
        fitness_class = data['fitness_class']
        if fitness_class.available_slots < 1:
            raise serializers.ValidationError("No available slots for this class.")
        return data

    def create(self, validated_data):
        fitness_class = validated_data['fitness_class']
        fitness_class.available_slots -= 1
        fitness_class.save()
        return super().create(validated_data)
