# FastAPI JWT Authentication Demo

A small FastAPI app with signup, login, profile, logout and account deletion, secured with JWT bearer tokens. Users are stored in a local JSON file (`users.json`) and there is a simple HTML/JS frontend served by the same app.

This is a learning project, not production auth: passwords are stored in plain text, the JWT secret is hardcoded, tokens have no expiry, and `GET /users` returns every user record without authentication.

## Tech stack

Python 3.10+, FastAPI, Uvicorn, `python-jose` (JWT), Pydantic (`EmailStr` via `email-validator`), Jinja2 templates, vanilla JavaScript.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

No environment variables are needed; the app does not read any. `.env.example` is included only as a reminder that `SECRET_KEY` in `main.py` should be moved to an environment variable before any real deployment.

`users.json` is created automatically on first run and is ignored by git because it holds user credentials.

## Running

Run from inside this folder (templates and static files use relative paths):

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 for the frontend, or http://127.0.0.1:8000/docs for the interactive API docs.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/` | No | HTML frontend |
| POST | `/signup` | No | Body: `username`, `email`, `password` |
| POST | `/login` | No | Body: `username`, `password`; returns a JWT `token` |
| GET | `/profile` | Bearer | Current user's username and email |
| GET | `/users` | No | All stored users |
| DELETE | `/delete` | Bearer | Delete the current user |
| POST | `/logout` | Bearer | Clears the stored token for the current user |

Send the token as `Authorization: Bearer <token>`.
