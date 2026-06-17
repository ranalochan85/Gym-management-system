# Gym Management System - Backend

Comprehensive FastAPI-based gym management system backend.

## Features

- User Management (Members, Trainers, Staff)
- Membership Management
- Attendance Tracking (QR Code & RFID)
- Workout Plans & Exercise Logging
- Nutrition & Diet Plans
- Payment Processing
- Group Classes Management
- Equipment Inventory
- Branch Management
- Financial Reports
- Notification System

## Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (optional)

## Setup

### Local Setup

1. **Clone repository**
   ```bash
   git clone <repo_url>
   cd gym-management-system/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Setup database**
   ```bash
   # Create database
   createdb -U postgres gym_management
   
   # Run migrations
   alembic upgrade head
   ```

6. **Run application**
   ```bash
   uvicorn app.main:app --reload
   ```

   Application will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access application**
   - API: `http://localhost:8000`
   - Database: `localhost:5432`
   - Redis: `localhost:6379`

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth_routes.py
│   │       ├── member_routes.py
│   │       ├── trainer_routes.py
│   │       ├── attendance_routes.py
│   │       ├── payment_routes.py
│   │       ├── workout_routes.py
│   │       ├── nutrition_routes.py
│   │       ├── branch_routes.py
│   │       └── class_routes.py
│   ├── core/
│   │   ├── constants.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── dependencies.py
│   ├── db/
│   │   ├── session.py
│   │   └── base.py
│   ├── models/
│   │   ├── user.py
│   │   ├── member.py
│   │   ├── trainer.py
│   │   ├── staff.py
│   │   ├── branch.py
│   │   ├── attendance.py
│   │   ├── workout.py
│   │   ├── nutrition.py
│   │   ├── payment.py
│   │   ├── inventory.py
│   │   ├── notification.py
│   │   └── class_model.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── member.py
│   │   ├── trainer.py
│   │   ├── attendance.py
│   │   ├── payment.py
│   │   ├── pagination.py
│   │   └── common.py
│   ├── utils/
│   │   ├── email.py
│   │   ├── file_handler.py
│   │   └── qrcode_generator.py
│   ├── config.py
│   └── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/refresh-token` - Refresh access token
- `POST /auth/change-password` - Change password
- `GET /auth/profile` - Get current user profile

### Members
- `GET /members` - List members
- `POST /members` - Create member
- `GET /members/{member_id}` - Get member details
- `PUT /members/{member_id}` - Update member
- `DELETE /members/{member_id}` - Delete member
- `GET /members/{member_id}/memberships` - Get member memberships

### Attendance
- `POST /attendance/checkin` - Check in member
- `POST /attendance/checkout` - Check out member
- `GET /attendance` - List attendance records
- `GET /attendance/daily-summary` - Get daily summary

### Payments
- `GET /payments` - List payments
- `POST /payments` - Create payment
- `GET /payments/{payment_id}` - Get payment details
- `POST /payments/{payment_id}/refund` - Refund payment
- `GET /payments/{payment_id}/invoice` - Get invoice

### Trainers
- `GET /trainers` - List trainers
- `POST /trainers` - Create trainer
- `GET /trainers/{trainer_id}` - Get trainer details
- `GET /trainers/{trainer_id}/performance` - Get performance metrics

### Workouts
- `GET /workouts/exercises` - List exercises
- `GET /workouts/plans/{member_id}` - Get workout plans
- `POST /workouts/plans` - Create workout plan
- `POST /workouts/progress/{member_id}` - Record body progress

### Nutrition
- `GET /nutrition/diet-plans/{member_id}` - Get diet plans
- `POST /nutrition/diet-plans` - Create diet plan
- `GET /nutrition/tracking/{diet_plan_id}` - Get nutrition tracking

### Branches
- `GET /branches` - List branches
- `GET /branches/{branch_id}` - Get branch details
- `GET /branches/{branch_id}/stats` - Get branch statistics

### Classes
- `GET /classes` - List classes
- `GET /classes/{class_id}` - Get class details
- `POST /classes/{class_id}/enroll` - Enroll in class

## Database Setup

### PostgreSQL Installation

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

### Create Database and User

```bash
sudo -u postgres psql

-- Create user
CREATE USER gym_user WITH PASSWORD 'gym_password';

-- Create database
CREATE DATABASE gym_management;

-- Grant privileges
ALTER ROLE gym_user SET client_encoding TO 'utf8';
ALTER ROLE gym_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE gym_user SET default_transaction_deferrable TO on;
ALTER ROLE gym_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE gym_management TO gym_user;

-- Exit
\q
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://gym_user:gym_password@localhost:5432/gym_management

# JWT
JWT_SECRET_KEY=your_secret_key_here_min_32_characters
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Environment
ENVIRONMENT=development
DEBUG=true
```

## Running Tests

```bash
pytest

# With coverage
pytest --cov=app --cov-report=html
```

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Development

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/

# Sort imports
isort app/
```

### Running in Development Mode

```bash
# With auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```bash
# Build image
docker build -t gym-management-api .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e JWT_SECRET_KEY="..." \
  gym-management-api
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
sudo service postgresql status

# Connect to database
psql -U gym_user -d gym_management -h localhost
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping

# Clear cache
redis-cli FLUSHALL
```

## Contributing

1. Create a feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Submit a pull request

## License

MIT License

## Support

For support, email support@gymsystem.local or create an issue in the repository.
