# Production-Ready FastAPI Backend Service

An asynchronous RESTful API architecture engineered with Python, FastAPI, and PostgreSQL. Demonstrates robust data validation with Pydantic, database orchestration with SQLAlchemy ORM, schema version control via Alembic, and route-level security with OAuth2 and JWT bearer tokens.

---

## Key Features

- **Asynchronous Endpoints:** Optimized request handling using FastAPI and ASGI architecture.
- **Strict Data Validation:** Type-safe serialization, sanitization, and request modeling using Pydantic schemas.
- **Relational Persistence:** Database abstraction and relational mappings using SQLAlchemy ORM.
- **Security & Authentication:** Secure password hashing (bcrypt) and stateless user authentication using OAuth2 with JWT tokens.
- **Schema Migrations:** Versioned database migrations handled via Alembic.
- **Interactive Documentation:** Out-of-the-box interactive API testing with Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## Tech Stack

**Framework:** FastAPI
**Language:** Python 3.11+
**Database:** PostgreSQL
**ORM & Migrations:** SQLAlchemy, Alembic
**Security:** Passlib (Bcrypt), Python-Jose (JWT)
**Server Engine:** Uvicorn

---

## Project Structure

```text
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py      # Authentication & token issuing
│       │   ├── users.py     # User registration & profile management
│       │   └── posts.py     # Core resource CRUD routes
│       └── router.py        # Central API route registration
├── core/
│   ├── config.py            # Environment settings (Pydantic BaseSettings)
│   └── security.py          # Password hashing & JWT verification
├── db/
│   ├── base.py              # Declarative base model
│   └── session.py           # Engine & get_db dependency session
├── models/                  # SQLAlchemy database models
├── schemas/                 # Pydantic validation schemas
└── main.py                  # ASGI application entrypoint