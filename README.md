# CodeAlpha Backend Development Tasks

Submission for the CodeAlpha Backend Development internship (October batch). All three projects are built with Python, Django and SQLite. Each folder has its own README with setup steps and API documentation.

| Task | Folder | Description |
|---|---|---|
| Task 1 | [task1_url_shortener](task1_url_shortener) | Shortens long URLs, stores the mapping in a database, and redirects short links to the original URL |
| Task 2 | [task2_event_registration](task2_event_registration) | Event listing and details, user signup and login, event registration, and viewing or cancelling registrations |
| Task 4 | [task4_job_board](task4_job_board) | Employer and candidate accounts, job posting and search filters, resume upload, applications and status tracking |

## Running a project
Open a task folder and follow the **Setup** section of its README. In short:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Author
Francis Ampofo Kwarteng