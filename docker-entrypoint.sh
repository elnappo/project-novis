#!/usr/bin/env bash
# Based on https://github.com/lukin0110/docker-django-boilerplate/blob/master/deployment/docker-entrypoint.sh

set -o errexit    # abort script at first error
set -o pipefail   # return the exit status of the last command in the pipe

[[ -z "$DATABASE_URL" ]] && echo "ERROR: DATABASE_URL must be set!" && exit 1;

# Define help message
show_help() {
    echo """
Usage: docker run <imagename> COMMAND
Commands
bash            : Start a bash shell
python          : Start a Python shell
shell           : Start a Django Python shell
test            : Run tests
migrate         : Run database migrations
createsuperuser : Create superuser
manage          : Run manage.py task
dev             : Start a normal Django development server
gunicorn        : Run Gunicorn server
help            : Show this message
"""
}

# Run
case "$1" in
    bash)
        exec /bin/bash "${@:2}"
    ;;
    python)
        exec python "${@:2}"
    ;;
    shell)
        exec python manage.py shell
    ;;
    test)
        exec python manage.py test
    ;;
    migrate)
        echo "Apply database migrations"
        exec python manage.py migrate --noinput
    ;;
    createsuperuser)
        [[ -z "$DJANGO_SUPERUSER_EMAIL" ]] && echo "ERROR: Need to set DJANGO_SUPERUSER_EMAIL" && exit 1;
        [[ -z "$DJANGO_SUPERUSER_PASSWORD" ]] && echo "ERROR: Need to set DJANGO_SUPERUSER_PASSWORD" && exit 1;
        echo "Create superuser ${DJANGO_SUPERUSER_EMAIL}"
        exec python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser(\"$DJANGO_SUPERUSER_EMAIL\", \"$DJANGO_SUPERUSER_PASSWORD\")" || true
    ;;
    manage)
        echo "Running Django management command ${@:2}"
        exec python manage.py "${@:2}"
    ;;
    dev)
        echo "Running Development Server on 0.0.0.0:8000"
        exec python manage.py runserver 0.0.0.0:8000
    ;;
    gunicorn)
        echo "Running App via Gunicorn"
        exec gunicorn -b :8000 --worker-class gevent --worker-connections 20 --timeout 10 --graceful-timeout 30 --access-logfile - wsgi
    ;;
    help)
        show_help
        ;;
    *)
        echo "unknown command ${@:1}"
        show_help
        exit 1
    ;;
esac
