# Job Board Platform

A REST-style backend for a job board, built with Django and SQLite for the CodeAlpha Backend Development internship. Employers post jobs, candidates upload resumes and apply, and employers track and update application statuses.

## Features
- Employer and candidate accounts (chosen at signup), with session-based login
- Employers can post jobs
- Anyone can browse open jobs and filter by keyword, location and job type
- Candidates can upload a resume (PDF, DOC or DOCX, max 5 MB)
- Candidates can apply for jobs (one application per job, resume required) and track their status
- Employers can view applicants for their own jobs and update each status (pending, reviewed, accepted, rejected)
- Role checks: candidates cannot post jobs, and employers cannot apply or see other employers' applications
- Django admin panel for managing all data

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Endpoints
| Method | Path | Who | Description |
|---|---|---|---|
| POST | `/signup/` | anyone | Create an account with `username`, `password`, `role` (`employer` or `candidate`) and `company_name` or `full_name` |
| POST | `/login/` | anyone | Log in with `username` and `password` |
| GET | `/jobs/` | anyone | List open jobs; filters: `?search=`, `?location=`, `?job_type=` |
| GET | `/jobs/<id>/` | anyone | Job details |
| POST | `/jobs/post/` | employer | Post a job (`title`, `description`, `location`, optional `job_type`) |
| POST | `/resume/` | candidate | Upload a resume as multipart form field `resume` |
| POST | `/jobs/<id>/apply/` | candidate | Apply for a job |
| GET | `/applications/` | candidate | List your applications and their statuses |
| GET | `/jobs/<id>/applications/` | employer | List applicants for one of your jobs |
| POST | `/applications/<id>/status/` | employer | Update status with `{"status": "accepted"}` |

## Example
```
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/signup/ -ContentType "application/json" -Body '{"username": "ama", "password": "StrongPass123", "role": "candidate", "full_name": "Ama Mensah"}'
```

## Models
- **Employer:** linked to a user, with a company name
- **Job:** belongs to an employer (title, description, location, type, open or closed)
- **Candidate:** linked to a user, with a name and an optional resume file
- **Application:** links a candidate to a job with a status (unique per candidate and job)

## Tech
Python, Django, SQLite