from api.repositories import qa_repository
from api.models.QA import QA, QAForCreate

from ai.src.models.question import generate_mcq, generate_open
from ai.src.models.answer import generate_mcq_answer, generate_open_answer

import random


def generate_qa(category: str, qa_type: str, knowledge_vector_db, attempt=10) -> QA:

    for _ in range(attempt):
        questions = qa_repository.get_qas_by_category(category, qa_type)
        if len(questions) >= 3:
            questions = random.sample(questions, 3)
            # Formatter les questions
            formatted_questions = '\n'.join([q.question for q in questions])

            if qa_type == "MCQ":
                # renvoie un dict de la forme question: str options: List[str]
                question_disc = generate_mcq(
                    formatted_questions, knowledge_vector_db)
                if question_disc:
                    # renvoie {'Answer': 'Answer B.', 'Justification': 'Explanation According to the Guidelines for'}
                    answer_disc = generate_mcq_answer(
                        question_disc, knowledge_vector_db)
                    if answer_disc:
                        qa_id = qa_repository.create_qa_mcq(
                            category, question_disc["question"], answer_disc["Answer"], question_disc["options"], answer_disc["Justification"])
                        qa = qa_repository.get_qa(qa_id)
                        if not qa:
                            return None
                        return qa
            else:
                # renvoie un str correspondant a question
                question = generate_open(
                    formatted_questions, knowledge_vector_db)
                if question:
                    answer = generate_open_answer(
                        question, knowledge_vector_db)
                    if answer:
                        qa_id = qa_repository.create_qa_open(
                            category, question, answer)
                        qa = qa_repository.get_qa(qa_id)
                        if not qa:
                            return None
                        return qa


def generate_qas(creation_data: QAForCreate, knowledge_vector_db) -> list[QA]:
    """
    Génère un nombre spécifié de paires Question/Réponse.
    """
    generated_qas = []
    for _ in range(creation_data.number):  # Utilise _ si l'index i n'est pas utilisé
        try:
            category = random.sample(creation_data.categories, 1)[0]
            # Appel de la fonction qui génère UN SEUL QA
            new_qa = generate_qa(
                category,
                creation_data.type,
                knowledge_vector_db
            )
            generated_qas.append(new_qa)
        except Exception as e:
            # Gérer les erreurs de génération d'un seul QA (log, skip, stop?)
            print(f"Erreur lors de la génération d'un QA : {e}")
            # Peut-être continuer ou arrêter la boucle selon le besoin
            # continue
            # ou raise HTTPException(status_code=500, detail=f"Failed to generate QA item: {e}")

    # Retourne la liste des QAs générés (peut être vide si number=0 ou si erreurs gérées par 'continue')
    return generated_qas


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
