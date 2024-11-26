# 🎉 Auth and Profile Management Service API Overview 🎉

This is a backend service for authentication and profile management built using FastAPI. The application handles:

- ✅ User registration with email verification.
- 🔒 Secure login with token generation.
- 🔄 Password reset functionality.
- 🧑‍💻 User profile management, including email verification.

---

## 📂 Project Structure

### Key Files and Their Roles 🗂️

- `auth_service.py`: Handles authentication business logic.
- `auth_controller.py`: Manages API endpoints for authentication.
- `profile_service.py`: Deals with profile-related logic.
- `profile_controller.py`: Manages API endpoints for user profiles.
- `config/db.py`: Sets up the database connection using MongoDB.
- `utils/`: Helper functions and utilities:
  - `error_handler.py`: Custom error responses. 🚨
  - `password_crypt.py`: Password hashing and verification. 🔑
  - `email_conf.py`: Sends email notifications. 📧
  - `oauth2.py`: JWT token creation and verification. 🎟️
- `schemas/user_serializer.py`: Serializes database user data into JSON format. 🗃️

---

## 🌟 Environment Variables

Ensure you have the following environment variables set up. No shortcuts here! 🛠️

<pre>MONGO_URI=<Your MongoDB connection URI> SECRET_KEY=<Your JWT secret key> ALGORITHM=<Your JWT algorithm> EMAIL_HOST=<Email host> EMAIL_PORT=<Email port> MAIL_SERVER=<Email server> EMAIL_USER=<Email username> EMAIL_PASSWORD=<Email password></pre>

---

## 🔑 Authentication Endpoints

### 1. 🚀 Register User

Registers a new user and sends a verification email.

**Endpoint:** `POST /api/auth/register`

**Request Body:**

```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "securepassword"
}
```

**Response**

```json
{
  "id": "user_id",
  "username": "john_doe",
  "email": "john.doe@example.com",
  "verified": false
}
```

### 2. 🔓 Login User

Logs in a user and generates access and refresh tokens.

**Endpoint:** POST /api/auth/login

**Request Body (Form):**

username: john.doe@example.com
password: securepassword

**Response**

```json
{
  "user": {
    "id": "user_id",
    "username": "john_doe",
    "email": "john.doe@example.com"
  },
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token"
}
```

## 3. 📧 Request Password Reset Code

Sends a password reset code to the user's email.

**Endpoint:** POST /api/auth/forgot-password/get-code

**Request Body:**

```json
{
  "email": "john.doe@example.com"
}
```

**Response:**

```json
{
  "message": "Password reset code was sent to the provided email"
}
```

## 4. 🔄 Reset Password

Resets the user's password using the code.

**Endpoint:** PUT /api/auth/forgot-password/

**Request Body:**

```json
{
  "email": "john.doe@example.com",
  "code": "123456",
  "password": "new_secure_password"
}
```

**Response:**

```json
{
  "message": "Password reset was successful",
  "profile": {
    "id": "user_id",
    "username": "john_doe",
    "email": "john.doe@example.com",
    "verified": false
  }
}
```

## 🧑‍💼 Profile Management Endpoints

## 1. ✅ Verify Email

Verifies a user's email using a code.

**Endpoint:** POST /api/profile/verify/{code}

**Headers:**

Authorization: Bearer <access_token>

**Response:**

```json
{
  "message": "Email is successfully verified",
  "profile": {
    "id": "user_id",
    "username": "john_doe",
    "email": "john.doe@example.com",
    "verified": true
  }
}
```

## 2. 📄 Get Profile

Fetches the profile of the authenticated user.

**Endpoint:** POST /api/profile/profile

**Headers:**

Authorization: Bearer <access_token>
Response:

```json
{
  "id": "user_id",
  "username": "john_doe",
  "email": "john.doe@example.com",
  "verified": true
}
```

## 🛠️ Testing the API

**Tools**
Use **Postman** or **Swagger UI** to test endpoints. 🚀

**Setup**
Import the environment variables and start the FastAPI server using the command:

```bash
uvicorn main:app --reload
```

Visit Swagger UI at http://localhost:8000/docs for API exploration. 🧐
