# English Word Trainer Backend

A FastAPI-based backend for the English Word Trainer application.

## Features

- User authentication with JWT tokens
- PostgreSQL database integration
- CORS support for frontend integration
- API documentation with Swagger UI and ReDoc

## Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd word-english-trainer-backend
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create .env file:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Environment Variables

- `DEBUG`: Enable debug mode (default: False)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `WORKERS`: Number of worker processes (default: 1)
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time in minutes (default: 60)
- `DATABASE_URL`: PostgreSQL connection URL

## Running the Application

### Development

```bash
uvicorn app.main:app --reload
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
docker-compose up -d
```

## API Documentation

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## API Endpoints

### Authentication

- POST `/api/auth/signup` - Create new user account
- POST `/api/auth/signin` - Sign in and get JWT token
- GET `/api/auth/profile` - Get current user profile

### Health Check

- GET `/health` - Check API health status
