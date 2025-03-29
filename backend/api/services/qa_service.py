from api.repositories import qa_repository

from api.models.Page import QA


def get_all_qas() -> list[QA]:
    """
    Récupère toutes les QAs de la base de données.
    """
    qas = qa_repository.get_qas()
    if not qas:
        return []
    return qas


def get_qa(qa_id: str) -> QA:
    """
    Récupère une QA spécifique de la base de données.
    """
    qa = qa_repository.get_qa(qa_id)
    if not qa:
        return None
    return qa


def update_qa(qa: QA) -> QA:
    """
    Met à jour une QA dans la base de données.
    """
    isModified = qa_repository.update_qa(qa)
    if isModified == False:
        return None

    updated_qa = qa_repository.get_qa(qa.id)
    return updated_qa


def delete_qa(qa_id: str) -> bool:
    """
    Supprime une QA de la base de données.
    """
    return qa_repository.delete_qa(qa_id)
