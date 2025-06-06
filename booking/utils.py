import logging
from django.conf import settings
from datetime import datetime as dt
import os
import pytz
from rest_framework.exceptions import ValidationError
from django.utils.timezone import make_aware


class CustomLogger:

    def __init__(self, name):
        self.name = name

    def get_custom_logger(self):
        log_dir = str(settings.LOGS_DIR) + '/logs/' + \
            str(((dt.today()).strftime('%Y-%m-%d')))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(filename=log_dir + '/logs.txt',
                            format='%(asctime)s %(process)d %(thread)s %(levelname)2s '
                                   '%(pathname)s %(funcName)s %(lineno)d %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger(name=self.name)
        logger.addHandler(logging.StreamHandler())
        return logger


def validate_timezone(tz_name: str = 'Asia/Kolkata') -> str:
    """
    Validates if a given timezone name is valid. Defaults to Asia/Kolkata.
    """
    try:
        pytz.timezone(tz_name)
        return tz_name
    except pytz.UnknownTimeZoneError:
        raise ValidationError("Invalid timezone specified.")

def convert_to_timezone(dt, tz_name='Asia/Kolkata'):
    """
    Converts a UTC datetime to the given timezone.
    """
    if dt is None:
        return None
    # Ensure datetime is timezone-aware (assume UTC if naive)
    if dt.tzinfo is None:
        dt = make_aware(dt)

    target_tz = pytz.timezone(tz_name)
    return dt.astimezone(target_tz)

