# Visual Workflow - LinkedIn Networking Application

This document provides visual representations of the application's workflows and architecture.

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                    │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐          │
│  │   Web App    │        │  Mobile App  │        │    Admin     │          │
│  │ (React/Vue)  │        │(React Native)│        │  Dashboard   │          │
│  └──────┬───────┘        └──────┬───────┘        └──────┬───────┘          │
└─────────┼──────────────────────┼──────────────────────┼──────────────────────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                                 ▼
          ┌────────────────────────────────────────────┐
          │          API GATEWAY (Port 8000)           │
          │    • Authentication & Authorization        │
          │    • Rate Limiting & Load Balancing       │
          │    • Request Routing                      │
          └────────────────┬───────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MICROSERVICES LAYER                                │
│                                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   User   │  │ Profile  │  │ Company  │  │Recommend │  │Connection│     │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │  │ Service  │     │
│  │ :8001    │  │ :8002    │  │ :8003    │  │ :8004    │  │ :8005    │     │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │
│       │             │             │             │             │            │
│  ┌────┴─────────────┴─────────────┴─────────────┴─────────────┴────┐      │
│  │                    Analytics Service (:8006)                      │      │
│  └───────────────────────────────┬───────────────────────────────────┘      │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
          ▼                          ▼                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA LAYER                                      │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│  │  PostgreSQL  │    │    Redis     │    │Elasticsearch │                  │
│  │   :5432      │    │    :6379     │    │    :9200     │                  │
│  │              │    │              │    │              │                  │
│  │ • User Data  │    │ • Sessions   │    │ • Search     │                  │
│  │ • Profiles   │    │ • Cache      │    │ • Indexing   │                  │
│  │ • Companies  │    │ • Queue      │    │ • Analytics  │                  │
│  │ • Analytics  │    │              │    │              │                  │
│  └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                                                              │
│  ┌──────────────┐                                                           │
│  │   AWS S3     │                                                           │
│  │              │                                                           │
│  │ • Resumes    │                                                           │
│  │ • Documents  │                                                           │
│  └──────────────┘                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
          ▲                          ▲
          │                          │
┌─────────┴──────────┐    ┌──────────┴─────────┐
│   LinkedIn API     │    │    ML Services     │
│                    │    │                    │
│ • Profile Data     │    │ • Recommendation   │
│ • Connections      │    │ • NLP Processing   │
│ • OAuth            │    │ • Pattern Analysis │
└────────────────────┘    └────────────────────┘
```

## Complete User Workflow

```
                                  START
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   User Visits Application     │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Click "Connect with LinkedIn"│
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │  Redirect to LinkedIn OAuth   │
                    │  • User Authorizes App        │
                    │  • LinkedIn Returns Auth Code │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │   Exchange Code for Token     │
                    │   (API Gateway → User Service)│
                    └───────────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐     ┌─────────────────┐    ┌─────────────────┐
    │ Fetch LinkedIn│     │  Store User     │    │  Generate JWT   │
    │ Profile Data  │     │  Profile in DB  │    │  Access Token   │
    └───────┬───────┘     └─────────┬───────┘    └─────────┬───────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │  User Logged In Successfully  │
                    │  Redirect to Dashboard        │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   Upload Resume (Optional)    │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │  Resume Parsing & Analysis    │
                    │  • Extract Skills             │
                    │  • Parse Experience           │
                    │  • Store in S3 + Database     │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │   Search for Companies        │
                    │   • Search by Industry        │
                    │   • Filter by Location/Size   │
                    └───────────────┬───────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐     ┌─────────────────┐    ┌─────────────────┐
    │Query Postgres │     │ Search Elastic  │    │  Return Company │
    │ Company Data  │     │ for Indexed Cos │    │  List to User   │
    └───────┬───────┘     └─────────┬───────┘    └─────────┬───────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │   User Selects Company        │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Get Recommendations          │
                    │  (Recommendation Service)     │
                    └───────────────┬───────────────┘
                                    │
                    ┌───────────────▼───────────────┐
                    │   ML RECOMMENDATION ENGINE    │
                    │                               │
                    │   ┌─────────────────────┐     │
                    │   │ Fetch User Profile  │     │
                    │   │ + Resume Data       │     │
                    │   └──────────┬──────────┘     │
                    │              │                │
                    │   ┌──────────▼──────────┐     │
                    │   │ Fetch Company       │     │
                    │   │ Employees from DB   │     │
                    │   └──────────┬──────────┘     │
                    │              │                │
                    │   ┌──────────▼──────────┐     │
                    │   │ Calculate Scores:   │     │
                    │   │ • Industry (25%)    │     │
                    │   │ • Skills (20%)      │     │
                    │   │ • Experience (15%)  │     │
                    │   │ • Location (10%)    │     │
                    │   │ • Mutual Conn (15%) │     │
                    │   │ • Culture (10%)     │     │
                    │   │ • Seniority (5%)    │     │
                    │   └──────────┬──────────┘     │
                    │              │                │
                    │   ┌──────────▼──────────┐     │
                    │   │ Rank & Sort by      │     │
                    │   │ Total Match Score   │     │
                    │   └──────────┬──────────┘     │
                    │              │                │
                    │   ┌──────────▼──────────┐     │
                    │   │ Cache Results       │     │
                    │   │ in Redis            │     │
                    │   └──────────┬──────────┘     │
                    └──────────────┼────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Display Top Recommendations │
                    │ • Person Name & Title       │
                    │ • Match Score & Reasoning   │
                    │ • Mutual Connections        │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ User Selects Person to      │
                    │ Connect With                │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Compose Connection Message  │
                    │ (Optional Personal Note)    │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Send Connection Request     │
                    │ (Connection Service)        │
                    └──────────────┬──────────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
    ┌───────────────┐     ┌────────────────┐    ┌────────────────┐
    │ Call LinkedIn │     │ Store Request  │    │ Update User    │
    │ API to Send   │     │ in Database    │    │ Analytics      │
    │ Connection    │     │ (Status: Pending)│   │                │
    └───────┬───────┘     └────────┬───────┘    └────────┬───────┘
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │ Show Success Confirmation   │
                    │ • Track in Analytics        │
                    │ • Monitor Connection Status │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ User Views Analytics Dashboard│
                    │ • Connection Success Rate    │
                    │ • Top Industries             │
                    │ • Monthly Stats              │
                    │ • Company Breakdown          │
                    └──────────────────────────────┘
                                   │
                                   ▼
                                  END
```

## Authentication Flow Detail

```
┌─────────┐                   ┌──────────┐                 ┌─────────────┐
│         │                   │          │                 │             │
│  User   │                   │   App    │                 │  LinkedIn   │
│ Browser │                   │  Server  │                 │    OAuth    │
│         │                   │          │                 │             │
└────┬────┘                   └────┬─────┘                 └──────┬──────┘
     │                             │                              │
     │  1. Click Login             │                              │
     ├────────────────────────────►│                              │
     │                             │                              │
     │  2. Redirect to LinkedIn    │                              │
     │◄────────────────────────────┤                              │
     │                             │                              │
     │  3. Authorize App                                          │
     ├────────────────────────────────────────────────────────────►
     │                             │                              │
     │  4. Redirect with Auth Code │                              │
     │◄────────────────────────────────────────────────────────────┤
     │                             │                              │
     │  5. Send Auth Code          │                              │
     ├────────────────────────────►│                              │
     │                             │                              │
     │                             │  6. Exchange Code for Token  │
     │                             ├─────────────────────────────►│
     │                             │                              │
     │                             │  7. Return Access Token      │
     │                             │◄─────────────────────────────┤
     │                             │                              │
     │                             │  8. Fetch Profile Data       │
     │                             ├─────────────────────────────►│
     │                             │                              │
     │                             │  9. Return Profile           │
     │                             │◄─────────────────────────────┤
     │                             │                              │
     │                        ┌────▼────┐                         │
     │                        │ Store:  │                         │
     │                        │ • User  │                         │
     │                        │ • Token │                         │
     │                        │ • Profile                         │
     │                        └────┬────┘                         │
     │                             │                              │
     │  10. Return JWT Token       │                              │
     │◄────────────────────────────┤                              │
     │                             │                              │
     │  11. Subsequent API Calls   │                              │
     │     (Authorization: Bearer) │                              │
     ├────────────────────────────►│                              │
     │                             │                              │
```

## Recommendation Algorithm Flow

```
                        ┌─────────────────────┐
                        │  Start: Get Recs    │
                        │  for Company X      │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   Check Redis Cache         │
                    │   Key: user:{id}:recs:{cid} │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │      Cache Hit?             │
                    └─┬───────────────────────┬───┘
                      │ Yes                   │ No
                      │                       │
            ┌─────────▼─────────┐            │
            │ Return Cached     │            │
            │ Recommendations   │            │
            └─────────┬─────────┘            │
                      │                      │
                      │         ┌────────────▼────────────┐
                      │         │ Fetch Data from DB:     │
                      │         │ • User Profile          │
                      │         │ • User Resume           │
                      │         │ • Company Employees     │
                      │         │ • User's Connections    │
                      │         └────────────┬────────────┘
                      │                      │
                      │         ┌────────────▼────────────┐
                      │         │ For Each Employee:      │
                      │         │ Calculate Sub-Scores    │
                      │         └────────────┬────────────┘
                      │                      │
                      │         ┌────────────▼─────────────────────────────┐
                      │         │                                          │
                      │         │  ┌─────────────────────────────────┐    │
                      │         │  │ 1. Industry Match (25%)         │    │
                      │         │  │    • Compare industries         │    │
                      │         │  │    • Score: 0.0 - 1.0          │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         │  ┌────────────▼────────────────────┐    │
                      │         │  │ 2. Skill Overlap (20%)          │    │
                      │         │  │    • Jaccard similarity         │    │
                      │         │  │    • Common skills / All skills │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         │  ┌────────────▼────────────────────┐    │
                      │         │  │ 3. Experience Level (15%)       │    │
                      │         │  │    • Years experience delta     │    │
                      │         │  │    • Normalize 0.0 - 1.0       │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         │  ┌────────────▼────────────────────┐    │
                      │         │  │ 4. Geographic Proximity (10%)   │    │
                      │         │  │    • Same city: 1.0            │    │
                      │         │  │    • Same state: 0.7           │    │
                      │         │  │    • Same country: 0.4         │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         │  ┌────────────▼────────────────────┐    │
                      │         │  │ 5. Mutual Connections (15%)     │    │
                      │         │  │    • Graph query for common     │    │
                      │         │  │    • Normalize by network size  │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         │  ┌────────────▼────────────────────┐    │
                      │         │  │ 6. Culture Fit (10%)            │    │
                      │         │  │    • NLP on profile text        │    │
                      │         │  │    • Company values match       │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         │  ┌────────────▼────────────────────┐    │
                      │         │  │ 7. Seniority Match (5%)         │    │
                      │         │  │    • Title/level comparison     │    │
                      │         │  │    • Appropriate reach-out      │    │
                      │         │  └────────────┬────────────────────┘    │
                      │         │               │                         │
                      │         └───────────────┼─────────────────────────┘
                      │                         │
                      │         ┌───────────────▼────────────┐
                      │         │ Calculate Total Score:     │
                      │         │                            │
                      │         │ score = (industry × 0.25)  │
                      │         │       + (skills × 0.20)    │
                      │         │       + (experience × 0.15)│
                      │         │       + (location × 0.10)  │
                      │         │       + (mutual × 0.15)    │
                      │         │       + (culture × 0.10)   │
                      │         │       + (seniority × 0.05) │
                      │         └───────────────┬────────────┘
                      │                         │
                      │         ┌───────────────▼────────────┐
                      │         │ Filter: score > threshold  │
                      │         │ (default: 0.6)             │
                      │         └───────────────┬────────────┘
                      │                         │
                      │         ┌───────────────▼────────────┐
                      │         │ Sort by Total Score DESC   │
                      │         │ Limit to Top N (default 50)│
                      │         └───────────────┬────────────┘
                      │                         │
                      │         ┌───────────────▼────────────┐
                      │         │ Enrich with:               │
                      │         │ • Profile pictures         │
                      │         │ • Reasoning breakdown      │
                      │         │ • Mutual connection count  │
                      │         └───────────────┬────────────┘
                      │                         │
                      │         ┌───────────────▼────────────┐
                      │         │ Cache in Redis             │
                      │         │ TTL: 24 hours              │
                      │         └───────────────┬────────────┘
                      │                         │
                      └─────────────────────────┘
                                                │
                                ┌───────────────▼────────────┐
                                │ Return Recommendations     │
                                │ to User                    │
                                └────────────────────────────┘
```

## Data Flow - Connection Request

```
┌──────────┐     1. POST /api/connections/send      ┌─────────────┐
│          │────────────────────────────────────────►│             │
│  Client  │                                         │ API Gateway │
│          │◄────────────────────────────────────────│             │
└──────────┘     2. Validate JWT & Rate Limit       └──────┬──────┘
                                                             │
                                        3. Route to Service │
                                                             ▼
                                                    ┌─────────────────┐
                                                    │   Connection    │
                                                    │    Service      │
                                                    └────────┬────────┘
                                                             │
                    ┌────────────────────────────────────────┼───────────────┐
                    │                                        │               │
         4. Validate│Input                       5. Check   │    6. Call    │
                    ▼                            Rate Limit │    LinkedIn   │
            ┌───────────────┐                               │    API        │
            │ Validation:   │                               ▼               ▼
            │ • Person ID   │                      ┌─────────────┐  ┌────────────┐
            │ • Message     │                      │    Redis    │  │  LinkedIn  │
            │ • User Auth   │                      │             │  │    API     │
            └───────┬───────┘                      │ Check user: │  │            │
                    │                              │ • 20 req/hr │  │ Send conn  │
                    │                              │ • Increment │  │ request    │
                    │                              └──────┬──────┘  └─────┬──────┘
                    │                                     │               │
                    │                                     │               │
                    └─────────────────┬───────────────────┘               │
                                      │                                   │
                           7. Store in Database                           │
                                      ▼                                   │
                            ┌──────────────────┐                          │
                            │   PostgreSQL     │                          │
                            │                  │                          │
                            │ INSERT INTO      │                          │
                            │ connections:     │                          │
                            │ • id             │                          │
                            │ • user_id        │                          │
                            │ • target_id      │                          │
                            │ • status: pending│                          │
                            │ • message        │                          │
                            │ • sent_at        │                          │
                            └──────────┬───────┘                          │
                                      │                                   │
                    ┌─────────────────┴───────────────────────────────────┘
                    │
         8. Update Analytics
                    ▼
          ┌──────────────────┐
          │ Analytics Service│
          │                  │
          │ • Increment sent │
          │ • Track by comp. │
          │ • Update metrics │
          └──────────┬───────┘
                    │
         9. Return Success
                    ▼
            ┌───────────────┐
            │   Response:   │
            │               │
            │ {             │
            │   success: ✓  │
            │   conn_id: X  │
            │   status: ... │
            │ }             │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │  Show in UI   │
            │  • Success    │
            │  • Track stat │
            └───────────────┘
```

## Service Communication Pattern

```
                    ┌─────────────────────────────────┐
                    │       API GATEWAY               │
                    │   Receives all client requests  │
                    └───────────────┬─────────────────┘
                                    │
                                    │ Routes based on endpoint
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐      ┌────────────────┐     ┌────────────────┐
    │ User Service  │      │Profile Service │     │Company Service │
    │               │      │                │     │                │
    │ ┌───────────┐ │      │ ┌────────────┐ │     │ ┌────────────┐ │
    │ │ REST API  │ │      │ │  REST API  │ │     │ │  REST API  │ │
    │ └─────┬─────┘ │      │ └──────┬─────┘ │     │ └──────┬─────┘ │
    │       │       │      │        │       │     │        │       │
    │ ┌─────▼─────┐ │      │ ┌──────▼─────┐ │     │ ┌──────▼─────┐ │
    │ │ Business  │ │      │ │  Business  │ │     │ │  Business  │ │
    │ │  Logic    │ │      │ │   Logic    │ │     │ │   Logic    │ │
    │ └─────┬─────┘ │      │ └──────┬─────┘ │     │ └──────┬─────┘ │
    │       │       │      │        │       │     │        │       │
    │ ┌─────▼─────┐ │      │ ┌──────▼─────┐ │     │ ┌──────▼─────┐ │
    │ │   Data    │ │      │ │   Data     │ │     │ │   Data     │ │
    │ │  Access   │ │      │ │  Access    │ │     │ │  Access    │ │
    │ └─────┬─────┘ │      │ └──────┬─────┘ │     │ └──────┬─────┘ │
    └───────┼───────┘      └────────┼───────┘     └────────┼───────┘
            │                       │                      │
            └───────────────────────┼──────────────────────┘
                                    │
                    ┌───────────────▼────────────────┐
                    │    Shared Data Layer:          │
                    │  • PostgreSQL (structured)     │
                    │  • Redis (cache/sessions)      │
                    │  • Elasticsearch (search)      │
                    │  • S3 (file storage)           │
                    └────────────────────────────────┘

Each service:
• Independently deployable
• Owns its domain logic
• Communicates via REST APIs
• Shares common data layer
• Can be scaled independently
```

## Monitoring & Observability

```
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVICES                          │
│  User │ Profile │ Company │ Recommend │ Connection │ Analytics  │
└───┬───────┬────────┬───────────┬────────────┬───────────┬───────┘
    │       │        │           │            │           │
    │       │        │           │            │           │
    │  Metrics       │           │            │           │
    │  Logs          │           │            │           │
    │  Traces        │           │            │           │
    │       │        │           │            │           │
    └───────┴────────┴───────────┴────────────┴───────────┘
                     │
                     ▼
    ┌────────────────────────────────────────────────────┐
    │              MONITORING STACK                      │
    │                                                    │
    │  ┌──────────────┐    ┌──────────────┐            │
    │  │  Prometheus  │    │   Grafana    │            │
    │  │    :9090     │───►│    :3001     │            │
    │  │              │    │              │            │
    │  │ • Metrics    │    │ • Dashboards │            │
    │  │ • Time-series│    │ • Alerts     │            │
    │  │ • Alerts     │    │ • Visualize  │            │
    │  └──────────────┘    └──────────────┘            │
    │                                                   │
    │  ┌───────────────────────────────────────────┐   │
    │  │           ELK Stack                       │   │
    │  │                                           │   │
    │  │  ┌─────────────┐   ┌─────────────┐       │   │
    │  │  │Elasticsearch│◄──│  Logstash   │       │   │
    │  │  └──────┬──────┘   └──────▲──────┘       │   │
    │  │         │                 │              │   │
    │  │         ▼                 │              │   │
    │  │  ┌─────────────┐          │              │   │
    │  │  │   Kibana    │    ┌─────┴─────┐        │   │
    │  │  │             │    │   Logs    │        │   │
    │  │  │ • Search    │    │   from    │        │   │
    │  │  │ • Analyze   │    │  Services │        │   │
    │  │  │ • Visualize │    └───────────┘        │   │
    │  │  └─────────────┘                         │   │
    │  └───────────────────────────────────────────┘   │
    └────────────────────────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │   Alerting Channels    │
            │                        │
            │  • Email               │
            │  • Slack               │
            │  • PagerDuty           │
            │  • SMS                 │
            └────────────────────────┘
```

