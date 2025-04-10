# Bruce Tech Lead Assignment

This project implements a microservices architecture with three core services (Organization, Feedback, and Member) and an Nginx Gateway for unified API access. Organization is an extra service acting as a source of truth for Feedback and Member services

## Architecture Overview

- **Gateway Service**: Nginx-based API gateway that routes requests to appropriate services
- **Organization Service**: Manages organization information (source of truth for organization data)
- **Feedback Service**: Handles user feedback related to organizations
- **Member Service**: Manages members associated with organizations

## Setup Instructions

### Prerequisites

- Docker and Docker Compose

### Step 1: Environment Configuration

The project uses environment variables defined in the `.env` file. A default configuration is provided, but you can modify it if needed:

```bash
# Feedback Database Config
FEEDBACK_POSTGRES_USER=postgres
FEEDBACK_POSTGRES_PASSWORD=postgres
FEEDBACK_POSTGRES_DB=feedback_db
FEEDBACK_POSTGRES_PORT=5432
FEEDBACK_DB_HOST=feedback-db

# Member Database Config
MEMBER_POSTGRES_USER=postgres
MEMBER_POSTGRES_PASSWORD=postgres
MEMBER_POSTGRES_DB=member_db
MEMBER_POSTGRES_PORT=5432
MEMBER_DB_HOST=member-db

# Service Ports
ORGANIZATION_SERVICE_PORT=18000
FEEDBACK_SERVICE_PORT=18001
MEMBER_SERVICE_PORT=18002

# Service URLs
ORGANIZATION_SERVICE_URL=http://organization-service:${ORGANIZATION_SERVICE_PORT}/api/v1/organizations

# Gateway Service
GATEWAY_EXTERNAL_PORT=8080
```

### Step 2: Start the Services

Launch the entire application stack using Docker Compose:

```bash
docker compose -f compose.dev.yaml up -d
```

This will start:

- Organization Service
- Feedback Service with its own PostgreSQL database
- Member Service with its own PostgreSQL database
- The API Gateway (Nginx)

### Step 3: Verify Services

Check if all services are running:

```bash
docker ps
```

## How to Run Tests

The project includes automated tests for each service.

### Run All Tests

```bash
docker compose -f compose.test.yaml up
```

### Run Tests for a Specific Service

```bash
# Run Feedback service tests
docker compose -f compose.test.yaml run --rm feedback-test

# Run Member service tests
docker compose -f compose.test.yaml run --rm member-test
```

## How to Access APIs

### API Gateway

The API gateway, backed by Nginx, routes requests to the appropriate services. All endpoints are accessible through:

```
http://localhost:8080/api/v1/...
```

### API Endpoints

#### Organization Service
- `GET /api/v1/organizations/{organization_id}` - Get organization details
- `GET /api/v1/organizations/{organization_id}/exists` - Check if organization exists

#### Feedback Service
- `POST /api/v1/organizations/{organization_id}/feedbacks` - Create feedback
- `GET /api/v1/organizations/{organization_id}/feedbacks` - Get all feedbacks
- `DELETE /api/v1/organizations/{organization_id}/feedbacks` - Delete all feedbacks

#### Member Service
- `POST /api/v1/organizations/{organization_id}/members` - Create member
- `GET /api/v1/organizations/{organization_id}/members` - Get all members
- `DELETE /api/v1/organizations/{organization_id}/members` - Delete all members


## How to Access APIs Documentation

### API Documentation

Access the API documentation selector:

```
http://localhost:8080/api-docs
```

From there, you can view documentation for each service, or access directly to service documentation as below:

- Organization Service: [http://localhost:8080/organization-docs](http://localhost:8080/organization-docs)
- Feedback Service: [http://localhost:8080/feedback-docs](http://localhost:8080/feedback-docs)
- Member Service: [http://localhost:8080/member-docs](http://localhost:8080/member-docs)


## How to Seed Sample Data

### Organization Service

Sample organizations are loaded from  `dummy.json` with the following data:

- Organization ID: 1, Name: "TalentAdore"
- Organization ID: 2, Name: "Bruce Nguyen"

You can modify the JSON file if needed

### Feedback & Member Services

These services are configured to *automatically* seed sample data when they start. This is handled by the `seed_feedbacks()` and `seed_members()` functions that run on service startup.