# Mini Social Media App

A mini social network built with Django, SQLite, HTML, CSS and JavaScript.

## Features
- User profiles (bio, post / follower / following counts)
- Posts and comments
- Like / unlike (no page reload) and follow / unfollow
- Home feed of people you follow, with an "Everyone" tab
- Registration, login, logout, admin panel

## Database tables
users (Django auth), Profile, Post (with likes), Comment, Follow (followers)

## Run locally
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations social
    python manage.py migrate
    python manage.py seed              # optional demo users: ada, grace, linus (password demo12345)
    python manage.py createsuperuser   # optional, for /admin/
    python manage.py runserver

Open http://127.0.0.1:8000
