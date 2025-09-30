# Dormitory Management System

A Django + Django REST Framework project for managing dormitory requests and student accounts, with JWT authentication and role-based access control.

---

## Project Overview

This system has **two types of users**:

- **Students**: Can submit requests for:
  - Dormitory maintenance (repair, cleaning, needed items)
  - Complaints
  - Priority requests (if payment is provided)
  - **Filter requests** based on:
    - Status (`Pending`, `Accepted`, `Rejected`)
    - Roommates
    - Week, Month, or Term

- **Admins** (Dormitory staff) Can:
  - View all requests
  - Change request status (Accepted, Rejected, Pending)
  - Add comments to requests

**Features**:
- JWT authentication for all users
- Role-based API access (some APIs are for Students only, some for Admins)
- Request priority handling based on payment
- Request filtering by status, roommates, and time period

---

##  Tech Stack

- **Backend**: Django, Django REST Framework  
- **Authentication**: JWT (JSON Web Tokens)  
- **Database**: PostgreSQL (Dockerized)  
- **Task Queue (Optional)**: Celery + Redis  
- **Containerization**: Docker & Docker Compose  

---

##  Docker Setup

1. **Build and start containers**
```bash
docker-compose up -d --build
```
2. **Check logs**
```bash
docker-compose logs -f project
```
3.**Enter Django container**
```bash
docker exec -it Dormitory-web bash
```
4.**Apply migrate**
```bash
python Dormitory_system/manage.py migrate
```
5.**Create superuser**
```bash
python Dormitory_system/manage.py createsuperuser
```
## Authentication
- **JWT tokens are used for login and API access**
- **Include the token in the header for API requests:**
```bash
Authorization: Bearer <your_token_here>
```

## API Documentation
Once the server is running, open: http://127.0.0.1:8000/swagger/

You can view all endpoints and try them directly via Swagger UI.

## Development Notes
To reset the database in Docker:
```bash
docker-compose down -v
docker-compose up -d --build
docker exec -it Dormitory-web python Dormitory_system/manage.py migrate
```

##  Project Structure
```bash
Dormitory_system/
├── Dormitory_system/       # Django settings
├── allusers/               # Student & user models
├── dormitory/              # dormitory models
├── room/                   # Dormitory room models
├── request/                # Dorm requests and status
├── wallet/                 # Student account balance
├── transaction/            # Transaction model
├── logs/                   # Application logs
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```


> **Developer:** Mohamadreza Heydarnia

> **Date:** September 2025
