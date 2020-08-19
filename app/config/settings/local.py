from .base import *
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="!-#bh7j)51ipa=k)0$q-76(isvalgui91m!!ch6((xacp0)h4e",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/3.1/topics/email/#console-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
