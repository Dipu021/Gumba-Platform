# Gumba

Gumba is a FastAPI-based backend platform for managing community organizations, donor contributions, and agent onboarding workflows. It supports registration of local Gumba entities, authentication for users and administrators, agent applications with identity verification uploads, and secure donation processing.

## Overview

The application is designed for organizations that need a lightweight but professional platform to:

- Register and list Gumba institutions
- Allow users to sign up and authenticate securely
- Let applicants submit agent profiles with uploaded identity documents
- Approve or reject agent applications through role-based access control
- Accept donations from users and send a confirmation email

## Features

- User registration and JWT-based login
- Role-based access for regular users and administrators
- Gumba creation and retrieval APIs
- Agent application workflow with file upload support
- Donation management tied to users and Gumba organizations
- Email notifications for successful donations
- SQLAlchemy ORM with SQLite by default
- Swagger/OpenAPI documentation via FastAPI

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL/SQLite support through environment configuration
- JWT authentication with python-jose
- Password hashing with passlib + bcrypt
- FastAPI Mail for donation confirmation emails
- Uvicorn for running the API server

## Project Structure

```text
Gumba/
├── api/
│   ├── agent.py
│   ├── auth.py
│   ├── donations.py
│   └── gumba.py
├── database/
│   └── database.py
├── models/
│   ├── agent.py
│   ├── agentapplication.py
│   ├── donations.py
│   ├── gumba.py
│   └── user.py
├── schemas/
│   ├── agent.py
│   ├── agentapplication.py
│   ├── auth.py
│   ├── donations.py
│   └── gumba.py
├── security/
│   ├── hash_password.py
│   ├── oauth2.py
│   ├── verify_password.py
│   └── __init__.py
├── services/
│   ├── email.py
│   ├── get_current_user.py
│   └── __init__.py
├── .env
├── .gitignore
├── create_admin.py
├── main.py
├── pyproject.toml
├── README.md
├── reset_admin.py
├── requirements.txt
├── test.db
└── uploads/
```

## Getting Started

### Prerequisites

- Python 3.13 or later
- pip or uv

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Gumba
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or, if using uv:

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the project root with the following values:

```env
DATABASE_URL="sqlite:///./test2.db"
SECRET_KEY="your-super-secret-key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
MAIL_USERNAME="your-email@example.com"
MAIL_PASSWORD="your-app-password"
MAIL_FROM="your-from-email@example.com"
```

> Replace the sample values with your own secure configuration before running the app.

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

- http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- ReDoc docs: http://localhost:8000/redoc

## Main API Endpoints

### Authentication

- `POST /auth/register` — Register a new user
- `POST /auth/login` — Login and receive a JWT token

### Gumba Management

- `POST /gumba/gumbas` — Create a Gumba record
- `GET /gumba/gumbas` — List all Gumbas
- `GET /gumba/gumbas/{gumba_id}` — Fetch a specific Gumba

### Agent Management

- `POST /agent/admin` — Create an agent entry from admin-side form data
- `POST /agent/apply` — Submit an agent application as a logged-in user
- `GET /agent/agents` — Get all agents
- `GET /agent/agents/{agent_id}` — Get one agent
- `PATCH /agent/applications/{application_id}/approve` — Approve a pending application

### Donations

- `POST /donations/donations` — Create a donation for a specific Gumba

## Database

The project uses SQLAlchemy with a database URL sourced from the `.env` file. The default configuration points to SQLite for local development:

```env
DATABASE_URL="sqlite:///./test2.db"
```

The database schema is created automatically on application startup through the SQLAlchemy metadata setup in `main.py`.

## Admin Setup

To create the initial administrator account, run:

```bash
python create_admin.py
```

To update an existing user's account to admin status and reset the password:

```bash
python reset_admin.py
```

## Security Notes

- Passwords are hashed using bcrypt
- JWTs are used for API authentication
- Uploaded identity documents are saved under `uploads/identity`
- Secrets must never be committed to source control

## License

This project is currently distributed without a formal license declaration. If you are publishing or sharing it publicly, consider adding an appropriate open-source license.

## Contributing

Contributions are welcome. Please keep the codebase clean and consistent, and validate your changes against the current FastAPI routes and database models before submitting updates.
