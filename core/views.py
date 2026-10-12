"""Views: server-rendered homepage + small JSON API (no DRF needed)."""
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
    events = list(Event.objects.all()) or [
        {"name": n, "description": d, "icon": "\u25a0"} for n, d in DEFAULTS["events"]
    ]
    clubs = list(Club.objects.all()) or [
        {"name": n, "category": c, "icon": "\u25a0"} for n, c in DEFAULTS["clubs"]
    ]
    schedule = list(ScheduleEntry.objects.all()) or [
        {"day": d, "morning": m, "afternoon": a, "evening": e}
        for d, m, a, e in DEFAULTS["schedule"]
    ]
    gallery = list(GalleryItem.objects.all()) or [
        {"title": t, "icon": "\u25a0"} for t in DEFAULTS["gallery"]
    ]
    winners = list(Winner.objects.all()) or [
        {"team_name": t, "category": c} for t, c in DEFAULTS["winners"]
    ]
    updates = list(Update.objects.filter(is_active=True)) or [
        {"title": t, "description": d, "icon": "\u25a0"} for t, d in DEFAULTS["updates"]
    ]
    help_topics = list(HelpTopic.objects.all()) or [
        {"title": t, "description": d, "icon": "\u25a0"} for t, d in DEFAULTS["help"]
    ]
    faqs = list(FAQ.objects.all()) or [
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
    updates = Update.objects.filter(is_active=True).order_by("-created_at")
    if not updates.exists():
        data = [{"id": 0, "title": t, "description": d, "icon": "\u25a0"} for t, d in DEFAULTS["updates"]]
    else:
        data = _serialize(updates, ["id", "title", "description", "icon"])
    return JsonResponse({"updates": data})


def api_events(request):
    events = Event.objects.all()
    if not events.exists():
        data = [{"id": 0, "name": n, "description": d} for n, d in DEFAULTS["events"]]
    else:
        data = _serialize(events, ["id", "name", "description"])
    return JsonResponse({"events": data})


def api_clubs(request):
    clubs = Club.objects.all()
    if not clubs.exists():
        data = [{"id": 0, "name": n, "category": c} for n, c in DEFAULTS["clubs"]]
    else:
        data = _serialize(clubs, ["id", "name", "category"])
    return JsonResponse({"clubs": data})


def api_schedule(request):
    rows = ScheduleEntry.objects.all()
    if not rows.exists():
        data = [{"day": d, "morning": m, "afternoon": a, "evening": e} for d, m, a, e in DEFAULTS["schedule"]]
    else:
        data = _serialize(rows, ["day", "morning", "afternoon", "evening"])
    return JsonResponse({"schedule": data})


def api_faqs(request):
    faqs = FAQ.objects.all()
    if not faqs.exists():
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
        obj = form.save()
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
        form.save()
        return render(request, "core/index.html", {"reg_ok": True, "reg_form": RegistrationForm(), "fb_form": FeedbackForm()})
    return render(request, "core/index.html", {"reg_form": form, "fb_form": FeedbackForm()})
