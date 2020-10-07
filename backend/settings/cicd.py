from .base import *

SECRET_KEY = "unsafe-secret-key"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

if env("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "github_actions",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }
