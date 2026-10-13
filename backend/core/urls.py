from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("healthz/", views.healthz, name="healthz"),
    path("register/", views.register_page, name="register"),
    path("api/updates/", views.api_updates, name="api-updates"),
    path("api/events/", views.api_events, name="api-events"),
    path("api/clubs/", views.api_clubs, name="api-clubs"),
    path("api/schedule/", views.api_schedule, name="api-schedule"),
    path("api/faqs/", views.api_faqs, name="api-faqs"),
    path("api/register/", views.api_register, name="api-register"),
    path("api/feedback/", views.api_feedback, name="api-feedback"),
]
