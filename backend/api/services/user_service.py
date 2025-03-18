from uuid import UUID

from api.exceptions import AlreadyExistsException
from api.models.User import User, UserForCreate, UserForUpdate, UserOutput
from api.repositories import user_repository
from api.services import auth_service


def create_user(user: UserForCreate) -> UserOutput:
    if find_user_by_email(user.email):
        raise AlreadyExistsException("User already exists")

    user: User = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=auth_service.get_password_hash(user.password)
    )
    user_repository.create_user(user.model_dump(by_alias=True))

    # Get the user with the id
    user_output: UserOutput = find_user_by_id(user.id)
    return user_output


def get_users() -> list[UserOutput]:
    users = user_repository.get_users()
    return [UserOutput(
        id=user['id'],
        email=user['email'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        roles=user['roles']
    ) for user in users]


def find_user_by_email(email: str) -> UserOutput:
    result = user_repository.find_user_by_email(email)
    if not result:
        return None
    user_output: UserOutput = UserOutput(
        id=result['id'],
        email=result['email'],
        first_name=result['first_name'],
        last_name=result['last_name'],
        roles=result['roles']
    )
    return user_output


def find_user_by_email_with_hashed_password(email: str) -> User:
    result = user_repository.find_user_by_email(email)
    if not result:
        return None

    user = User(
        email=result['email'],
        first_name=result['first_name'],
        last_name=result['last_name'],
        roles=result['roles'],
        hashed_password=result['hashed_password']
    )
    # Update the user id after the object creation because Python
    user.id = result['id']
    return user


def find_user_by_id(user_id: UUID) -> UserOutput:
    result = user_repository.find_user_by_id(user_id)
    if not result:
        return None

    user_output: UserOutput = UserOutput(
        id=result['id'],
        email=result['email'],
        first_name=result['first_name'],
        last_name=result['last_name'],
        roles=result['roles']
    )
    return user_output


def update_user(user_id: UUID, user: UserForUpdate) -> UserOutput:
    other_user = find_user_by_email(user.email)
    if other_user and other_user.id != user_id:
        raise AlreadyExistsException("User already exists")

    modify_count = user_repository.update_user(
        user_id, user.model_dump(by_alias=True))

    return find_user_by_id(user_id)


def grant_admin(user_id: UUID) -> UserOutput:
    user = find_user_by_id(user_id)
    if not user:
        return None

    user_repository.grant_role_to_user(user_id, 'admin')
    user.roles.append('admin')

    return user


def delete_user(user_id: UUID) -> int:
    return user_repository.delete_user(user_id)
