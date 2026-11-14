import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Event, Registration


def event_to_dict(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "location": event.location,
        "date": event.date.isoformat(),
        "capacity": event.capacity,
    }


def event_list(request):
    events = Event.objects.all().order_by("date")
    return JsonResponse({"events": [event_to_dict(e) for e in events]})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return JsonResponse(event_to_dict(event))


@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return JsonResponse({"error": "username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)

    User.objects.create_user(username=username, password=password)
    return JsonResponse({"message": "Account created", "username": username}, status=201)

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    user = authenticate(
        request,
        username=data.get("username"),
        password=data.get("password"),
    )
    if user is None:
        return JsonResponse({"error": "Invalid username or password"}, status=401)

    login(request, user)
    return JsonResponse({"message": "Logged in", "username": user.username})

@csrf_exempt
def register_for_event(request, event_id):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    event = get_object_or_404(Event, id=event_id)

    if Registration.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({"error": "Already registered"}, status=400)

    if Registration.objects.filter(event=event).count() >= event.capacity:
        return JsonResponse({"error": "Event is full"}, status=400)

    registration = Registration.objects.create(user=request.user, event=event)
    return JsonResponse(
        {"message": "Registered", "registration_id": registration.id, "event": event.title},
        status=201,
    )

def my_registrations(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    registrations = Registration.objects.filter(user=request.user).select_related("event")
    data = [
        {
            "registration_id": r.id,
            "event": event_to_dict(r.event),
            "registered_at": r.registered_at.isoformat(),
        }
        for r in registrations
    ]
    return JsonResponse({"registrations": data})


@csrf_exempt
def cancel_registration(request, registration_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Use DELETE"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    registration = get_object_or_404(
        Registration, id=registration_id, user=request.user
    )
    registration.delete()
    return JsonResponse({"message": "Registration cancelled"})