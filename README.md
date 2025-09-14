# UserBoard

A simple, clean full-stack CRUD application for managing users. Built with FastAPI, React, and PostgreSQL.

## Features

- **Create** new users with firstname, lastname, age, and date of birth
- **Read** and list all users in a clean table interface
- **Delete** users with confirmation prompts
- **Validation** on both frontend and backend
- **Responsive** design with clean styling

## Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **PostgreSQL** - Robust relational database
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **React 18** - UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool and dev server
- **CSS** - Clean, responsive styling

### Infrastructure
- **Docker Compose** - Multi-container orchestration
- **pytest** - Python testing framework

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Running the Application

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd UserBoard
   ```

2. **Start all services:**

```bash
docker compose up -d
```

3. **Access the application:**
   - **Web UI**: http://localhost:5173
   - **API Documentation**: http://localhost:8000/docs
   - **API Base**: http://localhost:8000

### Stopping the Application

```bash
docker compose down
```

To also remove the database volume:
```bash
docker compose down -v
```

## Development

### Running Tests

**API Tests:**
```bash
cd api
pip install -r requirements.txt
pytest tests/
```

### API Endpoints

- `GET /users` - List all users
- `POST /users/create` - Create a new user
- `DELETE /user` - Delete a user by ID (pass ID in request body)

## Troubleshooting

**Port conflicts:**
If ports 5173, 8000, or 5432 are busy, update the ports in `docker-compose.yml`.

**Database connection issues:**
Check that PostgreSQL is healthy: `docker compose logs db`

**Frontend can't reach API:**
Verify CORS settings in `api/app/main.py` and check that `VITE_API_URL` matches your API host.
