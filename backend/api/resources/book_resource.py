import asyncio
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from pydantic import BaseModel
from api.resources.state import app_state

from api.dependancies import auth_required, oauth2_scheme
from api.models.Book import Book, BookForCreate
from api.models.Page import PageOuput
from api.services import auth_service, book_service


router = APIRouter(
    prefix="/books",
    dependencies=[Depends(auth_required)],
    tags=["Book"],
)


@router.post("/create", response_model=PageOuput)
async def create_book(book: BookForCreate, token: str = Depends(oauth2_scheme)) -> PageOuput:
    current_user = auth_service.get_current_user(token)

    knowledge_vector_db = app_state.get("knowledge_vector_db")

    if current_user.id != book.user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        page = book_service.create_book(book, knowledge_vector_db)

    except ValueError as ve:  # Attraper l'erreur spécifique attendue
        # Log l'erreur originale pour le débogage côté serveur
        # Remplacez par votre système de logging
        print(f"QA generation failed: {ve}")

        # Lever une HTTPException appropriée pour le client
        raise HTTPException(
            # status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Ou 422, 503...
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Optionnel: inclure une partie du message d'erreur
            detail=f"Failed during question generation: {ve}"
            # Ou gardez un message plus générique pour le client:
            # detail="An error occurred during question generation. Please try again later or contact support."
        )
    except Exception as e:  # Attraper d'autres erreurs inattendues
        print(f"Unexpected error during QA generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected server error occurred during question generation."
        )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return page


@router.get("/{user_id}", response_model=list[Book])
async def get_books(user_id: UUID, token: str = Depends(oauth2_scheme)) -> list[Book]:
    current_user = auth_service.get_current_user(token)

    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    books = book_service.get_books(user_id)
    return books


@router.get("/{book_id}/{user_id}", response_model=Book)
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


@router.get("/pages/{book_id}/{user_id}", response_model=list[PageOuput])
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


@router.get("/page/{page_id}/{user_id}", response_model=PageOuput)
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


@router.put("/page/{book_id}/{user_id}", response_model=PageOuput)
async def add_page(book_id: UUID, user_id: UUID, token: str = Depends(oauth2_scheme)) -> PageOuput:
    current_user = auth_service.get_current_user(token)
    knowledge_vector_db = app_state.get("knowledge_vector_db")
    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        page = book_service.add_page(book_id, knowledge_vector_db)
    except ValueError as ve:  # Attraper l'erreur spécifique attendue
        # Log l'erreur originale pour le débogage côté serveur
        # Remplacez par votre système de logging
        print(f"QA generation failed: {ve}")

        # Lever une HTTPException appropriée pour le client
        raise HTTPException(
            # status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Ou 422, 503...
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # Optionnel: inclure une partie du message d'erreur
            detail=f"Failed during question generation: {ve}"
            # Ou gardez un message plus générique pour le client:
            # detail="An error occurred during question generation. Please try again later or contact support."
        )
    except Exception as e:  # Attraper d'autres erreurs inattendues
        print(f"Unexpected error during QA generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected server error occurred during question generation."
        )

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="pages not found")
    return page


class Message(BaseModel):
    page_id: UUID
    message: str
    user_id: UUID


@router.post("/send_meessage", response_model=str)
async def send_message(message: Message, token: str = Depends(oauth2_scheme)) -> str:

    current_user = auth_service.get_current_user(token)
    knowledge_vector_db = app_state.get("knowledge_vector_db")

    if current_user.id != message.user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    message, _ = book_service.send_message(
        message.page_id, message.message, knowledge_vector_db)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return message


async def event_stream(page_id: UUID, message: str, knowledge_vector_db) -> StreamingResponse:
    async for chunk in book_service.send_message_stream(page_id, message, knowledge_vector_db):
        await asyncio.sleep(0.001)
        yield f"data: {chunk}[END_CHUNK]\n\n"


@router.post("/send_message_stream", response_class=StreamingResponse)
async def send_message_stream(message: Message, token: str = Depends(oauth2_scheme)) -> StreamingResponse:

    current_user = auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    knowledge_vector_db = app_state.get("knowledge_vector_db")

    # Vérification des permissions
    if current_user.id != message.user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    return StreamingResponse(event_stream(message.page_id, message.message, knowledge_vector_db),
                             media_type="text/event-stream")
