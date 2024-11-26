from bson import ObjectId
from fastapi import status
from app.config.db import motor_db
from app.models.user import VerifyEmail
from app.utils.error_handler import server_error
from app.schemas.user_serializer import user_serializer


class ProfileService:
    def __init__(self) -> None:
        self.collection_name = motor_db['user']
        
    async def verify(self, id:str, code:VerifyEmail):
        user = await self.collection_name.find_one({"_id":ObjectId(id), "code":code})

        if user is None:
            server_error(status.HTTP_404_NOT_FOUND, f"User not found")

        try:
            verified = await self.collection_name.find_one_and_update(
                {"_id":ObjectId(id), "code":code},
                {"$set":{"verified":True, "code":'none'}}
                )
            return{
                   "message":"Email is successfully verified",
                   "profile":user_serializer(verified)
                   }
        except Exception as e:
           server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=str(e))
           
    async def get_profile(self, id:str):
        profile = await self.collection_name.find_one({"_id":ObjectId(id), "verified":True})
        if profile is None:
            server_error(status.HTTP_404_NOT_FOUND, f"Please verify your email before you proceed")
        try:
            return user_serializer(profile)
        except Exception as e:
            server_error(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, e=str(e))