# Django Healthcare Backend

A RESTful healthcare management API built with **Django, Django REST Framework, and JWT authentication**. The application supports user registration, login, patient management, doctor management, and patient–doctor mapping, with interactive API documentation using Swagger UI.

## Features

- **User Authentication:** Register users and authenticate with username and password.
- **JWT Authentication:** Secure protected endpoints using access and refresh tokens.
- **Patient Management:** Create, retrieve, update, and delete patient records.
- **Doctor Management:** Create, list, retrieve, update, and delete doctor records.
- **Patient–Doctor Mapping:** Associate patients with doctors and manage these relationships.
- **User-Specific Patient Access:** Patients are scoped to the authenticated user who created them.
- **Input Validation:** Validate request data, including patient phone numbers.
- **API Documentation:** Explore and test endpoints through Swagger UI.
- **Automated Testing:** Test API functionality using Django's test framework.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend framework |
| Django REST Framework | REST API development |
| Simple JWT | Token-based authentication |
| drf-spectacular | OpenAPI schema and Swagger documentation |
| Database | Configured through Django settings |
| Git and GitHub | Version control and hosting |

## Project Structure

```text
Django Healthcare Backend/
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── .env
├── .env.example
├── .gitignore
├── manage.py
└── README.md
```

## Getting Started

### Prerequisites

- Python installed on your system
- pip
- Git
- VS Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/Singh-Vedant/django-healthcare-backend.git
cd django-healthcare-backend
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository contains a `requirements.txt` file:

```bash
python -m pip install -r requirements.txt
```

If no requirements file exists, install the project's dependencies and verify the database driver required by your settings:

```bash
python -m pip install Django djangorestframework djangorestframework-simplejwt drf-spectacular python-dotenv
```

### 4. Configure environment variables

Review `.env.example` and create or update your local `.env` file with the environment variables required by `config/settings.py`.

For example, if your project uses environment-based configuration:

```env
SECRET_KEY=replace-with-a-secure-secret-key
DEBUG=True
```

Add the appropriate database configuration if required by your project.

**Important:** Never commit `.env`, database passwords, or production secret keys to GitHub.

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## API Documentation

Swagger UI provides an interactive interface for exploring endpoints, submitting requests, and viewing responses.

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **OpenAPI Schema:** `http://127.0.0.1:8000/api/schema/`

## API Endpoints

All endpoints below are prefixed with `/api/`.

### Authentication

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/auth/register/` | Register a user | Not required |
| POST | `/auth/login/` | Authenticate and obtain JWT tokens | Not required |
| POST | `/auth/token/refresh/` | Refresh an access token | Refresh token |

**Registration request:**

```json
{
  "name": "Vedant Singh",
  "username": "vedant",
  "email": "vedant@example.com",
  "password": "SecurePass123!"
}
```

**Login request:**

```json
{
  "username": "vedant",
  "password": "SecurePass123!"
}
```

A successful login returns an access token and a refresh token.

### Patients

| Method | Endpoint | Description |
|---|---|---|
| GET | `/patients/` | List the authenticated user's patients |
| POST | `/patients/` | Create a patient |
| GET | `/patients/{id}/` | Retrieve a patient |
| PUT | `/patients/{id}/` | Replace a patient's data |
| PATCH | `/patients/{id}/` | Partially update a patient |
| DELETE | `/patients/{id}/` | Delete a patient |

Patient creation associates the record with the authenticated user.

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| GET | `/doctors/` | List doctors |
| POST | `/doctors/` | Create a doctor |
| GET | `/doctors/{id}/` | Retrieve a doctor |
| PUT | `/doctors/{id}/` | Replace a doctor's data |
| PATCH | `/doctors/{id}/` | Partially update a doctor |
| DELETE | `/doctors/{id}/` | Delete a doctor |

### Patient–Doctor Mappings

| Method | Endpoint | Description |
|---|---|---|
| GET | `/mappings/` | List mappings accessible to the user |
| POST | `/mappings/` | Create a patient–doctor mapping |
| GET | `/mappings/{patient_id}/` | List mappings for a patient |
| DELETE | `/mappings/delete/{mapping_id}/` | Delete a specific mapping |

## JWT Authentication

Protected endpoints require a valid JWT access token.

### How to authenticate

1. Register a user using `/api/auth/register/`.
2. Log in using `/api/auth/login/`.
3. Copy the returned `access` token.
4. Open Swagger UI and select **Authorize**.
5. Enter the access token in the format expected by the configured Bearer authentication scheme. For example:

```text
Bearer YOUR_ACCESS_TOKEN
```

6. Authorize and execute protected API requests.

When the access token expires, use `/api/auth/token/refresh/` with the refresh token to obtain a new access token.

## Testing

The project includes automated API tests.

Run the full API test suite:

```bash
python manage.py test api
```

Run Django system checks:

```bash
python manage.py check
```

The current test suite has **16 tests**, which have passed successfully in the local development environment.

## Security Considerations

- Keep secret keys and credentials out of source control.
- Use HTTPS and secure environment configuration in production.
- Use JWT access tokens only for their intended lifetime.
- Enforce authentication and authorization for protected resources.
- Review patient and doctor access rules before deploying with real healthcare data.
- Do not use Django's development server as a production server.

## Future Improvements

- Add role-based permissions for administrators, doctors, and patients.
- Add pagination, filtering, and search.
- Expand API validation and automated test coverage.
- Configure production deployment and monitoring.
- Add audit logging for sensitive healthcare operations.

## Author

**Vedant Singh**

- GitHub: [Singh-Vedant](https://github.com/Singh-Vedant)
- Repository: [django-healthcare-backend](https://github.com/Singh-Vedant/django-healthcare-backend)

---

*This project is intended for healthcare management API development and learning. Use appropriate security, privacy, and compliance controls before handling real patient data.*
