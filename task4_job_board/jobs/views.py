import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Application, Candidate, Employer, Job


def job_to_dict(job):
    return {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location,
        "job_type": job.job_type,
        "company": job.employer.company_name,
        "is_open": job.is_open,
        "created_at": job.created_at.isoformat(),
    }


def job_list(request):
    jobs = Job.objects.filter(is_open=True).select_related("employer")

    search = request.GET.get("search")
    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(description__icontains=search))

    location = request.GET.get("location")
    if location:
        jobs = jobs.filter(location__icontains=location)

    job_type = request.GET.get("job_type")
    if job_type:
        jobs = jobs.filter(job_type__iexact=job_type)

    jobs = jobs.order_by("-created_at")
    return JsonResponse({"jobs": [job_to_dict(j) for j in jobs]})


def job_detail(request, job_id):
    job = get_object_or_404(Job.objects.select_related("employer"), id=job_id)
    return JsonResponse(job_to_dict(job))

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
    role = data.get("role")

    if not username or not password:
        return JsonResponse({"error": "username and password are required"}, status=400)
    if role not in ("employer", "candidate"):
        return JsonResponse({"error": "role must be employer or candidate"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already taken"}, status=400)

    user = User.objects.create_user(username=username, password=password)

    if role == "employer":
        Employer.objects.create(user=user, company_name=data.get("company_name") or username)
    else:
        Candidate.objects.create(user=user, full_name=data.get("full_name") or username)

    return JsonResponse({"message": "Account created", "username": username, "role": role}, status=201)


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
def post_job(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        return JsonResponse({"error": "Only employers can post jobs"}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    title = data.get("title")
    description = data.get("description")
    location = data.get("location")
    if not title or not description or not location:
        return JsonResponse(
            {"error": "title, description and location are required"}, status=400
        )

    job = Job.objects.create(
        employer=employer,
        title=title,
        description=description,
        location=location,
        job_type=data.get("job_type", "full-time"),
    )
    return JsonResponse(job_to_dict(job), status=201)

@csrf_exempt
def upload_resume(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        return JsonResponse({"error": "Only candidates can upload resumes"}, status=403)

    resume = request.FILES.get("resume")
    if not resume:
        return JsonResponse({"error": "Attach a file in the 'resume' field"}, status=400)

    if not resume.name.lower().endswith((".pdf", ".doc", ".docx")):
        return JsonResponse({"error": "Only PDF, DOC or DOCX files are allowed"}, status=400)

    if resume.size > 5 * 1024 * 1024:
        return JsonResponse({"error": "File must be under 5 MB"}, status=400)

    candidate.resume = resume
    candidate.save()
    return JsonResponse({"message": "Resume uploaded", "resume": candidate.resume.name})

@csrf_exempt
def apply_for_job(request, job_id):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        return JsonResponse({"error": "Only candidates can apply"}, status=403)

    job = get_object_or_404(Job, id=job_id, is_open=True)

    if not candidate.resume:
        return JsonResponse({"error": "Upload a resume before applying"}, status=400)

    if Application.objects.filter(candidate=candidate, job=job).exists():
        return JsonResponse({"error": "Already applied"}, status=400)

    application = Application.objects.create(candidate=candidate, job=job)
    return JsonResponse(
        {
            "message": "Application submitted",
            "application_id": application.id,
            "job": job.title,
            "status": application.status,
        },
        status=201,
    )

def my_applications(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        candidate = request.user.candidate
    except Candidate.DoesNotExist:
        return JsonResponse({"error": "Only candidates have applications"}, status=403)

    applications = Application.objects.filter(candidate=candidate).select_related(
        "job", "job__employer"
    )
    data = [
        {
            "application_id": a.id,
            "job": job_to_dict(a.job),
            "status": a.status,
            "applied_at": a.applied_at.isoformat(),
        }
        for a in applications
    ]
    return JsonResponse({"applications": data})

def job_applications(request, job_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        return JsonResponse({"error": "Only employers can view applications"}, status=403)

    job = get_object_or_404(Job, id=job_id, employer=employer)
    applications = Application.objects.filter(job=job).select_related("candidate")
    data = [
        {
            "application_id": a.id,
            "candidate": a.candidate.full_name,
            "resume": a.candidate.resume.url if a.candidate.resume else None,
            "status": a.status,
            "applied_at": a.applied_at.isoformat(),
        }
        for a in applications
    ]
    return JsonResponse({"job": job.title, "applications": data})


@csrf_exempt
def update_application_status(request, application_id):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Login required"}, status=401)

    try:
        employer = request.user.employer
    except Employer.DoesNotExist:
        return JsonResponse({"error": "Only employers can update status"}, status=403)

    application = get_object_or_404(
        Application, id=application_id, job__employer=employer
    )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    new_status = data.get("status")
    valid = [choice[0] for choice in Application.STATUS_CHOICES]
    if new_status not in valid:
        return JsonResponse({"error": f"status must be one of {valid}"}, status=400)

    application.status = new_status
    application.save()
    return JsonResponse({"message": "Status updated", "status": application.status})