#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_microservice.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# backend/
# ├── manage.py
# ├── dians_project/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── wsgi.py
# │   └── ...
# ├── app/
# │   ├── migrations/
# │   │   └── __init__.py
# │   ├── __init__.py
# │   ├── ...
# login_microservice/
# ├── manage.py
# ├── login_microservice/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── wsgi.py
# │   ├── asgi.py
# ├── app/
# │   ├── migrations/
# │   │   └── __init__.py
# │   ├── __init__.py
# │   ├── models.py
# │   ├── serializer.py
# │   ├── service.py
# │   ├── views.py
# │   └── urls.py
