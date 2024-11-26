from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.routes.auth.auth_service import AuthService
from app.models.auth import ForgotPassword, RegisterModel, ResetPassword


router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)

auth_service = AuthService()


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(model: RegisterModel):
    user =await auth_service.register(model)
    return user

@router.post('/login', status_code=status.HTTP_201_CREATED)
async def login(model: OAuth2PasswordRequestForm = Depends()):
    user =await auth_service.login(model)
    return user

@router.post('/forgot-password/get-code', status_code=status.HTTP_201_CREATED)
async def init_password_reset(model: ForgotPassword):
    user =await auth_service.init_password_reset(model)
    return user

@router.put('/forgot-password/', status_code=status.HTTP_201_CREATED)
async def reset_password(model: ResetPassword):
    user =await auth_service.reset_password(model)
    return user