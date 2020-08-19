web: gunicorn --pythonpath app config.wsgi:application --bind 0.0.0.0:8000
worker: celery -A config.celery_app worker --workdir app
beat: celery -A config.celery_app beat --workdir app --scheduler django_celery_beat.schedulers:DatabaseScheduler