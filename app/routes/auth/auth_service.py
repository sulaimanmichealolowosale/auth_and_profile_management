from datetime import timedelta
from bson import ObjectId
from fastapi import status
from app.config.db import motor_db
from app.models.auth import ForgotPassword, RegisterModel, ResetPassword
from app.utils.error_handler import server_error
from app.schemas.user_serializer import user_serializer
from app.utils.oauth2 import credentials_exception
from app.utils.password_crypt import get_password_hash, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.oauth2 import create_access_token
from app.utils.email_conf import forgot_password_email_html, send_email, generate_verification_code, verify_email_html


class AuthService:
    def __init__(self) -> None:
        self.collection_name = motor_db['user']
        

    async def register(self, model:RegisterModel):
        """
        Registers a new user after sending the verification email.
        """
        # Check if the user already exists
        existing_user = await self.collection_name.find_one({"email": model.email})
        if existing_user is not None:
            server_error(status.HTTP_409_CONFLICT, f"User with email: {model.email} already exists")
        
        try:
            # Generate the verification code first
            code = generate_verification_code()
            email_body = verify_email_html(
                login_email=model.email,
                password=model.password,
                username=model.username,
                code=code,
            )
            
            # Send the verification code to the user's email
            await send_email(
                subject="Welcome to Multivendor Restaurants!",
                recipients=[model.email],
                body=email_body,
            )
            

            # Hash the user's password
            hashed_password = get_password_hash(model.password)
            model.password = hashed_password

            # Insert the new user into the database
            
            register_model = model.model_dump()
            
            register_model['code'] = code
            register_model['forgot_password_code'] = "none"
            register_model['verified'] = False
            user = await self.collection_name.insert_one(register_model)
            inserted_user = await self.collection_name.find_one({"_id": ObjectId(user.inserted_id)})

            # Return the user data after successful registration
            return user_serializer(inserted_user)
        except Exception as e:
            # If anything fails, return a server error
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
        
    async def login(self, model: OAuth2PasswordRequestForm):
        """
        Logs in a user and generates access and refresh tokens.
        """
        # Check if the user exists and password matches
        existing_user = await self.collection_name.find_one({"email": model.username})
        if existing_user is None or not verify_password(model.password, existing_user['password']):
            raise credentials_exception()
        
        try:
            # Prepare user data
            data = {
                "id": str(existing_user['_id']),
                "username": existing_user['username'],
                "email": existing_user['email'],
            }

            # Create the access and refresh tokens
            access_token = create_access_token(data=data)
            refresh_token = create_access_token(data=data, expires_delta=timedelta(days=1))

            # Return the tokens and user data
            return {
                "user": user_serializer(existing_user),
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        except Exception as e:
            # If anything fails, return a server error
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
            
    async def init_password_reset(self, model: ForgotPassword):
        
        user = await self.collection_name.find_one({"email":model.email})
        if user is None:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e="Email not found")
        try:
            code = generate_verification_code()
            email_body = forgot_password_email_html(
                code=code,
            )
            
            await send_email(
                subject="Password reset code!",
                recipients=[model.email],
                body=email_body,
            )
            
            await self.collection_name.find_one_and_update(
                {"email":model.email},
                {"$set":{"forgot_password_code":code}}
                
                )
            
            return {
                "message":"Password reset code was sent to the provided email"
            }
        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))


    async def reset_password(self, model: ResetPassword):
        
        user = await self.collection_name.find_one({"email":model.email,"forgot_password_code":model.code})
        if user is None:
            server_error(status_code=status.HTTP_404_NOT_FOUND, e="Invalid password reset code")
        try:
            
            # Hash the user's password
            hashed_password = get_password_hash(model.password)
            model.password = hashed_password
            
            user = await self.collection_name.find_one_and_update(
                {"email":model.email},
                {"$set":{"password":model.password, "forgot_password_code":"none"}}
                )
            
            return {
                "message":"Password reset was sucessful",
                "profile":user_serializer(user)
            }
        except Exception as e:
            server_error(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e))
