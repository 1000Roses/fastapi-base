from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.schemas.user import Token
from app.core.logging import log_service_call


router = APIRouter()


@router.post("/token", response_model=Token)
@log_service_call("AuthAPI")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    auth_response = await service.authenticate_user(form_data.username, form_data.password, request)
    if auth_response.status != status.HTTP_200_OK:
        return auth_response
    
    return await service.create_access_token(form_data.username, request) 