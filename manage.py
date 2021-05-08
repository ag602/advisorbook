#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
    try:
        from django.core.management import call_command, execute_from_command_line
        if sys.argv[1] == 'runserver':
            import django
            django.setup()
            call_command('makemigrations')
            call_command('migrate')
            from django.conf import settings
            # get the currently active user model
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.count():
                call_command('createsuperuser')
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
