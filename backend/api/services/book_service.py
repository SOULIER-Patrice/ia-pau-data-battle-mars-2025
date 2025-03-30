from uuid import UUID
from typing import AsyncGenerator, List
from langchain_community.vectorstores import FAISS

from api.models.QA import QA
from api.models.Book import Book, BookForCreate
from api.models.Page import PageOuput, PageForCreate
from api.repositories import book_repository, page_repository, qa_repository
from api.services import qa_service


from ai.src.models.question import generate_mcq, generate_open
from ai.src.models.answer import chat_with_ai_stream, generate_feedback_stream, generate_mcq_answer, generate_open_answer, generate_feedback, chat_with_ai
import random


def create_book(book: BookForCreate, knowledge_vector_db: FAISS) -> PageOuput:
    book: Book = Book(
        title=book.title,
        categories=book.categories,
        type=book.type,
        user_id=book.user_id,
    )
    book_id = book_repository.create_book(book)
    page = add_page(book_id, knowledge_vector_db)

    return page


def get_book(book_id: UUID) -> Book:
    book = book_repository.get_book(book_id)
    return book


def get_books(user_id: UUID) -> List[Book]:
    books = book_repository.get_books(user_id)
    return books


def get_page(page_id: UUID) -> PageOuput:

    page = page_repository.get_page(page_id)
    if page:
        qa = qa_repository.get_qa(page.qa_id)
        if qa:
            page_output_data = {
                "id": page.id,
                "title": page.title,
                "book_id": page.book_id,
                "history": page.history,
                "created_at": page.created_at,
                "qa_id": page.qa_id,
                "category": qa.category,
                "question": qa.question,
                "options": qa.options,
                "answer": qa.answer,
                "justification": qa.justification,
                "isVerified": qa.is_verified,
            }
            return PageOuput(**page_output_data)
        else:
            return None
    else:
        return None


def get_pages(book_id: UUID) -> List[PageOuput]:
    """
    Récupère toutes les pages associées à un livre donné et les renvoie sous forme d'objets PageOuput.

    Args:
        book_id: L'ID du livre.

    Returns:
        Une liste d'objets PageOuput contenant les données des pages et des QA associées, ou une liste vide si aucune page n'est trouvée.
    """
    pages = page_repository.get_pages(book_id)
    if pages:
        page_outputs = []
        for page in pages:
            qa = qa_repository.get_qa(page.qa_id)
            if qa:
                page_output_data = {
                    "id": page.id,
                    "title": page.title,
                    "book_id": page.book_id,
                    "history": page.history,
                    "created_at": page.created_at,
                    "qa_id": page.qa_id,
                    "category": qa.category,
                    "question": qa.question,
                    "options": qa.options,
                    "answer": qa.answer,
                    "justification": qa.justification,
                    "isVerified": qa.is_verified,
                }
                page_outputs.append(PageOuput(**page_output_data))
            else:
                # Si la QA n'est pas trouvée, vous pouvez choisir de ne pas inclure la page ou de la renvoyer avec des données QA vides
                # Pour cet exemple, nous n'incluons pas la page si la QA n'est pas trouvée.
                pass
        return page_outputs
    else:
        return []


def add_page(book_id: UUID, knowledge_vector_db: FAISS) -> PageOuput:

    book = get_book(book_id)
    category = random.sample(book.categories, 1)[0]
    qas_catagory = qa_repository.get_qas_by_category(category, book.type)
    qas_in_book = qa_repository.get_qas_by_book(book.id)
    print(qas_catagory, qas_in_book)
    available_qas = [qa for qa in qas_catagory if qa.id not in [
        q.id for q in qas_in_book]]
    if available_qas:
        qa = random.sample(available_qas, 1)[0]  # Take the first available QA
    else:
        qa = qa_service.generate_qa(
            category, book.type, knowledge_vector_db)

    page_title = f"{qa.category} - {qa.question[:100]}"
    # Créer l'objet PageForCreate
    page_for_create = PageForCreate(
        title=page_title,
        book_id=book_id,
        qa_id=qa.id,
    )

    page_id = page_repository.create_page(page_for_create)

    page = get_page(page_id)
    return page


def send_message(page_id: UUID, message: str, knowledge_vector_db: FAISS):
    try:
        page = get_page(page_id)
        if not page:
            return "Page non trouvée.", []

        history = page.history  # Access history attribute.

        if not history:
            user_answer = message
            if page.category == "MCQ":  # access category attribute.
                # access question and options attribute.
                question = f"{page.question} {page.options}"
                # access answer and justification attribute.
                correct_answer = f"{page.answer} {page.justification}"
            else:
                question = page.question  # access question attribute.
                correct_answer = page.answer  # access answer attribute.

                result = generate_feedback(
                    question, correct_answer, user_answer, knowledge_vector_db)
        else:
            result = chat_with_ai(f"{history}", message, knowledge_vector_db)

        history.append({"user": message})
        history.append({"ai": result})

        page_repository.update_page_history(page_id, history)

        return result, history

    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")
        return "Une erreur est survenue.", []


async def send_message_stream(page_id: UUID, message: str, knowledge_vector_db: FAISS) -> AsyncGenerator[str, None]:
    try:
        page = get_page(page_id)
        if not page:
            yield "Page non trouvée."
            return

        book = get_book(page.book_id)
        if not book:
            yield "Livre non trouvé."
            return

        history = page.history

        response_chunks = []  # Liste pour accumuler les chunks

        if not history:
            user_answer = message
            if book.type == "chat":
                question = page.question
                correct_answer = page.answer
                async for chunk in generate_feedback_stream(question, correct_answer, user_answer, knowledge_vector_db):
                    # Ajouter chaque chunk à la liste
                    response_chunks.append(chunk)
                    yield chunk
        else:
            async for chunk in chat_with_ai_stream(f"{history}", message, knowledge_vector_db):
                # Ajouter chaque chunk à la liste
                response_chunks.append(chunk)
                yield chunk

        # Combiner tous les chunks en une seule réponse
        full_response = ''.join(response_chunks)

        # Mettre à jour l'historique de la page avec le message et la réponse complète
        history.append({"user": message})
        history.append({"ai": full_response})

        page_repository.update_page_history(page_id, history)

    except Exception as e:
        yield f"Erreur lors de l'envoi du message : {e}"
