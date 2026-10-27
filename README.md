# Contact Deduplicator API

A REST API for managing contacts and cleaning up duplicates. Each user keeps a private list of contacts, finds near-duplicate names with fuzzy matching, and merges two duplicates into one record.

## Features

- User registration and login with JWT authentication
- Per-user contacts: create, list, update and delete (users only see their own data)
- Duplicate detection: fuzzy name matching with `rapidfuzz` (similarity threshold 85)
- Merge endpoint: fills the missing fields of the kept contact and removes the duplicate
- Database migrations with Alembic
- Automated tests with pytest
- Docker setup for one-command startup

## Tech stack

Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT (`python-jose`, `passlib`), rapidfuzz, pytest, Docker

## Quick start with Docker

1. Copy `.env.example` to `.env` and set your own values:

   ```
   DATABASE_URL=postgresql://postgres:password@localhost:5432/contacts
   SECRET_KEY=change-me
   POSTGRES_PASSWORD=change-me
   ```

2. Start everything:

   ```
   docker compose up --build
   ```

3. Open the interactive docs at http://localhost:8000/docs

Migrations are applied automatically when the API container starts.

## Running locally without Docker

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

You need a running PostgreSQL database and a `.env` file with `DATABASE_URL` and `SECRET_KEY`.

## API overview

| Method | Endpoint                                | Description                    |
| ------ | --------------------------------------- | ------------------------------ |
| POST   | `/users/register`                       | Create a user                  |
| POST   | `/users/login`                          | Get a JWT access token         |
| POST   | `/contacts/create`                      | Create a contact               |
| GET    | `/contacts/all`                         | List your contacts             |
| PUT    | `/contacts/{contact_id}`                | Update a contact               |
| DELETE | `/contacts/{contact_id}`                | Delete a contact               |
| GET    | `/contacts/find-duplicates`             | Find pairs of similar contacts |
| POST   | `/contacts/merge/{keep_id}/{remove_id}` | Merge two contacts into one    |

All `/contacts` endpoints require a `Bearer` token.

## Running the tests

```
pytest -v
```

Tests run against an in-memory SQLite database and cover authentication, contact creation, duplicate detection and merging, including the case of merging a contact with itself.

## Author

Andrii, https://github.com/Andrii56823
