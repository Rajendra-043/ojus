"""Views: server-rendered homepage + small JSON API (no DRF needed)."""
import json

from django.db.utils import OperationalError, ProgrammingError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

_DB_ERRORS = (OperationalError, ProgrammingError)


def healthz(request):
    """Render health check — no database access, never 500s on missing tables."""
    return JsonResponse({"ok": True})


def _fetch(model, *args, **kwargs):
    """list(model.objects.filter(...)) or None when the DB/table is unavailable
    (e.g. migrations haven't run in this environment yet)."""
    try:
        return list(model.objects.filter(*args, **kwargs))
    except _DB_ERRORS:
        return None

from .forms import FeedbackForm, RegistrationForm
from .models import (
    Club,
    Event,
    FAQ,
    Feedback,
    GalleryItem,
    HelpTopic,
    Registration,
    ScheduleEntry,
    Update,
    Winner,
)

# Fallback content (matches the PDF) used when the DB is still empty.
DEFAULTS = {
    "events": [
        ("Robotics", "Build robots and solve challenges."),
        ("Programming", "Coding and programming contests."),
        ("Gaming", "Gaming tournaments and challenges."),
        ("Circuit Design", "Test your electronics skills."),
        ("Singing", "Music and live performances."),
        ("Dancing", "Solo, group and freestyle dance."),
        ("Craft & Art", "Painting, drawing and creativity."),
        ("Sports", "Cricket, football, badminton and more."),
        ("Paper Presentation", "Present innovative ideas."),
    ],
    "clubs": [
        ("Vista", "Culture"), ("Innovation", "Ideas"), ("Ekaksh", "Drama"),
        ("Laasya", "Dance"), ("Alankar", "Music"), ("Speaking Club", "Communication"),
        ("Astro", "Astronomy"), ("Clicks", "Photography"), ("Techno", "Technology"),
        ("Robotics", "Robotics"), ("Quizbizz", "Quiz"), ("PAC", "Activities"),
        ("GDSC", "Development"), ("Startup", "Business"), ("Literary", "Writing"),
    ],
    "schedule": [
        ("Day 1", "Opening", "Technical Events", "Gaming"),
        ("Day 2", "Workshops", "Cultural Events", "Sports"),
        ("Day 3", "Finals", "Prize Distribution", "Closing"),
    ],
    "gallery": ["Music", "Dance", "Robotics", "Technology", "Art", "Gaming", "Awards", "Memories"],
    "winners": [
        ("Rhythm Crew", "Dance Winner"),
        ("Team Nova", "Technical Winner"),
        ("Pixel Warriors", "Gaming Winner"),
    ],
    "updates": [
        ("Registration Open", "Register for your favourite events."),
        ("New Competitions", "Explore new challenges."),
        ("Special Shows", "Enjoy performances and activities."),
    ],
    "help": [
        ("Registration Help", "Help with registration and forms."),
        ("Venue Help", "Find your event venue easily."),
        ("Technical Support", "Help with technical problems."),
        ("Volunteer Help", "Volunteers can guide you."),
        ("Emergency Help", "Contact coordinators for urgent help."),
        ("General Enquiry", "Ask the Help Desk for any query."),
    ],
    "faqs": [
        ("Who can participate?", "Students can participate according to event rules."),
        ("Can I join multiple events?", "Yes, depending on the event schedule."),
        ("How can I register?", "Fill the registration form below."),
        ("Where are events held?", "At different venues inside BIT Durg."),
        ("What if I have a problem?", "Visit the OJAS Help Desk or contact volunteers."),
    ],
}


def _qs_or_default(model, order_field="order", default_key=None, fmt=None):
    items = list(model.objects.all())
    if items:
        return items
    return [{"fallback": True, "data": row} for row in DEFAULTS[default_key]] if fmt == "raw" else DEFAULTS[default_key]


def index(request):
    events = _fetch(Event) or [
        {"name": n, "description": d, "icon": "\U0001F3AF"} for n, d in DEFAULTS["events"]
    ]
    clubs = _fetch(Club) or [
        {"name": n, "category": c, "icon": "\U0001F91D"} for n, c in DEFAULTS["clubs"]
    ]
    schedule = _fetch(ScheduleEntry) or [
        {"day": d, "morning": m, "afternoon": a, "evening": e}
        for d, m, a, e in DEFAULTS["schedule"]
    ]
    gallery = _fetch(GalleryItem) or [
        {"title": t, "icon": "\U0001F4F8"} for t in DEFAULTS["gallery"]
    ]
    winners = _fetch(Winner) or [
        {"team_name": t, "category": c} for t, c in DEFAULTS["winners"]
    ]
    updates = _fetch(Update, is_active=True) or [
        {"title": t, "description": d, "icon": "\U0001F4E3"} for t, d in DEFAULTS["updates"]
    ]
    help_topics = _fetch(HelpTopic) or [
        {"title": t, "description": d, "icon": "\U0001F198"} for t, d in DEFAULTS["help"]
    ]
    faqs = _fetch(FAQ) or [
        {"question": q, "answer": a} for q, a in DEFAULTS["faqs"]
    ]
    context = {
        "events": events,
        "clubs": clubs,
        "schedule": schedule,
        "gallery": gallery,
        "winners": winners,
        "updates": updates,
        "help_topics": help_topics,
        "faqs": faqs,
        "reg_form": RegistrationForm(),
        "fb_form": FeedbackForm(),
    }
    return render(request, "core/index.html", context)


def _serialize(qs, fields):
    return [{f: getattr(o, f) for f in fields} for o in qs]


def api_updates(request):
    updates = _fetch(Update, is_active=True)
    if not updates:
        data = [{"id": 0, "title": t, "description": d, "icon": "\U0001F4E3"} for t, d in DEFAULTS["updates"]]
    else:
        data = _serialize(updates, ["id", "title", "description", "icon"])
    return JsonResponse({"updates": data})


def api_events(request):
    events = _fetch(Event)
    if not events:
        data = [{"id": 0, "name": n, "description": d} for n, d in DEFAULTS["events"]]
    else:
        data = _serialize(events, ["id", "name", "description"])
    return JsonResponse({"events": data})


def api_clubs(request):
    clubs = _fetch(Club)
    if not clubs:
        data = [{"id": 0, "name": n, "category": c} for n, c in DEFAULTS["clubs"]]
    else:
        data = _serialize(clubs, ["id", "name", "category"])
    return JsonResponse({"clubs": data})


def api_schedule(request):
    rows = _fetch(ScheduleEntry)
    if not rows:
        data = [{"day": d, "morning": m, "afternoon": a, "evening": e} for d, m, a, e in DEFAULTS["schedule"]]
    else:
        data = _serialize(rows, ["day", "morning", "afternoon", "evening"])
    return JsonResponse({"schedule": data})


def api_faqs(request):
    faqs = _fetch(FAQ)
    if not faqs:
        data = [{"question": q, "answer": a} for q, a in DEFAULTS["faqs"]]
    else:
        data = _serialize(faqs, ["question", "answer"])
    return JsonResponse({"faqs": data})


def _save_from_request(request, form_class):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)
        form = form_class(payload)
    else:
        form = form_class(request.POST)
    if form.is_valid():
        try:
            obj = form.save()
        except _DB_ERRORS:
            return JsonResponse(
                {"ok": False, "error": "Database unavailable — migrations have not run yet."},
                status=503,
            )
        return JsonResponse({"ok": True, "id": obj.pk})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@csrf_exempt
@require_POST
def api_register(request):
    return _save_from_request(request, RegistrationForm)


@csrf_exempt
@require_POST
def api_feedback(request):
    return _save_from_request(request, FeedbackForm)


def register_page(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            form.save()
        except _DB_ERRORS:
            return render(
                request,
                "core/index.html",
                {"reg_form": form, "fb_form": FeedbackForm(),
                 "db_error": "Registration database is unavailable — please try again later."},
                status=503,
            )
        return render(request, "core/index.html", {"reg_ok": True, "reg_form": RegistrationForm(), "fb_form": FeedbackForm()})
    return render(request, "core/index.html", {"reg_form": form, "fb_form": FeedbackForm()})
