"""Django settings for OJAS 2026 (BIT Durg)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-ojas-2026-bit-durg-dev-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"


def _env_hosts(name):
    raw = os.environ.get(name, "")
    return [h.strip() for h in raw.split(",") if h.strip()]


# Base hosts (local dev) + env override. Render hostnames are added
# automatically below so deploys don't hit DisallowedHost.
ALLOWED_HOSTS = _env_hosts("DJANGO_ALLOWED_HOSTS") or [
    "127.0.0.1",
    "localhost",
    "testserver",
]
if ".onrender.com" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".onrender.com")
_render_host = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()
if _render_host and _render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_render_host)

CSRF_TRUSTED_ORIGINS = _env_hosts("DJANGO_CSRF_TRUSTED_ORIGINS") or [
    "https://*.onrender.com",
]
if _render_host and f"https://{_render_host}" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_render_host}")

# Render terminates TLS at its proxy — tell Django the forwarded proto is https.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ojas_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ojas_backend.wsgi.application"
ASGI_APPLICATION = "ojas_backend.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
_static_dir = BASE_DIR / "static"
# Only add if it exists (Render builds from different roots otherwise warn).
STATICFILES_DIRS = [_static_dir] if _static_dir.is_dir() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    # Compressed (not manifest-hashed): never 500s when collectstatic
    # hasn't run, still served efficiently by WhiteNoise.
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
}

# Campus photo: save the provided BIT Durg photo as
#   backend/static/core/img/campus.jpg
# It is served as the site background (see templates + styles.css).
CAMPUS_PHOTO_PATH = "core/img/campus.jpg"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
