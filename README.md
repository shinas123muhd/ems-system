# EMS Pro — Employee Management System

## Tech Stack
- **Backend:** Python (Django 4.x), Django REST Framework
- **Authentication:** JWT (access + refresh tokens via simplejwt)
- **Frontend:** HTML, CSS, JavaScript (vanilla, no framework)
- **Database:** SQLite (switch to PostgreSQL for production)

## Features
- 🔐 Auth: Login, Register, Change Password, Profile Management
- 🧩 Dynamic Form Builder with drag-and-drop field reordering
- 👥 Employee CRUD with dynamic field support
- 🔍 Employee search & filter by dynamic field labels
- 🌐 Full REST API with JWT authentication

## Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register |
| POST | /api/auth/login/ | Login (returns JWT) |
| POST | /api/auth/logout/ | Logout (blacklist token) |
| GET/PUT | /api/auth/profile/ | Get/update profile |
| POST | /api/auth/change-password/ | Change password |
| POST | /api/auth/token/refresh/ | Refresh JWT |

### Forms
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | /api/forms/ | List/create forms |
| GET/PUT/DELETE | /api/forms/{id}/ | Form detail |
| GET/POST | /api/forms/{id}/fields/ | Form fields |

### Employees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | /api/employees/ | List/create employees |
| GET/PUT/DELETE | /api/employees/{id}/ | Employee detail |

**Auth header:** `Authorization: Bearer <access_token>`

## Web Routes
- `/accounts/login/` — Login page
- `/accounts/register/` — Register page
- `/employees/` — Employee list
- `/employees/dashboard/` — Dashboard
- `/employees/forms/` — Form list
- `/employees/forms/builder/` — Create form
- `/employees/create/` — Create employee
