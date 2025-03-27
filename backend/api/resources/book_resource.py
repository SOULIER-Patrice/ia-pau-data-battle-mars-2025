from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends

from pydantic import BaseModel

from api.dependancies import auth_required, allowed_roles, oauth2_scheme
from api.exceptions import AlreadyExistsException
from api.models.Book import Book, BookForCreate
from api.models.Page import PageOuput
from api.services import auth_service, book_service


router = APIRouter(
    prefix="/books",
    dependencies=[Depends(auth_required)],
    tags=["Book"],
)


@router.post("/create")
async def create_book(book: BookForCreate, token: str = Depends(oauth2_scheme)) -> PageOuput:
    current_user = auth_service.get_current_user(token)

    if current_user.id != book.user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    page = book_service.create_book(book)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return page


@router.get("/{user_id}")
async def get_books(user_id: UUID, token: str = Depends(oauth2_scheme)) -> list[Book]:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    books = book_service.get_books(user_id)
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="books not found")
    return books


@router.get("/{book_id}/{user_id}")
async def get_book(book_id: UUID, user_id: UUID,  token: str = Depends(oauth2_scheme)) -> Book:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    book = book_service.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="book not found")
    return book


@router.get("/pages/{book_id}/{user_id}")
async def get_pages(book_id: UUID, user_id: UUID, token: str = Depends(oauth2_scheme)) -> list[PageOuput]:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    pages = book_service.get_pages(book_id)
    if not pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pages not found")
    return pages


@router.get("/page/{page_id}/{user_id}")
async def get_page(page_id: UUID, user_id: UUID, token: str = Depends(oauth2_scheme)) -> PageOuput:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    page = book_service.get_page(page_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pages not found")
    return page


@router.put("/page/{book_id}/{user_id}")
async def add_page(book_id: UUID, user_id: UUID, token: str = Depends(oauth2_scheme)) -> PageOuput:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    page = book_service.add_page(book_id)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pages not found")
    return page


class MessageModel(BaseModel):
    page_id: UUID
    message: str
    user_id: UUID


@router.post("/send_meessage")
async def send_message(message: MessageModel, token: str = Depends(oauth2_scheme)) -> str:
    current_user = auth_service.get_current_user(token)

    if current_user.id != message.user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    message, _ = book_service.send_message(message.page_id, message)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return message
