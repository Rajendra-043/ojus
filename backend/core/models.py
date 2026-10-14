"""Database models for OJAS 2026 — mirrors the PDF sections."""
from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=80, unique=True)
    category = models.CharField(max_length=80, default="")
    description = models.CharField(max_length=200, default="", blank=True)
    icon = models.CharField(max_length=8, default="\U0001F91D")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=200, default="")
    icon = models.CharField(max_length=8, default="\U0001F3AF")
    club = models.ForeignKey(Club, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class ScheduleEntry(models.Model):
    day = models.CharField(max_length=20)  # Day 1 / Day 2 / Day 3
    morning = models.CharField(max_length=120)
    afternoon = models.CharField(max_length=120)
    evening = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Schedule entries"

    def __str__(self):
        return self.day


class GalleryItem(models.Model):
    title = models.CharField(max_length=80)
    icon = models.CharField(max_length=8, default="\U0001F4F8")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Winner(models.Model):
    team_name = models.CharField(max_length=80)
    category = models.CharField(max_length=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.team_name} ({self.category})"


class Update(models.Model):
    """'What's New' cards. This is the model the updates API / requirements cover."""

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=8, default="\U0001F4E3")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class HelpTopic(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=300)
    icon = models.CharField(max_length=8, default="\U0001F198")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=400)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


class Registration(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    club = models.CharField(max_length=80, default="", blank=True)
    event = models.CharField(max_length=80, default="", blank=True)
    message = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} -> {self.event or 'OJAS'}"


class Feedback(models.Model):
    name = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback from {self.name}"
