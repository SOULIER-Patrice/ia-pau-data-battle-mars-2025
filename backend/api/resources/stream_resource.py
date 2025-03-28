import asyncio
import sys
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import StreamingResponse

from api.resources.state import app_state
from api.services import auth_service, book_service

router = APIRouter(
    prefix="/stream",
    tags=["Stream"],
)


async def event_stream(page_id: UUID, message: str, knowledge_vector_db) -> StreamingResponse:
    async for chunk in book_service.send_message_stream(page_id, message, knowledge_vector_db):
        await asyncio.sleep(0.1)
        yield f"data: {chunk}\n\n"


@router.get("/send_message_stream", response_class=StreamingResponse, dependencies=[])
async def send_message_stream(
    page_id: UUID = Query(...,
                          description="ID de la page pour laquelle le message est envoyé"),
    message: str = Query(..., description="Message envoyé par l'utilisateur"),
    user_id: UUID = Query(...,
                          description="ID de l'utilisateur envoyant le message"),
    token: str = Query(..., description="Jeton d'authentification"),
) -> StreamingResponse:
    """
    Envoie un message à l'IA et retourne une réponse en streaming via SSE (Server-Sent Events).

    - **page_id**: ID de la page cible.
    - **message**: Message envoyé par l'utilisateur.
    - **user_id**: ID de l'utilisateur envoyant le message.
    - **token**: Jeton d'authentification pour valider l'utilisateur.
    """
    current_user = auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    knowledge_vector_db = app_state.get("knowledge_vector_db")

    # Vérification des permissions
    if current_user.id != user_id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    return StreamingResponse(event_stream(page_id, message, knowledge_vector_db),
                             media_type="text/event-stream")
