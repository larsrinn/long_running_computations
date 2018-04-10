release: python manage.py migrate
web: gunicorn long_running_computations.wsgi --timeout 60 --log-file -
worker: celery worker --app=long_running_computations.celery --concurrency=4 --loglevel=info
