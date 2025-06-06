from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from booking.utils import CustomLogger, validate_timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

logger = CustomLogger(__name__).get_custom_logger()


class ClassListView(APIView):
    """
    GET /classes/?timezone=Asia/Kolkata
    Returns upcoming fitness classes converted to the requested timezone.
    """

    def get(self, request):
        tz_name = request.GET.get('timezone', 'Asia/Kolkata')

        try:
            tz_name = validate_timezone(tz_name)
        except ValidationError:
            return Response({"error": "Invalid timezone"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            now_utc = timezone.now()
            upcoming_classes = FitnessClass.objects.filter(start_time__gte=now_utc).order_by('start_time')

            serializer = FitnessClassSerializer(upcoming_classes, many=True, context={'timezone': tz_name})
            logger.info(f"Returned {len(upcoming_classes)} classes for timezone {tz_name}")

            return Response({
                "message": "Classes fetched successfully for the specified timezone.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching classes for timezone: {tz_name}", exc_info=True)
            return Response({
                "message": "An error occurred while retrieving classes.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookClassView(APIView):
    """
    POST /book/
    Body: {fitness_class, client_name, client_email}
    Validates availability and creates a booking.
    """

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error(f"Invalid booking request: {serializer.errors}")
            return Response({
                "message": "Booking request is not valid.",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = serializer.save()
            logger.info(f"Booking successful for class ID {booking.fitness_class.id} by {booking.client_email}")

            return Response({
                "message": "Booking successful.",
                "booking_id": booking.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("Error occurred during booking.", exc_info=True)
            return Response({
                "message": "An error occurred while processing your booking.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingListView(APIView):
    """
    GET /bookings/?email=client@example.com
    Returns bookings made by the specified email.
    """

    def get(self, request):
        email = request.GET.get('email')
        if not email:
            logger.warning("Missing 'email' parameter in booking list request.")
            return Response({
                "message": "Email parameter is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            bookings = Booking.objects.filter(client_email__iexact=email)
            serializer = BookingSerializer(bookings, many=True)
            logger.info(f"Returned {len(bookings)} bookings for email {email}")

            return Response({
                "message": "Bookings details fetched successfully.",
                "count": len(bookings),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching bookings for email {email}", exc_info=True)
            return Response({
                "message": "An error occurred while retrieving bookings.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
