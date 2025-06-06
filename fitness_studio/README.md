# Fitness Studio API

A RESTful API built with Django REST Framework for managing fitness classes and bookings. Clients can view upcoming classes, book slots, and retrieve their booking history.

---

## Features

- View upcoming fitness classes (with timezone support)
- Book a class (with slot availability validation)
- View bookings by client email

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite (default, can be configured)

---

## Setup Instructions

### 1. Clone the repository

git clone https://github.com/jharohit030/fitness_studio.git
cd fitness_studio

### 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt


### 4. Apply migrations
python manage.py makemigrations booking
python manage.py migrate

### 5. Create a superuser (optional, for admin access)
python manage.py createsuperuser

### 6. For load the classes data in db run script:
python manage.py seed_data

### 7. Run the development server
python manage.py runserver


## API Endpoints

1.  Get Upcoming Classes

    GET /classes/?timezone=Asia/Kolkata

    Returns upcoming classes in the specified timezone.

    Default timezone: Asia/Kolkata

    postman curl: 
        curl --location 'http://127.0.0.1:8000/classes/'


2. Book a Class

    POST /book/

    postman_curl:
        curl --location 'http://127.0.0.1:8000/book/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "fitness_class": "Strength Train",
            "client_name": "Aman",
            "client_email": "aman@yopmail.com"
        }'


3. Get Bookings by Email

    GET /bookings/?email=gaurav@yopmail.com

    Returns all bookings made by the client.

    postman_curl:
        curl --location 'http://127.0.0.1:8000/bookings/?email=jharohit03071%40gmail.com'


## Running Tests

Run unit tests using:
    python manage.py test

Tests are isolated using a temporary database.
No test data persists after the tests complete.

## Project Structure


fitness_studio/
├── booking/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── utils.py
│   └── tests.py
├── fitness_studio/
│   ├── settings.py
│   ├── urls.py
├── manage.py
└── README.md


## Timezone Support

The API supports conversion of class start_time to any valid IANA Timezone.

Example: Asia/Kolkata, America/New_York, Europe/London