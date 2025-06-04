from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import pytz
from booking.utils import CustomLogger, validate_timezone
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer


logger = CustomLogger(__name__).get_custom_logger()

class ClassListView(APIView):
    """
    GET /classes/?timezone=Asia/Kolkata
    Returns upcoming fitness classes converted to requested timezone.
    """

    def get(self, request):
        try:
            tz_name = request.GET.get('timezone', 'Asia/Kolkata')
            try:
                tz_name = validate_timezone(tz_name)
            except pytz.UnknownTimeZoneError:
                return Response({"error": "Invalid timezone"}, status=status.HTTP_400_BAD_REQUEST)

            now_ist = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
            classes = FitnessClass.objects.filter(start_time__gte=now_ist).order_by('start_time')
            serializer = FitnessClassSerializer(classes, many=True, context={'timezone': tz_name})

            logger.info(f"Returned {len(classes)} classes for timezone {tz_name}")
            return Response({
                "message": "Classes fetched successful for the specified timezone.",
                "response": serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error occurred fetching classes for specified timezone: {tz_name} ", exc_info=True)
            return Response({
                "message": "An error occurred while retrieving classes.",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BookClassView(APIView):
    """
    POST /book/
    Body: {fitness_class, client_name, client_email}
    Validates availability and creates a booking.
    """

    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            if not serializer.is_valid():
                logger.error(f"Booking request is not valid: {serializer.errors}")
                error_dict = {field: error[0] for field, error in serializer.errors.items()}
                return Response({
                    "message": "Booking request is not valid.",
                    "errors": error_dict
                }, status=status.HTTP_400_BAD_REQUEST)

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
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookingListView(APIView):
    """
    GET /bookings/?email=rohit@yopmail.com
    Returns bookings made by the given email.
    """

    def get(self, request):
        try:
            email = request.GET.get('email')
            if not email:
                logger.warning("Missing 'email' parameter in booking list request.")
                return Response({"message": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

            bookings = Booking.objects.filter(client_email=email)
            serializer = BookingSerializer(bookings, many=True)
            logger.info(f"Returned {len(bookings)} bookings for email {email}")
            return Response({
                "message": "Bookings fetched successfully.",
                "count": len(bookings),
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error occurred fetching bookings for email {email}: {str(e)}", exc_info=True)
            return Response({
                "message": "An error occurred while retrieving bookings.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
