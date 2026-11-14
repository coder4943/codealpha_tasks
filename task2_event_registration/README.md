# Event Registration System

A REST-style backend for managing events and user registrations, built with Django and SQLite for the CodeAlpha Backend Development internship.

## Features
- View a list of events and the details of a single event
- User signup and login (session-based)
- Register for an event while logged in
- View and cancel your own registrations
- Prevents duplicate registrations and registrations beyond an event's capacity
- Django admin panel for organizers to create and manage events

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create events at `http://127.0.0.1:8000/admin/`.

## Endpoints
| Method | Path | Description |
|---|---|---|
| GET | `/events/` | List all events |
| GET | `/events/<id>/` | Event details |
| POST | `/signup/` | Create an account with `{"username": "...", "password": "..."}` |
| POST | `/login/` | Log in with the same fields |
| POST | `/events/<id>/register/` | Register the logged-in user for an event |
| GET | `/registrations/` | List the logged-in user's registrations |
| DELETE | `/registrations/<id>/cancel/` | Cancel one of your registrations |

## Models
- **Event:** title, description, location, date, capacity
- **Registration:** links a user to an event (unique per user and event)

## Tech
Python, Django, SQLite