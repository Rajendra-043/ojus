from django.contrib import admin
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

for model in (Club, Event, ScheduleEntry, GalleryItem, Winner, Update, HelpTopic, FAQ, Registration, Feedback):
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
