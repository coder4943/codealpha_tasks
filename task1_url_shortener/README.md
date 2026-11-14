# CodeAlpha URL Shortener

A simple URL shortener built with Django and SQLite for the CodeAlpha Backend Development internship.

## Features
- Accepts a long URL and generates a unique 6-character short code
- Stores each code and its original URL in a database
- Redirects visitors from the short link to the original URL
- Returns a 404 for unknown codes

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usage

Create a short link (PowerShell):
```
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/shorten/ -ContentType "application/json" -Body '{"url": "https://github.com"}'
```

The response contains the short code and the full short URL. Visit the short URL in a browser to be redirected.

## Endpoints
| Method | Path | Description |
|---|---|---|
| POST | `/shorten/` | Create a short link from `{"url": "..."}` |
| GET | `/<code>/` | Redirect to the original URL |

## Tech
Python, Django, SQLite