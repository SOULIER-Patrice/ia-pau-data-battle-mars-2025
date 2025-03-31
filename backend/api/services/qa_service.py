from api.repositories import qa_repository
from api.models.QA import QA, QAForCreate

from ai.src.models.question import generate_mcq, generate_open
from ai.src.models.answer import generate_mcq_answer, generate_open_answer

import random


def generate_qa(category: str, qa_type: str, knowledge_vector_db, ollama_client, attempt=10) -> QA:

    if qa_type not in ["MCQ", "OPEN"]:
        raise ValueError(f"Unsupported qa_type: {qa_type}")  # Erreur immédiate

    for attempt_count in range(attempt):
        questions = qa_repository.get_qas_by_category(category, qa_type)
        print(len(questions), "questions found")

        if len(questions) >= 1:
            if len(questions) >= 3:
                questions = random.sample(questions, 3)
            # Formatter les questions
            formatted_questions = '\n'.join([q.question for q in questions])
            # renvoie un dict de la forme question: str options: List[str]
            try:
                if qa_type == "MCQ":
                    print("Generating MCQ")
                    question_disc = generate_mcq(
                        formatted_questions, knowledge_vector_db, ollama_client)
                    answer_disc = generate_mcq_answer(
                        question_disc, knowledge_vector_db, ollama_client)

                    if answer_disc:
                        qa_id = qa_repository.create_qa_mcq(
                            [category], question_disc["question"], answer_disc["Answer"], question_disc["options"], answer_disc["Justification"])
                        qa = qa_repository.get_qa(qa_id)
                        if not qa:
                            return None
                        return qa
                elif qa_type == "OPEN":
                    # renvoie un str correspondant a question
                    question = generate_open(
                        formatted_questions, knowledge_vector_db, ollama_client)
                    answer = generate_open_answer(
                        question, knowledge_vector_db, ollama_client)

                    if answer:
                        qa_id = qa_repository.create_qa_open(
                            [category], question, answer)
                        qa = qa_repository.get_qa(qa_id)
                        if not qa:
                            return None
                        return qa
                else:
                    raise (f"{qa_type} failed. Retrying...")

            except Exception as e:  # Soyez spécifique si possible
                print(
                    f"Attempt {attempt_count+1}/{attempt} failed. Error: {e}. Retrying...")
                # Loggez l'erreur si nécessaire
                continue  # Continue à la prochaine tentative

    # Si la boucle se termine sans succès
    raise ValueError(
        f"Failed to generate a {qa_type} question/answer for category '{category}' after {attempt} attempts.")


def generate_qas(creation_data: QAForCreate, knowledge_vector_db, ollama_client) -> list[QA]:
    """
    Génère un nombre spécifié de paires Question/Réponse.
    """
    generated_qas = []
    # Utilise _ si l'index i n'est pas utilisé
    for count in range(creation_data.number):
        try:
            category = random.sample(creation_data.categories, 1)[0]
            # Appel de la fonction qui génère UN SEUL QA
            new_qa = generate_qa(
                category,
                creation_data.type,
                knowledge_vector_db,
                ollama_client
            )
            if new_qa:  # Assurez-vous que generate_qa retourne bien quelque chose
                generated_qas.append(new_qa)
        except Exception as e:
            # Gérer l'erreur : logguer, ajouter un marqueur d'erreur, etc.
            raise ValueError(
                f"Erreur lors de la génération de la QA {count + 1}/{creation_data.number} pour la catégorie '{category}': {e}")

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
