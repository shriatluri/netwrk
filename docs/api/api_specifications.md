# LinkedIn Networking Application - API Specifications

## 1. Authentication APIs

### 1.1 LinkedIn OAuth Authentication
```http
POST /api/auth/linkedin
Content-Type: application/json

{
  "code": "string",
  "state": "string",
  "redirect_uri": "string"
}
```

**Response:**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "string",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "email": "string",
    "linkedin_id": "string",
    "name": "string",
    "profile_picture": "string"
  }
}
```

### 1.2 Token Refresh
```http
POST /api/auth/refresh
Authorization: Bearer {refresh_token}
```

### 1.3 Logout
```http
POST /api/auth/logout
Authorization: Bearer {access_token}
```

## 2. Profile Management APIs

### 2.1 Get User Profile
```http
GET /api/profile
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "uuid",
  "email": "string",
  "linkedin_profile": {
    "name": "string",
    "headline": "string",
    "industry": "string",
    "location": "string",
    "summary": "string",
    "experience": [
      {
        "title": "string",
        "company": "string",
        "duration": "string",
        "description": "string"
      }
    ],
    "education": [
      {
        "school": "string",
        "degree": "string",
        "field": "string",
        "year": "number"
      }
    ],
    "skills": ["string"]
  },
  "resume_data": {
    "file_url": "string",
    "parsed_content": {
      "skills": ["string"],
      "experience": ["string"],
      "education": ["string"]
    }
  },
  "preferences": {
    "target_companies": ["string"],
    "connection_goals": "string",
    "industry_focus": ["string"]
  }
}
```

### 2.2 Update Profile
```http
PUT /api/profile
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "preferences": {
    "target_companies": ["string"],
    "connection_goals": "string",
    "industry_focus": ["string"]
  }
}
```

### 2.3 Upload Resume
```http
POST /api/profile/resume
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

{
  "file": "binary_data"
}
```

**Response:**
```json
{
  "success": true,
  "file_url": "string",
  "parsed_content": {
    "skills": ["string"],
    "experience": ["string"],
    "education": ["string"]
  }
}
```

## 3. Company APIs

### 3.1 Search Companies
```http
GET /api/companies/search?q={query}&industry={industry}&location={location}&size={size}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "companies": [
    {
      "id": "uuid",
      "name": "string",
      "industry": "string",
      "size": "string",
      "location": "string",
      "linkedin_company_id": "string",
      "description": "string",
      "website": "string",
      "employee_count": "number"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number"
}
```

### 3.2 Get Company Details
```http
GET /api/companies/{company_id}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "string",
  "industry": "string",
  "size": "string",
  "location": "string",
  "description": "string",
  "website": "string",
  "employee_count": "number",
  "employees": [
    {
      "linkedin_id": "string",
      "name": "string",
      "position": "string",
      "department": "string",
      "seniority_level": "string",
      "profile_picture": "string",
      "connection_score": "float"
    }
  ]
}
```

## 4. Recommendation APIs

### 4.1 Get Recommendations
```http
GET /api/recommendations/{company_id}?limit={limit}&min_score={min_score}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "recommendations": [
    {
      "id": "uuid",
      "target_person": {
        "linkedin_id": "string",
        "name": "string",
        "position": "string",
        "company": "string",
        "profile_picture": "string",
        "headline": "string"
      },
      "match_score": "float",
      "reasoning": [
        {
          "factor": "string",
          "score": "float",
          "description": "string"
        }
      ],
      "connection_status": "string",
      "mutual_connections": "number"
    }
  ],
  "total": "number",
  "company": {
    "id": "uuid",
    "name": "string"
  }
}
```

### 4.2 Refresh Recommendations
```http
POST /api/recommendations/refresh
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "company_id": "uuid",
  "force_update": "boolean"
}
```

### 4.3 Get Recommendation Analytics
```http
GET /api/recommendations/analytics
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "total_recommendations": "number",
  "successful_connections": "number",
  "connection_rate": "float",
  "top_industries": [
    {
      "industry": "string",
      "count": "number"
    }
  ],
  "success_by_company": [
    {
      "company": "string",
      "connection_rate": "float"
    }
  ]
}
```

## 5. Connection Management APIs

### 5.1 Send Connection Request
```http
POST /api/connections/send
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "target_person_id": "string",
  "message": "string",
  "recommendation_id": "uuid"
}
```

**Response:**
```json
{
  "success": true,
  "connection_id": "uuid",
  "status": "pending",
  "message": "Connection request sent successfully"
}
```

### 5.2 Get Connection Status
```http
GET /api/connections/status?status={status}&limit={limit}&offset={offset}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "connections": [
    {
      "id": "uuid",
      "target_person": {
        "name": "string",
        "position": "string",
        "company": "string",
        "profile_picture": "string"
      },
      "status": "string",
      "sent_at": "timestamp",
      "responded_at": "timestamp",
      "message": "string"
    }
  ],
  "total": "number",
  "page": "number",
  "limit": "number"
}
```

### 5.3 Accept Connection Request
```http
POST /api/connections/accept
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "connection_id": "uuid"
}
```

## 6. Analytics APIs

### 6.1 Get User Analytics
```http
GET /api/analytics/user
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "profile_completeness": "float",
  "total_connections_sent": "number",
  "successful_connections": "number",
  "connection_rate": "float",
  "top_industries": [
    {
      "industry": "string",
      "count": "number"
    }
  ],
  "monthly_stats": [
    {
      "month": "string",
      "connections_sent": "number",
      "connections_accepted": "number"
    }
  ]
}
```

### 6.2 Get Company Analytics
```http
GET /api/analytics/company/{company_id}
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "company": {
    "id": "uuid",
    "name": "string"
  },
  "total_employees": "number",
  "connections_attempted": "number",
  "successful_connections": "number",
  "connection_rate": "float",
  "top_departments": [
    {
      "department": "string",
      "connection_rate": "float"
    }
  ],
  "seniority_breakdown": [
    {
      "level": "string",
      "count": "number",
      "connection_rate": "float"
    }
  ]
}
```

## 7. Error Responses

### 7.1 Standard Error Format
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "string",
    "timestamp": "timestamp"
  }
}
```

### 7.2 Common Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error
- `503` - Service Unavailable

## 8. Rate Limiting

### 8.1 Rate Limits
- **Authentication**: 10 requests per minute
- **Profile APIs**: 100 requests per hour
- **Company APIs**: 200 requests per hour
- **Recommendation APIs**: 50 requests per hour
- **Connection APIs**: 20 requests per hour
- **Analytics APIs**: 30 requests per hour

### 8.2 Rate Limit Headers
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 9. Webhooks

### 9.1 Connection Status Webhook
```http
POST /webhooks/connection-status
Content-Type: application/json

{
  "event": "connection.status_changed",
  "data": {
    "connection_id": "uuid",
    "user_id": "uuid",
    "target_person_id": "string",
    "status": "accepted|declined|pending",
    "timestamp": "timestamp"
  }
}
```

### 9.2 LinkedIn API Webhook
```http
POST /webhooks/linkedin
Content-Type: application/json

{
  "event": "linkedin.connection_accepted",
  "data": {
    "user_id": "uuid",
    "connection_id": "string",
    "timestamp": "timestamp"
  }
}
```

## 10. SDK Examples

### 10.1 JavaScript SDK
```javascript
import { LinkedInNetworkingAPI } from '@linkedin-networking/sdk';

const api = new LinkedInNetworkingAPI({
  baseURL: 'https://api.linkedin-networking.com',
  apiKey: 'your-api-key'
});

// Get recommendations
const recommendations = await api.recommendations.get('company-id');

// Send connection request
const connection = await api.connections.send({
  target_person_id: 'linkedin-id',
  message: 'Hi, I would like to connect!'
});
```

### 10.2 Python SDK
```python
from linkedin_networking import LinkedInNetworkingAPI

api = LinkedInNetworkingAPI(
    base_url='https://api.linkedin-networking.com',
    api_key='your-api-key'
)

# Get recommendations
recommendations = api.recommendations.get('company-id')

# Send connection request
connection = api.connections.send(
    target_person_id='linkedin-id',
    message='Hi, I would like to connect!'
)
```

---

*This API specification provides comprehensive documentation for all endpoints in the LinkedIn networking application. Regular updates are recommended as new features are added.*
