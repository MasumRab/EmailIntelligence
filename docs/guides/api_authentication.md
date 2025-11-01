# API Authentication Guide

This document explains how to authenticate with the Email Intelligence Platform API.

## Authentication Overview

The Email Intelligence Platform uses JWT (JSON Web Token) based authentication to secure API endpoints. All sensitive operations require a valid access token.

## Getting an Access Token

### Method 1: Using the Login Endpoint

To obtain an access token, make a POST request to the login endpoint:

```
POST /api/auth/login
```

**Request Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Method 2: Using the Legacy Token Endpoint

For backward compatibility, you can also use the legacy token endpoint:

```
POST /token
```

**Request Parameters:**
- `username`: Your username
- `password`: Your password

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Using the Access Token

Once you have obtained an access token, include it in the Authorization header of your requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Registering a New User

To register a new user, make a POST request to the register endpoint:

```
POST /api/auth/register
```

**Request Body:**
```json
{
  "username": "new_username",
  "password": "new_password"
}
```

## Protected Endpoints

All endpoints that modify data or access sensitive information require authentication. This includes:

- Email management endpoints (`/api/emails/*`)
- Category management endpoints (`/api/categories/*`)
- AI analysis endpoints (`/api/ai/*`)
- Workflow management endpoints (`/api/workflows/*`)
- Filter management endpoints (`/api/filters/*`)
- Model management endpoints (`/api/models/*`)
- Training endpoints (`/api/training/*`)
- Dashboard endpoints (`/api/dashboard/*`)

## Token Expiration

Access tokens have a default expiration time of 30 minutes. When a token expires, you will receive a 401 Unauthorized response. To get a new token, repeat the login process.

## Example Usage

### 1. Login and Get Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### 2. Use Token to Access Protected Endpoint

```bash
curl -X GET "http://localhost:8000/api/emails" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Error Responses

When authentication fails, you will receive one of the following responses:

**401 Unauthorized:**
```json
{
  "detail": "Could not validate credentials"
}
```

**401 Unauthorized (Incorrect credentials):**
```json
{
  "detail": "Incorrect username or password"
}
```

**400 Bad Request (User already exists):**
```json
{
  "detail": "User already exists"
}
```