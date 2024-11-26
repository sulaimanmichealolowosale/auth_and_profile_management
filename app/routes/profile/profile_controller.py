from fastapi import APIRouter, Depends

from app.routes.profile.profile_service import ProfileService
from app.utils.oauth2 import get_current_user


router = APIRouter(
    prefix="/api/profile",
    tags=['Profile']
)


profile_service = ProfileService()


@router.post('/verify/{code}')
async def verify_email(code:str, current_user = Depends(get_current_user)):
    user =await profile_service.verify(id = current_user['_id'], code=code)
    return user


@router.post('/profile')
async def get_profile(current_user = Depends(get_current_user)):
    profile =await profile_service.get_profile(id = current_user['_id'])
    return profile