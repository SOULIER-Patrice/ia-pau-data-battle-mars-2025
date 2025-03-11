from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends

from pydantic import BaseModel

from api.dependancies import auth_required, allowed_roles, oauth2_scheme
from api.exceptions import AlreadyExistsException
from api.models.User import UserForUpdate, UserOutput
from api.services import auth_service, user_service


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(auth_required)],
    tags=["User"],
)


@router.get("", dependencies=[Depends(allowed_roles(allowed_roles=["admin"]))])
def get_users() -> list[UserOutput]:
    return user_service.get_users()


@router.get("/{user_id}")
def get_user(user_id: UUID, token: str = Depends(oauth2_scheme)) -> UserOutput:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    user = user_service.find_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


class PasswordReset(BaseModel):
    old_password: str
    new_password: str


@router.post("/reset-password")
async def reset_password(
    passwords: PasswordReset,
    token: str = Depends(oauth2_scheme)
):
    current_user: UserOutput = auth_service.get_current_user(token)

    try:
        password_modified = auth_service.reset_password(
            current_user.id, passwords.old_password, passwords.new_password)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return password_modified


@router.get("/grant-admin/{user_id}")
async def grant_admin(user_id: UUID, token: str = Depends(oauth2_scheme)):
    current_user = auth_service.get_current_user(token)

    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    user = user_service.grant_admin(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.put("/{user_id}")
def update_user(user_id: UUID, user: UserForUpdate, token: str = Depends(oauth2_scheme)):
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    updated_user = user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
def delete_user(user_id: UUID, token: str = Depends(oauth2_scheme)):
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    deleted_count = user_service.delete_user(user_id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "User deleted successfully"}
