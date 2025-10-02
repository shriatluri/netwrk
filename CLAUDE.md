# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LinkedIn networking application that helps users connect with relevant professionals at target companies by analyzing their LinkedIn profile, resume, and company preferences. The system uses ML-powered recommendations with a multi-factor scoring algorithm to suggest optimal connections.

## Architecture

### Microservices Architecture
The application is built using a microservices architecture with the following services:
- **API Gateway** (port 8000): Authentication, rate limiting, load balancing
- **User Service** (port 8001): User registration, authentication, profile management
- **Profile Service** (port 8002): LinkedIn profile processing, resume parsing
- **Company Service** (port 8003): Company data management, employee directory
- **Recommendation Service** (port 8004): ML-based connection suggestions
- **Connection Service** (port 8005): LinkedIn connection automation
- **Analytics Service** (port 8006): Usage analytics, success metrics

### Data Layer
- **PostgreSQL**: Primary database for structured data
- **Redis**: Caching layer for session management and API responses
- **Elasticsearch**: Search and recommendation indexing
- **S3**: File storage for resumes and documents

### External Dependencies
- **LinkedIn API**: Profile data and connection management
- **ML Services**: Recommendation engine and NLP processing

## Development Commands

### Environment Setup
```bash
# Start all services with Docker
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild containers
docker-compose build
```

### Database Management
```bash
# Run migrations
python scripts/migrate.py

# Seed database with test data
python scripts/seed.py
```

### Development Servers
```bash
# Start both backend and frontend in development mode
npm run dev

# Start backend only
npm run dev:backend

# Start frontend only
npm run dev:frontend

# Start mobile app
npm run dev:mobile
```

### Testing
```bash
# Run all tests
npm test

# Run backend tests
npm run test:backend

# Run frontend tests
npm run test:frontend

# Backend tests with pytest
cd src/backend && pytest tests/

# Integration tests
pytest tests/integration/
```

### Code Quality
```bash
# Run linters
npm run lint

# Run backend linter
npm run lint:backend

# Run frontend linter
npm run lint:frontend

# Format code with Prettier
npm run format
```

### Building
```bash
# Build both backend and frontend
npm run build

# Build backend only
npm run build:backend

# Build frontend only
npm run build:frontend
```

### Documentation
```bash
# Serve documentation locally
npm run docs:serve  # Available at http://localhost:8000

# Build documentation
npm run docs:build
```

## Recommendation Algorithm

The recommendation system uses a multi-factor scoring approach with the following weights:
- **Industry Alignment** (25%): Match user and target industries
- **Skill Compatibility** (20%): Analyze skills overlap
- **Experience Alignment** (15%): Match experience levels
- **Geographic Proximity** (10%): Consider location factors
- **Mutual Connections** (15%): Leverage network connections
- **Company Culture Fit** (10%): Align with company values
- **Seniority Compatibility** (5%): Match seniority levels

Scoring formula:
```
Total Score = (Industry Match × 0.3) +
              (Skill Overlap × 0.25) +
              (Experience Alignment × 0.2) +
              (Geographic Proximity × 0.1) +
              (Mutual Connections × 0.15)
```

The algorithm combines content-based filtering (profile and resume analysis), collaborative filtering (user behavior patterns), graph-based analysis (LinkedIn network), and machine learning models.

## API Architecture

All API endpoints are documented in `docs/api/api_specifications.md`. Key endpoint groups:
- `/api/auth/*` - LinkedIn OAuth authentication and token management
- `/api/profile/*` - User profile and resume management
- `/api/companies/*` - Company search and employee data
- `/api/recommendations/*` - Connection recommendations and analytics
- `/api/connections/*` - Connection request management
- `/api/analytics/*` - User and company analytics

Rate limits vary by endpoint type (see API docs for specifics).

## Security Considerations

- OAuth 2.0 for LinkedIn API authentication
- JWT tokens for session management
- End-to-end encryption for sensitive data
- GDPR/CCPA compliance with data protection
- Rate limiting per user/IP
- Input validation and sanitization
- Audit logging for security events

Always validate LinkedIn API terms of service compliance. Never commit secrets or credentials - use environment variables.

## Key Documentation

- `docs/architecture/system_design.md` - Complete system architecture and data models
- `docs/api/api_specifications.md` - REST API documentation with examples
- `docs/algorithms/algorithm_design.md` - Recommendation algorithm details
- `docs/security/security_considerations.md` - Security and privacy framework
- `CONTRIBUTING.md` - Development guidelines and PR process

## Prerequisites

- Node.js 16+
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose
