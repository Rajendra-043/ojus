from django.core.management.base import BaseCommand
from core.models import (
    Club, Event, FAQ, GalleryItem, HelpTopic, ScheduleEntry, Update, Winner,
)
from core.views import DEFAULTS


class Command(BaseCommand):
    help = "Seed OJAS 2026 content (events, clubs, schedule, updates, faqs...)"

    def handle(self, *args, **options):
        for i, (name, cat) in enumerate(DEFAULTS["clubs"]):
            Club.objects.get_or_create(name=name, defaults={"category": cat, "order": i})
        for i, (name, desc) in enumerate(DEFAULTS["events"]):
            Event.objects.get_or_create(name=name, defaults={"description": desc, "order": i})
        for i, (day, m, a, e) in enumerate(DEFAULTS["schedule"]):
            ScheduleEntry.objects.get_or_create(day=day, defaults={"morning": m, "afternoon": a, "evening": e, "order": i})
        for i, t in enumerate(DEFAULTS["gallery"]):
            GalleryItem.objects.get_or_create(title=t, defaults={"order": i})
        for i, (t, c) in enumerate(DEFAULTS["winners"]):
            Winner.objects.get_or_create(team_name=t, defaults={"category": c, "order": i})
        for t, d in DEFAULTS["updates"]:
            Update.objects.get_or_create(title=t, defaults={"description": d})
        for i, (t, d) in enumerate(DEFAULTS["help"]):
            HelpTopic.objects.get_or_create(title=t, defaults={"description": d, "order": i})
        for i, (q, a) in enumerate(DEFAULTS["faqs"]):
            FAQ.objects.get_or_create(question=q, defaults={"answer": a, "order": i})
        self.stdout.write(self.style.SUCCESS("OJAS 2026 seed data loaded."))
