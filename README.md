# FastAPI & PostgreSQL Architecture Sprint | Documentation

A technical breakdown and implementation record covering the architecture of an asynchronous RESTful API backend built with **Python 3.13**, **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**. 

This documentation tracks key engineering patterns mastered during the sprint, including Pydantic V2 settings management, OAuth2 stateless authentication, relational upvoting database logic, CORS security, and automated database schema migrations via Alembic.

---

## 🎯 Architecture & Learning Objectives

- **Asynchronous API Execution:** Leveraging FastAPI and ASGI architecture for non-blocking I/O operation.
- **Strict Data Validation (Pydantic V2):** Utilizing `pydantic-settings` for environment configuration parsing and strong payload typing.
- **Relational Data Modeling:** Building schema-mapped models with SQLAlchemy ORM, composite key relationships, and foreign key cascades.
- **Stateless Authentication:** Passlib (Bcrypt) password hashing combined with OAuth2 Password Flow using JWT bearer tokens.
- **Database Migration Control:** Generating and applying programmatic schema versioning using Alembic.
- **Cross-Origin Resource Sharing (CORS):** Middleware configuration for secure cross-origin requests from web frontends.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.13
- **Web Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Database Versioning:** Alembic
- **Security & Tokens:** Python-Jose (JWT), Passlib (Bcrypt)
- **Data & Environment Validation:** Pydantic V2, Pydantic-Settings

---

## 📁 Repository Directory Structure

```text
Fastapi-backend-sprint/
├── alembic/                  # Database migration scripts and env.py setup
│   └── versions/             # Sequential migration files
├── app/
│   ├── routers/
│   │   ├── auth.py           # Authentication & token generation endpoints
│   │   ├── posts.py          # Post resource CRUD routes
│   │   ├── user.py           # User management and registration
│   │   └── vote.py           # Upvote/downvote relational logic
│   ├── config.py             # App environment configuration (Pydantic V2)
│   ├── database.py           # SQLAlchemy engine, session maker, & Base
│   ├── main.py               # FastAPI initialization & CORS middleware
│   ├── models.py             # SQLAlchemy ORM models
│   ├── oauth2.py             # JWT generation & dependency authentication
│   └── schemas.py            # Pydantic validation & response models
├── .env                      # Local environment variable configuration
├── .gitignore                # Git exclusions (.venv, __pycache__, .env)
├── alembic.ini               # Alembic setup configuration
└── requirements.txt          # Project dependencies
```

## ⚙️ Environment Setup & Quickstart
1. Prerequisites
Ensure you have Python 3.13+ and a running instance of PostgreSQL on port 5432.

2. Virtual Environment & Dependencies
- Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

- Install required dependencies
pip install -r requirements.txt

3. Environment Variables Configuration
Create a .env file in the project root directory:
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

4. Database Schema Migrations
Apply all migration revisions to your local PostgreSQL database:
alembic upgrade head

5. Running the API Server
Start the Uvicorn development server:
uvicorn app.main:app --reload

- Interactive API Docs (Swagger UI): http://127.0.0.1:8000/docs

- ReDoc Documentation: http://127.0.0.1:8000/redoc
---

## 🔒 API Route Summary

| Method   | Endpoint      | Description                                       | Auth Required |
| :---     | :---          | :---                                              | :---          |
| `POST`   | `/login`      | User login & JWT token retrieval                  | No            |
| `POST`   | `/users`      | Register a new user                               | No            |
| `GET`    | `/users/{id}` | Fetch public user profile details                 | No            |
| `GET`    | `/posts`      | Retrieve all posts (Supports pagination & search) | No            |
| `POST`   | `/posts`      | Create a new post resource                        | **Yes**       |
| `GET`    | `/posts/{id}` | Get post details by ID                            | No            |
| `DELETE` | `/posts/{id}` | Delete owned post resource                        | **Yes**       |
| `PUT`    | `/posts/{id}` | Update owned post resource                        | **Yes**       |
| `POST`   | `/vote`       | Upvote or remove vote on a post                   | **Yes**       |

## 📌 Important Technical Notes & Learnings
Pydantic V2 Migration Notice: BaseSettings was migrated to pydantic-settings (from pydantic_settings import BaseSettings), and orm_mode = True was updated to from_attributes = True inside ConfigDict models.

HTTP 204 Status Code Enforcement: Delete operations returning 204 NO CONTENT must not declare a response_model or return a body payload, per HTTP specification.

Strict Environment Matching: Variable names in .env (e.g., DATABASE_HOSTNAME) must map exactly to Settings class field attributes to prevent ValidationError on startup.

