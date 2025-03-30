from api.dependancies import auth_required, oauth2_scheme
from api.services import auth_service, qa_service
from api.models.QA import QA, QAForCreate

from api.resources.state import app_state

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
import json
import os

router = APIRouter(
    prefix="/qa",
    dependencies=[Depends(auth_required)],
    tags=["QA"],
)


@router.put("/create")
async def create_qa(create_qa: QAForCreate, token: str = Depends(oauth2_scheme)) -> list[QA]:
    current_user = auth_service.get_current_user(token)

    knowledge_vector_db = app_state.get("knowledge_vector_db")

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    # if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    qas = qa_service.generate_qas(create_qa, knowledge_vector_db)
    if not qas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )
    return qas


@router.get("")
async def get_qa(token: str = Depends(oauth2_scheme)) -> list[QA]:
    current_user = auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    # if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    qas = qa_service.get_all_qas()

    return qas


@router.get("/export", response_class=FileResponse)
async def export_qas(token: str = Depends(oauth2_scheme)) -> FileResponse:
    current_user = auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    # Récupérer toutes les questions
    qas = qa_service.get_all_qas()

    # Supprimer les UUID des questions
    for qa in qas:
        del qa.id

    # Convertir les questions en JSON
    json_data = json.dumps([qa.model_dump() for qa in qas], indent=4)

    # Sauvegarder le JSON dans un fichier temporaire
    file_path = "data/qas_export.json"
    with open(file_path, "w") as file:
        file.write(json_data)

    # Retourner le fichier en réponse
    return FileResponse(
        file_path,
        media_type="application/json",
        filename="qas_export.json",
    )


@router.get("/{qa_id}")
async def get_qa_by_id(qa_id: str, token: str = Depends(oauth2_scheme)) -> QA:
    current_user = auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    qa = qa_service.get_qa(qa_id)
    if not qa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QA not found"
        )
    return qa


@router.put("")
async def update_qa(qa: QA, token: str = Depends(oauth2_scheme)) -> QA:
    current_user = auth_service.get_current_user(token)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )

    updated_qa = qa_service.update_qa(qa)
    if not updated_qa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QA not found"
        )
    return updated_qa
