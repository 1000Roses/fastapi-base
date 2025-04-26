# FastAPI Chat Bot

A FastAPI-based chat bot application with MySQL and Redis integration.

## Features

- MySQL connection pooling (max 20 connections, 10 reusable)
- Redis integration with string/list/JSON operations
- JWT authentication
- Structured logging with UUID tracking
- Modular architecture with separate handlers, services, and repositories

## Project Structure

```
.
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── redis.py
│   │   ├── models/
│   │   │   └── user.py
│   │   ├── schemas/
│   │   │   └── user.py
│   │   ├── services/
│   │   │   └── user.py
│   │   └── repositories/
│   │       └── user.py
│   ├── tests/
│   ├── .env
│   ├── requirements.txt
│   └── main.py
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env` file

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 