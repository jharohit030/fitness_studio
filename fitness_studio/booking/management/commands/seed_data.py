import pandas as pd
from django.core.management.base import BaseCommand
from booking.models import FitnessClass
import pytz
import os
from booking.utils import CustomLogger

logger = CustomLogger(__name__).get_custom_logger()


class Command(BaseCommand):
    help = 'Import fitness classes from an Excel file using bulk create.'

    def handle(self, *args, **kwargs):
        excel_path = "booking/script_data/classes_data.xlsx"

        if not os.path.exists(excel_path):
            logger.error(f"File not found: {excel_path}")
            return

        try:
            df = pd.read_excel(excel_path)

            required_columns = {'Class Name', 'Start Time', 'Instructor', 'Available Slots'}
            if not required_columns.issubset(df.columns):
                logger.error(f"Missing required columns. Required: {required_columns}")
                return

            class_objects = []
            for _, row in df.iterrows():
                try:
                    ist_time = pd.to_datetime(row['Start Time'])
                    utc_time = ist_time.tz_localize('Asia/Kolkata').astimezone(pytz.UTC)

                    class_objects.append(
                        FitnessClass(
                            name=row['Class Name'],
                            start_time=utc_time,
                            instructor=row['Instructor'],
                            available_slots=int(row['Available Slots'])
                        )
                    )
                except Exception as e:
                    logger.error(f"Skipping row due to error: {str(e)}")

            if class_objects:
                FitnessClass.objects.bulk_create(class_objects)
                logger.info(f"{len(class_objects)} classes imported successfully.")
            else:
                logger.warning("No valid rows to import.")

        except Exception as e:
            logger.error(f"Error while reading Excel file: {e}")
