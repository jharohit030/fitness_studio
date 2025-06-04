import logging
from django.conf import settings
from datetime import datetime as dt
import os
import pytz
from rest_framework.exceptions import ValidationError
from django.utils.timezone import is_naive, make_aware



class CustomLogger:
    def __init__(self, name):
        self.name = name

    def get_custom_logger(self):
        log_dir = str(settings.LOGS_DIR) + '/logs/' + str(((dt.today()).strftime('%Y-%m-%d')))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(filename=log_dir + '/logs.txt',
                            format='%(asctime)s %(process)d %(thread)s %(levelname)2s '
                                   '%(pathname)s %(funcName)s %(lineno)d %(message)s',
                            level=logging.INFO)
        logger = logging.getLogger(name=self.name)
        logger.addHandler(logging.StreamHandler())
        return logger


def validate_timezone(tz_name: str = 'Asia/Kolkata'):
    try:
        pytz.timezone(tz_name)
        return tz_name
    except pytz.UnknownTimeZoneError:
        raise ValidationError("Invalid timezone specified.")
    

def convert_to_timezone(dt, tz_name):
    """
        Convert datetime `dt` to the given timezone, assuming IST base if naive.
    """
    target_tz = pytz.timezone(tz_name)
    if is_naive(dt):
        dt = make_aware(dt, pytz.timezone('Asia/Kolkata'))
    return dt.astimezone(target_tz)
