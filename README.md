# OJAS 2026 — BIT Durg

Django backend + standalone frontend, built from the PDF reference.
Campus photo (building + palms + grass you sent) is used **as the page background**.

## Layout

```
ojus/
  backend/                  Django project (all backend here)
    manage.py
    requirements.txt
    ojas_backend/           settings / urls / wsgi / asgi
    core/                   models, views, urls, admin, forms, seed command
    templates/core/         index.html (Django template)
    static/core/            styles.css, script.js, img/campus.jpg  <-- put photo here
  frontend/                 standalone site (all frontend here)
    index.html, styles.css, script.js
    assets/campus.jpg       <-- put photo here
  fontend/                  mirror of frontend/ (you had this typo folder; kept in sync)
  requirements.txt          root pip requirements (same as backend)
```

## Campus photo as background (important)

Chat images can't be written to disk by me, so save it once manually:

1. Save the photo you sent as `campus.jpg`
2. Copy to `backend/static/core/img/campus.jpg`
3. Copy to `frontend/assets/campus.jpg`

CSS already points there with a dark overlay for readability:
`linear-gradient(rgba(5,7,15,.62),...) + url(...)`, `background-size: cover; attachment: fixed`.

## Run backend (Windows)

```powershell
cd "C:\Users\my pc\ojus\backend"
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py seed_ojas
py manage.py runserver
```

Open http://127.0.0.1:8000/ — full OJAS site (events, clubs, schedule,
gallery, winners, updates, help desk, FAQ, register, feedback).

Admin: `py manage.py createsuperuser` then /admin/.

## Run frontend only (no Django)

Just open `frontend/index.html` in a browser.
If Django runs on :8000, cards/forms go live via fetch; otherwise built-in
fallback data is shown.

## API (JSON, no DRF needed)

- GET /api/updates/  — What's New cards (the "updates" requirement)
- GET /api/events/ /api/clubs/ /api/schedule/ /api/faqs/
- POST /api/register/ {name,email,phone,club,event,message}
- POST /api/feedback/ {name,message}

## requirements.txt

Root + backend both contain:

```
Django>=4.2,<5.2
whitenoise>=6.6
gunicorn>=21.2
```

Install: `py -m pip install -r requirements.txt`
