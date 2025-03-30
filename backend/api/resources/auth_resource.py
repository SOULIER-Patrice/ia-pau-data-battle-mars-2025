from datetime import timedelta
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer

# from config.config import config, fm_config
from api.exceptions import AlreadyExistsException
from api.models.Token import Token
from api.models.User import UserForCreate, UserOutput
from api.services import auth_service, user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


class UserData(BaseModel):
    token: Token
    user: UserOutput


@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return auth_service.get_current_user(token)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register_user(
    user: UserForCreate,
) -> UserData:
    try:
        user_output: UserOutput = user_service.create_user(user)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_output:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="L'utilisateur existe déjà",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user_output.email}, expires_delta=access_token_expires
    )
    return UserData(token=Token(access_token=access_token, token_type="bearer"), user=user_output)
