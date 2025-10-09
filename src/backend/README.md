# LinkedIn Networking App - Backend

This is the backend implementation for the LinkedIn Networking Application, built with a microservices architecture.

## Services

### User Service (Port 8001)
- User registration and authentication
- JWT token management
- User profile CRUD operations

### Profile Service (Port 8002)
- Resume upload and parsing
- LinkedIn profile data extraction
- Profile autofill from resume and LinkedIn

## Getting Started

### Prerequisites

```bash
# Python 3.9+
python --version

# PostgreSQL 13+
postgres --version

# Redis 6+
redis-server --version
```

### Installation

1. Install dependencies:
```bash
cd src/backend
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start database services (using Docker):
```bash
# From project root
docker-compose up -d postgres redis
```

4. Run database migrations:
```bash
# From project root
python scripts/migrate.py
```

### Running Services

#### Option 1: Run individual services
```bash
# User Service
python run_services.py user

# Profile Service (in another terminal)
python run_services.py profile
```

#### Option 2: Using Docker Compose
```bash
# From project root
docker-compose up user-service profile-service
```

## API Endpoints

### User Service (http://localhost:8001)

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

#### Profile Management
- `GET /api/profile/me` - Get current user's profile
- `POST /api/profile` - Create user profile
- `PUT /api/profile` - Update user profile
- `DELETE /api/profile` - Delete user profile

### Profile Service (http://localhost:8002)

#### Resume Management
- `POST /api/resume/upload` - Upload resume PDF
- `GET /api/resume/{resume_id}` - Get resume details
- `GET /api/resume` - Get all user resumes

#### LinkedIn Integration
- `POST /api/linkedin/extract` - Extract LinkedIn profile data
- `POST /api/profile/autofill` - Autofill profile from LinkedIn/resume

## API Usage Examples

### 1. Register a new user
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 2. Login and get token
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

### 3. Upload Resume
```bash
curl -X POST http://localhost:8002/api/resume/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@/path/to/resume.pdf"
```

### 4. Autofill Profile from LinkedIn and Resume
```bash
curl -X POST http://localhost:8002/api/profile/autofill \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "linkedin_url=https://linkedin.com/in/yourprofile" \
  -F "resume_id=1"
```

### 5. Create Profile with Autofilled Data
```bash
curl -X POST http://localhost:8001/api/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "headline": "Software Engineer",
    "location": "San Francisco, CA",
    "current_position": "Senior Software Engineer",
    "current_company": "Tech Corp",
    "industry": "Computer Software",
    "university": "Stanford University",
    "graduation_year": 2020,
    "major": "Computer Science",
    "grade": "3.8",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "skills": ["Python", "React", "AWS"],
    "interests": ["Machine Learning", "Web Development"]
  }'
```

## Database Models

### User
- Basic authentication and user management

### UserProfile
- Comprehensive user profile with:
  - Personal information (name, contact)
  - Professional details (position, company, industry)
  - Education (degree, university, graduation year, GPA)
  - LinkedIn integration
  - Skills and interests

### Resume
- Resume file metadata
- Parsed resume content
- Extracted information (skills, education, experience)

## Development

### Project Structure
```
src/backend/
├── shared/
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   └── schemas.py        # Pydantic schemas
├── services/
│   ├── user_service/
│   │   ├── main.py       # User service API
│   │   └── auth.py       # Authentication utilities
│   └── profile_service/
│       ├── main.py       # Profile service API
│       ├── resume_parser.py    # Resume parsing logic
│       ├── linkedin_scraper.py # LinkedIn data extraction
│       └── s3_client.py        # AWS S3 integration
├── requirements.txt
└── run_services.py
```

### Adding a New Service

1. Create service directory: `services/new_service/`
2. Create `main.py` with FastAPI app
3. Add models to `shared/models.py`
4. Add schemas to `shared/schemas.py`
5. Update `run_services.py`
6. Add Docker configuration

## Testing

```bash
# Run all tests
pytest

# Run specific service tests
pytest tests/test_user_service.py
pytest tests/test_profile_service.py

# Run with coverage
pytest --cov=services
```

## Important Notes

### LinkedIn Integration
The LinkedIn scraper currently returns mock data. For production:

1. **Option 1: LinkedIn Official API**
   - Register your app at https://www.linkedin.com/developers/
   - Implement OAuth 2.0 flow
   - Use official API endpoints

2. **Option 2: Third-party APIs**
   - Use RapidAPI LinkedIn services
   - Or similar authorized data providers

3. **Option 3: Manual Input**
   - Have users manually enter their information
   - Or import LinkedIn data export

**Important**: Direct web scraping of LinkedIn violates their Terms of Service.

### AWS S3 Configuration
Make sure to:
1. Create an S3 bucket
2. Set up IAM credentials with S3 access
3. Configure environment variables in `.env`

### Security
- Never commit `.env` file
- Use strong `SECRET_KEY` in production
- Enable HTTPS in production
- Implement rate limiting
- Validate all user inputs

## License
MIT
