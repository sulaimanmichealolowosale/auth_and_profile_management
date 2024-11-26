<h1>Auth and Profile Management Service API Overview</h1>
<p>This is a backend service for authentication and profile management built using FastAPI. The application handles:</p>

<ul>
<li>User registration with email verification.</li>
<li>Secure login with token generation.</li>
<li>Password reset functionality.</li>
<li>User profile management, including email verification.</li>

</ul>

<p>The logic is separated into services (business logic) and controllers (API endpoints), ensuring clean code and scalability.</p>

<h2>Project Structure</h2>
<strong>Key files and their roles:</strong>

<ul>
    <li>auth_service.py: Contains authentication business logic.</li>
    <li>auth_controller.py: Handles API endpoints for authentication.</li>
    <li>profile_service.py: Manages profile-related logic.</li>
    <li>profile_controller.py: Handles API endpoints for user profiles.</li>
    <li>config/db.py: Database connection setup using MongoDB.</li>
    <li>
    utils/: Contains helper functions such as:
        <ul>
            <li>error_handler.py: Custom error responses.</li>
            <li>password_crypt.py: Password hashing and verification.</li>
            <li>email_conf.py: Email utility functions for sending emails.</li>
            <li>oauth2.py: JWT token creation and verification.</li>
        </ul>
    </li>

    <li>schemas/user_serializer.py: Serializes database user data into JSON format.
    Environment Variables</li>

</ul>

<h3>Ensure you have the following environment variables set up:</h3>

MONGO_URI=<Your MongoDB connection URI>
SECRET_KEY=<Your JWT secret key>
ALGORITHM=<Your JWT algorithm>
EMAIL_HOST=<Email host>
EMAIL_PORT=<Email port>
MAIL_SERVER=<Email server>
EMAIL_USER=<Email username>
EMAIL_PASSWORD=<Email password>

Authentication Endpoints

1. Register User
   Registers a new user and sends a verification email.

Endpoint: POST /api/auth/register
Request Body:

{
"username": "john_doe",
"email": "john.doe@example.com",
"password": "securepassword"
}
Response:

{
"id": "user_id",
"username": "john_doe",
"email": "john.doe@example.com",
"verified": false
}

2. Login User
   Logs in a user and generates access and refresh tokens.

Endpoint: POST /api/auth/login
Request Body (Form):

username: john.doe@example.com
password: securepassword
Response:

{
"user": {
"id": "user_id",
"username": "john_doe",
"email": "john.doe@example.com"
},
"access_token": "jwt_access_token",
"refresh_token": "jwt_refresh_token"
}

3. Request Password Reset Code
   Sends a password reset code to the user's email.

Endpoint: POST /api/auth/forgot-password/get-code
Request Body:

{
"email": "john.doe@example.com"
}
Response:

{
"message": "Password reset code was sent to the provided email"
}

4. Reset Password
   Resets the user's password using the code.

Endpoint: PUT /api/auth/forgot-password/
Request Body:

{
"email": "john.doe@example.com",
"code": "123456",
"password": "new_secure_password"
}
Response:

{
"message": "Password reset was successful",
"profile": {
"id": "user_id",
"username": "john_doe",
"email": "john.doe@example.com",
"verified": false
}
}
Profile Management Endpoints

1. Verify Email
   Verifies a user's email using a code.

Endpoint: POST /api/profile/verify/{code}
Headers:

Authorization: Bearer <access_token>
Response:

{
"message": "Email is successfully verified",
"profile": {
"id": "user_id",
"username": "john_doe",
"email": "john.doe@example.com",
"verified": true
}
} 2. Get Profile
Fetches the profile of the authenticated user.

Endpoint: POST /api/profile/profile
Headers:

Authorization: Bearer <access_token>
Response:

{
"id": "user_id",
"username": "john_doe",
"email": "john.doe@example.com",
"verified": true
}

Testing
Tools: Use Postman or Swagger UI to test endpoints.
Setup: Import the environment variables and start the FastAPI server using:
bash
Copy code
uvicorn main:app --reload
Use Swagger UI at http://localhost:8000/docs for API exploration.
