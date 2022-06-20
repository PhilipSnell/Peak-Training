release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn xcell.wsgi --log-file -