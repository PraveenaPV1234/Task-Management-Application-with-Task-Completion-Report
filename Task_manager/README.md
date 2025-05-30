# Task Management Application with Completion Report

This Django project implements a Task Management System with the following features:

- JWT-based API access for regular users
- Admin Panel for Admins and SuperAdmins with role-based permissions
- Task Completion reporting with worked hours

##  Features

###  User (via API only)
- Authenticate via JWT
- View their assigned tasks (`GET /tasks/`)
- Mark a task as completed with a report and worked hours (`PUT /tasks/<id>/`)

### Admin
- Assign tasks to their users via web panel
- View tasks of users assigned to them
- View task completion reports (`GET /tasks/{id}/report`)
### SuperAdmin
- Create/delete users and admins
- Assign users to admins
- Manage all tasks
- View all task completion reports

## API Endpoints

| Method | Endpoint                  | Description                       |
|--------|---------------------------|-----------------------------------|
| POST   | `/api/token/`            | Get JWT token                     |
| GET    | `/tasks/`                | User fetches their own tasks      |
| PUT    | `/tasks/<id>/`          | Mark task completed w/ report     |
| GET    | `/tasks/<id>/report/`   | Admin/SuperAdmin view report      |

## 🖥️ Admin Panel (HTML Templates)

| Template               | Description                           |
|------------------------|---------------------------------------|
| `dashboard.html`       | Admin dashboard                       |
| `create_user.html`     | Create regular user                   |
| `create_admin.html`    | Create admin user                     |
| `promote_user.html`    | Promote user to admin                 |
| `assign_user.html`     | Assign a user to an admin             |
| `create_task.html`     | Admin assigns task to their user      |
| `users.html`           | List of users                         |
| `tasks.html`           | List of tasks                         |
| `base.html`            | Base layout template                  |

##  Setup Instructions

### 1. Clone the repository


git clone <your_repo_url>
cd task-manager


### 2. Create virtual environment and install requirements

python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
pip install -r requirements.txt


### 3. Run migrations

python manage.py makemigrations
python manage.py migrate


### 4. Create Superuser

python manage.py createsuperuser


### 5. Run the server

python manage.py runserver


##  Notes
- Make sure `rest_framework` and `rest_framework_simplejwt` are installed.
- SQLite is used as the default database.
- Use `admin/` for the Django admin backend and `/admin/dashboard/` for your custom admin panel.

