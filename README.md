# Django Healthcare Backend

A RESTful healthcare management API built with Django REST Framework and PostgreSQL. The application provides secure JWT-based authentication, patient management, doctor management, and patient-doctor assignments.

## Features

- **JWT Authentication** — User registration, login, access tokens, and token refresh.
- **Patient Management** — Create, view, update, and delete patient records.
- **Doctor Management** — Manage doctor profiles, specializations, email addresses, and phone numbers.
- **Patient-Doctor Assignments** — Assign doctors to patients, list assignments, and remove assignments.
- **Access Control** — Authenticated endpoints and patient records scoped to their creator.
- **Input Validation** — Serializer-based validation, including 10-digit patient phone numbers.
- **API Documentation** — Interactive Swagger UI and OpenAPI schema.
- **Automated Tests** — Tests for authentication, patient operations, validation, and other API behavior.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| Django REST Framework | REST API development |
| PostgreSQL | Relational database |
| Simple JWT | Token-based authentication |
| drf-spectacular | OpenAPI and Swagger documentation |
| python-dotenv | Environment variable management |

## Project Structure

```text
Django Healthcare Backend/
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── .env.example
├── .gitignore
├── manage.py
└── README.md
```

## Prerequisites

Install the following before starting:

- Python 3.10 or later
- PostgreSQL
- Git
- pip

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Singh-Vedant/django-healthcare-backend.git
cd django-healthcare-backend
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install Django djangorestframework djangorestframework-simplejwt drf-spectacular python-dotenv "psycopg[binary]"
```

### 4. Configure environment variables

Create a `.env` file in the project root, alongside `manage.py`.

```env
DJANGO_SECRET_KEY=replace-with-a-secure-secret-key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Replace the database values with your PostgreSQL credentials and database name. Ensure the database exists before running migrations.

Keep `.env` private. Never commit database credentials or secret keys to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

- API base URL: `http://127.0.0.1:8000/api/`
- Swagger documentation: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
- Django admin: `http://127.0.0.1:8000/admin/`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/auth/register/` | Register a user | Not required |
| POST | `/api/auth/login/` | Obtain JWT tokens | Not required |
| POST | `/api/auth/token/refresh/` | Refresh an access token | Refresh token required |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/patients/` | List your patients |
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/{id}/` | Retrieve a patient |
| PUT | `/api/patients/{id}/` | Update a patient |
| PATCH | `/api/patients/{id}/` | Partially update a patient |
| DELETE | `/api/patients/{id}/` | Delete a patient |

Patient records are scoped to the authenticated user who created them.

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/doctors/` | List doctors |
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/{id}/` | Retrieve a doctor |
| PUT | `/api/doctors/{id}/` | Update a doctor |
| PATCH | `/api/doctors/{id}/` | Partially update a doctor |
| DELETE | `/api/doctors/{id}/` | Delete a doctor |

### Patient-Doctor Assignments

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/mappings/` | List assignments for your patients |
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/{patient_id}/` | List assignments for a specific patient |
| DELETE | `/api/mappings/delete/{id}/` | Remove an assignment |

A patient and doctor pair cannot be assigned more than once.

## Authentication

Protected endpoints use JWT access tokens.

1. Register using `/api/auth/register/`.
2. Log in using `/api/auth/login/`.
3. Copy the returned `access` token.
4. Include it in protected requests:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

When testing through Swagger UI, click **Authorize** and provide the access token in the expected format.

## Example API Requests

### Register a user

`POST /api/auth/register/`

```json
{
  "username": "healthcare_user",
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

### Log in

`POST /api/auth/login/`

```json
{
  "username": "healthcare_user",
  "password": "SecurePass123!"
}
```

### Create a patient

`POST /api/patients/`

```json
{
  "name": "Test Patient",
  "age": 25,
  "gender": "Male",
  "phone": "9876543210",
  "address": "Delhi"
}
```

The authenticated user is automatically assigned as the creator of the patient record.

### Create a doctor

`POST /api/doctors/`

```json
{
  "name": "Dr. Priya Sharma",
  "specialization": "Dermatology",
  "email": "priya.sharma@example.com",
  "phone": "9876501234"
}
```

### Assign a doctor to a patient

`POST /api/mappings/`

```json
{
  "patient": 1,
  "doctor": 1
}
```

Replace the IDs with existing patient and doctor IDs accessible under your application's permissions.

## Running Tests

Run Django's system checks:

```bash
python manage.py check
```

Run the full test suite:

```bash
python manage.py test
```

Run tests for the API application:

```bash
python manage.py test api
```

Validate the generated OpenAPI schema:

```bash
python manage.py spectacular --validate
```

The project previously passed **16 automated tests**. Run the commands above again after making changes to verify the current state.

## Security Notes

- Store credentials and secret keys in environment variables.
- Do not commit `.env` files or real patient information.
- Use a strong, unique Django secret key.
- Disable debug mode and configure allowed hosts appropriately before production deployment.
- Use HTTPS in production.
- Apply appropriate authorization and access controls before exposing healthcare data.

## Future Improvements

- Frontend integration
- Deployment to a production hosting platform
- Expanded API and permission tests
- Pagination, filtering, and search
- Production monitoring and logging

## Author

**Vedant Singh**

- GitHub: [Singh-Vedant](https://github.com/Singh-Vedant)
- Project Repository: [django-healthcare-backend](https://github.com/Singh-Vedant/django-healthcare-backend)

---

Built with Django REST Framework and PostgreSQL.
