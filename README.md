# Online Chat Room — Django Backend

A Django project with a dedicated `chat` app and project configuration under `djangoproject/`. It is structured as the backend for an online chat-room application.

## Stack
- Python
- Django
- Django app routing and project settings

## Run locally
Create and activate a Python virtual environment, install the dependencies required by the project, configure a private development secret key, and run:

```bash
python manage.py migrate
python manage.py runserver
```

Review the chat app's models, views, URLs, and project settings to determine whether the current version uses polling, HTTP requests, or WebSockets. Configure production security settings before deployment.
