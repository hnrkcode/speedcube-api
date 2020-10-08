# Backend Project

This repository contains the backend part of the of the speedcube website and is an API built with [Django](https://www.djangoproject.com/) and [DRF](https://www.django-rest-framework.org/) for the frontend to consume.

The project uses [Simple JWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt) to implement JSON Web Token authentication and [django-cors-headers](https://github.com/adamchainz/django-cors-headers) to allow in-browser requests from other origins, so the frontend can communicate with the API.

## Setup

Install `PostgreSQL` and dependencies for `psycopg2`:

```bash
sudo apt update && sudo apt install postgresql postgresql-contrib libpq-dev python-dev
```

### Pipenv

Install dependencies with [Pipenv](https://github.com/pypa/pipenv) from the `Pipfile`:

```bash
pipenv install --dev
```
When the dependencies are installed you only need to activate the environment:

```bash
pipenv shell
```

## Development

Migrate models to database, create a superuser and run the project in development:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Tests

Run all unit tests:

```bash
python manage.py test
```

Test coverage:

```bash
coverage run --source="." manage.py test api
coverage report
```