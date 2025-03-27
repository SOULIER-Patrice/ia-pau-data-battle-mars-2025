from uuid import UUID
from typing import List
from langchain_community.vectorstores import FAISS

from api.models.Book import Book, BookForCreate
from api.models.Page import PageOuput, PageForCreate
from api.repositories import book_repository, page_repository


from ai.src.models.question import generate_mcq, generate_open
from ai.src.models.answer import generate_mcq_answer, generate_open_answer, generate_feedback, chat_with_ai
import random


def create_book(book: BookForCreate, knowledge_vector_db: FAISS) -> PageOuput:
    book: Book = Book(
        title= book.title,
        categories= book.categories,
        type = book.type,
        user_id= book.user_id,
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
        qa = page_repository.get_qa(page.qa_id)
        if qa:
            page_output_data = {
                "id": page.id,
                "title": page.title,
                "book_id": page.book_id,
                "history": page.history,
                "created_at": page.created_at,
                "qa_id": page.qa_id,
                "category": qa["category"],
                "question": qa["question"],
                "options": qa.get("options"),  # Utiliser .get() pour gérer les cas où 'options' est absent
                "answer": qa["answer"],
                "justification": qa.get("justification"),  # Utiliser .get() pour gérer les cas où 'justification' est absent
                "isVerified": qa["is_verified"],
            }
            return PageOuput(**page_output_data)
        else :
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
            qa = page_repository.get_qa(page.qa_id)
            if qa:
                page_output_data = {
                    "id": page.id,
                    "title": page.title,
                    "book_id": page.book_id,
                    "history": page.history,
                    "created_at": page.created_at,
                    "qa_id": page.qa_id,
                    "category": qa["category"],
                    "question": qa["question"],
                    "options": qa.get("options"),
                    "answer": qa["answer"],
                    "justification": qa.get("justification"),
                    "isVerified": qa["is_verified"],
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
    questions = page_repository.get_qa_by_category(category)
    # Prendre 3 questions de questions et les mettre dans questions
    if len(questions) >= 3:
        questions = random.sample(questions, 3)
    else:
        questions = random.sample(questions, len(questions)) # prend tout les elements si moins de 3.
    
    # Formatter les questions
    formatted_questions = '\n'.join([q.question for q in questions])

    if book.type == "MCQ":
        question_disc = generate_mcq(formatted_questions, knowledge_vector_db) # renvoie un dict de la forme question: str options: List[str]
        answer_disc = generate_mcq_answer(question_disc, knowledge_vector_db) # renvoie {'Answer': 'Answer B.', 'Justification': 'Explanation According to the Guidelines for'}

        qa_id = page_repository.create_qa_mcq(category, question_disc, answer_disc)

        page_title = f"{category} - {question_disc["question"][:100]}"
    else:
        question = generate_open(formatted_questions, knowledge_vector_db) # renvoie un str correspondant a question
        answer = generate_open_answer(question, knowledge_vector_db) # renvoie un str correspondant a answer
        qa_id = page_repository.create_qa_open(category, question, answer)

        page_title = f"{category} - {question[:100]}"
    
    # Créer l'objet PageForCreate
    page_for_create = PageForCreate(
        title=page_title,
        book_id=book_id,
        qa_id=qa_id,
    ) 

    page_id = page_repository.create_page(page_for_create)

    page = get_page(page_id)
    return page


def send_message(page_id: UUID, message: str, knowledge_vector_db: FAISS):
    try:
        page = get_page(page_id)
        if not page:
            return "Page non trouvée.", []

        history = page.history #Access history attribute.

        if not history:
            user_answer = message
            if page.category == "MCQ": #access category attribute.
                question = f"{page.question} {page.options}"#access question and options attribute.
                correct_answer = f"{page.answer} {page.justification}"#access answer and justification attribute.
            else:
                question = page.question #access question attribute.
                correct_answer = page.answer #access answer attribute.

            result = generate_feedback(question, correct_answer, user_answer, knowledge_vector_db)
        else:
            result = chat_with_ai(f"{history}", message, knowledge_vector_db)

        history.append({"user": message})
        history.append({"ai": result})

        page_repository.update_page_history(page_id, history)

        return result, history

    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")
        return "Une erreur est survenue.", []
