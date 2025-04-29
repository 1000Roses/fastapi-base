# FastAPI Employee Management System

A robust and scalable employee management system built with FastAPI, SQLAlchemy, and MySQL.

## Features

- RESTful API for employee management
- Asynchronous database operations
- Comprehensive logging system
- Request tracking with unique IDs
- SQL query logging
- Connection pooling
- Error handling and validation

## Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Async Support**: SQLAlchemy Async
- **Logging**: Loguru
- **Validation**: Pydantic

## Project Structure

```
app/
├── core/           # Core configurations and utilities
│   ├── config.py   # Application settings
│   ├── logging.py  # Logging configuration
│   └── sql_logging.py # SQL query logging
├── db/             # Database related code
│   └── session.py  # Database session management
├── models/         # SQLAlchemy models
├── repositories/   # Database repositories
├── schemas/        # Pydantic models
└── services/       # Business logic
```

## Database Configuration

The application uses connection pooling with the following settings:
- Pool Size: 20 connections
- Max Overflow: 10 connections
- Pool Recycle: 3600 seconds (1 hour)
- Pool Timeout: 30 seconds

## Logging Features

- Request ID tracking
- SQL query logging with execution time
- Service call logging
- Error tracking with stack traces
- Affected rows logging for SQL operations

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (see `.env.example`)
4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Employees

- `GET /employees` - List all employees
- `GET /employees/{id}` - Get employee by ID
- `POST /employees` - Create new employee
- `PUT /employees/{id}` - Update employee
- `DELETE /employees/{id}` - Delete employee

## Error Handling

The application uses a standardized error response format:
```json
{
    "status": int,
    "msg": str,
    "detail": Optional[Any]
}
```

## Development

- The project uses type hints throughout
- SQL queries are logged with execution time
- Each request has a unique ID for tracking
- Database operations are asynchronous
- Repository pattern for database access

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 