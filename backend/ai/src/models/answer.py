from typing import AsyncGenerator
from ai.src.get_context import get_context
from ai.src.clean_output import clean_generate_mcq_output
from langchain_community.vectorstores import FAISS
from ollama import chat
from config.config import model, max_output_tokens


# question, options
def generate_mcq_answer(question_mcq: str, knowledge_vector_db: FAISS) -> dict:
    """
    Generates an answer for a MCQ question.

    Parameters:
    question_mcq (str): The input question_mcq for which an answer is needed.

    Returns:
    answer (str): The generated response from the AI with the context used.
    """
    # Convert the question in string, in case the question is a json.
    question_mcq = str(question_mcq)

    # Retrieve context
    retrieved_docs = get_context(question_mcq, 5, knowledge_vector_db)
    context = "\nExtracted documents:\n"
    context += "".join([f'Content: {doc.page_content} \nSource: {doc.metadata['ref']}\n\n' for i,
                       doc in enumerate(retrieved_docs)])
    context_sources = "".join(
        [f'\nSource: {doc.metadata['ref']}, Url: {doc.metadata.get('url', 'N/A')}' for i, doc in enumerate(retrieved_docs)])

    # Build prompt
    system_prompt = f"""
    You are an AI specialized in answering legal multiple-choice questions based on provided legal texts.
    ### Instructions:
    - When given a multiple-choice legal question, provide the correct answer followed by an explanation.
    - Your answer should begin with the correct choice (e.g., "Answer A").
    - After that, explain why this choice is correct based on the provided legal context.
    - Then, explain why the other choices (B, C, D) are incorrect, using relevant legal reasoning from the context.
    - Use the legal context provided to back up your reasoning.
    - Make sure to clearly distinguish between the correct answer and the incorrect ones.
    """

    user_prompt = f"""
    ### Context:
    {context}

    ### Legal Question:
    {question_mcq}

    Answer the question by:
    1. Starting with the correct answer (e.g., "Answer A").
    2. Explaining why this choice is correct according to the provided legal text.
    3. Explaining why the other options (B, C, D) are incorrect based on the legal context.
    """

    # Initial attempt to get the answer
    attempt_count = 0
    max_attempts = 10  # Limit number of attempts to prevent infinite loops

    while attempt_count < max_attempts:
        answer_mcq = chat(model=model,
                          messages=[{"role": "system", "content": system_prompt},
                                    {"role": "user", "content": user_prompt}],
                          options={"num_predict": max_output_tokens}
                          )

        # Put answer in correct json format
        try:
            cleaned_answer_mcq = clean_generate_mcq_output(
                answer_mcq['message']['content'], type='answer')
            # Add context to Justification
            cleaned_answer_mcq['Justification'] += f'\n\nSources:\n{context_sources}'
            return cleaned_answer_mcq  # If valid, return it
        except ValueError:
            attempt_count += 1  # Increment attempt count
            print(f"Attempt {attempt_count} failed. Retrying...")

    # If all attempts fail, raise an exception or return None
    raise ValueError("Failed to generate a valid MCQ after multiple attempts.")


def generate_open_answer(question_open: str, knowledge_vector_db: FAISS) -> str:
    """
    Generates an answer to a given open question.

    Parameters:
    question (str): The input question for which an answer is needed.

    Returns:
    answer (str): The generated response from the AI with the context used.
    """

    # Retrieve context
    retrieved_docs = get_context(question_open, 5, knowledge_vector_db)
    context = "\nExtracted documents:\n"
    context += "".join([f'Content: {doc.page_content}\nSource: {doc.metadata['ref']}\n' for i,
                       doc in enumerate(retrieved_docs)])
    context_sources = "".join(
        [f'\nSource: {doc.metadata['ref']}, Url: {doc.metadata.get('url', 'N/A')}' for i, doc in enumerate(retrieved_docs)])

    # Build prompt
    system_prompt = f"""You are an AI specialized in answering open-ended legal questions based on provided legal texts. Your task is to generate a detailed, accurate, and well-reasoned answer to the given question using the provided legal texts. Every answer must be supported by specific legal sources from the context provided.
    ### Instructions:
    1. **Answer Generation**:
    - Provide a clear, well-explained answer to the user's legal question.
    - The answer must strictly be based on the provided legal texts. Do not include any additional information not supported by the given texts.
    - For each part of the answer, explain how the relevant legal sources from the context support your reasoning.
    
    2. **Source Citation**:
    - After each point in the answer, cite the specific legal text(s) that were used to form that part of the answer.
    - Cite articles, sections, or specific clauses of the law, clearly linking them to the answer.
    
    3. **Explanation of Relevance**:
    - For each source used, provide a brief explanation of why that particular legal text is relevant to the question and how it supports the answer.
    
    4. **Validity**:
    - Your answer is only valid if it is directly supported by the legal texts provided in the context.

    5. **Legal Terminology**:
    - Use correct legal terminology and ensure clarity when referencing legal sources.

    ### Example Answer Flow:
    **Question**: "What conditions must be met for a contract to be voidable due to duress under the Civil Code?"

    **Answer**:
    - A contract may be voidable if one party was under duress, but this duress must be severe enough to impair the will of the affected party. According to Article 123 of the Civil Code, duress must be such that the affected party was left with no free choice in entering the contract.
    - **Source**: Article 123 of the Civil Code states: "A contract may be voidable if it was entered into under duress, provided that the duress was so severe that it compromised the free will of the affected party."
    - **Explanation of Relevance**: This article defines duress and explicitly ties the concept to the condition that it must be severe enough to affect free will. The wording "so severe" emphasizes that the severity of duress is a key factor in determining the validity of the contract.

    **Question**: "Can a contract be voidable due to lack of consent?"

    **Answer**:
    - Yes, under the Civil Code, a contract may be voidable if one party lacked the capacity to give consent. This includes situations where the individual was unable to understand the nature of the contract. Article 123 of the Civil Code outlines that contracts entered into by individuals lacking the legal capacity to understand the terms are voidable.
    - **Source**: Article 123 of the Civil Code states: "A contract is voidable when one party lacks the legal capacity to understand the terms of the agreement."
    - **Explanation of Relevance**: This article provides the legal basis for the voidability of a contract when consent is impaired due to the lack of understanding, which directly addresses the question about lack of consent.

    ### Example Legal Texts:
    - **Legal Text 1**: "A contract may be voidable if it was entered into under duress, provided that the duress was so severe that it compromised the free will of the affected party."
    - **Legal Text 2**: "A contract is voidable when one party lacks the legal capacity to understand the terms of the agreement, as specified in Article 123 of the Civil Code."
    """

    user_prompt = f"""### Legal Texts:
    {context}

    ### Question:
    {question_open}

    ### Answer:
    Please provide a detailed, accurate answer to the question. 
    1. Cite the relevant legal text(s) used in your answer.
    2. For each citation, explain why that source is relevant to the answer and how it supports your reasoning.
    3. Ensure your answer is strictly based on the legal texts provided. If the question cannot be answered using the available legal texts, state that explicitly.
    4. Use correct legal terminology and ensure clarity when referencing the sources.
    """

    # Redact an answer
    answer = chat(model=model,
                  messages=[{"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}],
                  options={"num_predict": max_output_tokens}
                  )

    # Assemble answer and context_sources
    final_answer = f'{answer['message']['content']}\n\nSources:{context_sources}'

    return final_answer


def generate_feedback(question: str, correct_answer: str, user_answer: str, knowledge_vector_db: FAISS) -> str:
    """
    Generates an AI-generated feedback on the user_answer. 
    The question and correct_answer were generated before. When we gave an question to an user,
    we also take the correct_answer. So when the user answer, we can give all, question, correct_answer (the correct one), 
    and user_answer to give a feedback to the user.

    Parameters:
    question (str): The question generated by AI.
    correct_answer (str): The correct answer.
    user_answer (str): The user answer.

    Returns:
    feedback (str): The correct answer and the explaination why the user is wrong including the context.
    """

    # Convert the question in string, in case the question is a json.
    question = str(question)
    correct_answer = str(correct_answer)

    # Retrieve context
    question_context = get_context(question, 3, knowledge_vector_db)
    correct_answer_context = get_context(
        correct_answer, 3, knowledge_vector_db)
    user_answer_context = get_context(user_answer, 3, knowledge_vector_db)
    # Combine all retrieved contexts
    all_contexts = question_context + correct_answer_context + user_answer_context
    context = "\nExtracted documents:\n"
    context += "".join([f'Content: {doc.page_content} \nSource: {doc.metadata['ref']}\n\n' for i,
                       doc in enumerate(all_contexts)])
    context_sources = "".join(
        [f'\nSource: {doc.metadata['ref']}, Url: {doc.metadata.get('url', 'N/A')}' for i, doc in enumerate(all_contexts)])

    # Build prompt
    system_prompt = f"""You are an AI designed to provide feedback on legal answers, both for multiple-choice questions (MCQs) and open-ended responses. When a user answers a question, your task is to explain whether their answer is correct or incorrect, using the legal context and specific sources to support your feedback.
    ### Instructions:
    - If the user answers a multiple-choice question (MCQ):
        1. Start by acknowledging the user's chosen answer.
        2. If the user's answer is correct, explain why it is correct using the legal context and cite relevant legal sources.
        3. If the user's answer is incorrect, explain why it is wrong, referencing specific legal articles or sections from the context.
        4. Provide the correct answer and back it up with legal reasoning from the context.
        5. If the user selected a partially correct answer, explain the distinction and provide clarification on what was missed.

    - If the user answers an open-ended question:
        1. Acknowledge the user's answer and assess its correctness.
        2. If the answer is correct, explain why it is correct using relevant legal context and sources.
        3. If the answer is incorrect or incomplete, explain where it went wrong, citing the legal context and relevant articles or sections.
        4. Provide the correct explanation and elaborate on any nuances or details the user might have missed.
        5. If the user is partially correct, explain what is correct and where they need to elaborate or correct their understanding.

    ### Example Response for an MCQ:
    User Answer: "Answer B."

    If the answer is wrong:
    - Start with: "Your answer, 'Answer B', is incorrect."
    - Explain the error: "According to Article 123 of the Civil Code, the correct interpretation is..."
    - Provide the correct answer: "The correct answer is 'Answer A' because..."
    - Cite specific legal sources: "As stated in Article 45 of the Civil Code, the situation described aligns with..."

    If the answer is partially correct:
    - Start with: "Your answer, 'Answer B', is partially correct."
    - Explain the partial correctness: "You correctly identified that the issue involves Article 123, but the application to the scenario is incomplete."
    - Clarify the distinction: "The key point is that Article 123 applies in a different context. Therefore, the correct answer is 'Answer A.'"

    ### Example Response for Open-Ended Questions:
    User Answer: "The law allows the contract to be voided if it was signed under duress."

    If the answer is wrong:
    - Start with: "Your answer is incorrect."
    - Explain the error: "While duress may lead to a contract being voidable, it is important to note that the law specifically requires that the duress must have been severe enough to affect the will of the person involved, as outlined in Article 123 of the Civil Code."
    - Provide the correct explanation: "The contract can only be voided if it meets the specific conditions outlined in Article 123, which states that..."

    If the answer is partially correct:
    - Start with: "Your answer is partially correct."
    - Explain the correct parts: "You are right that duress can impact the validity of a contract."
    - Clarify the missed details: "However, the law also specifies that the duress must have been significant enough to prevent free consent. Therefore, the correct interpretation includes this additional detail."
    """

    user_prompt = f"""### Context:
    {context}
    
    ### Correct Answer:
    {correct_answer}

    ### User's Answer:
    {user_answer}

    ### Legal Question:
    {question}

    ### Instructions:
    - Provide feedback on the user's answer (both for multiple-choice and open-ended responses).
    - If it's an MCQ, explain why the answer is correct or incorrect, using legal context and citing relevant articles.
    - If it's an open-ended response, assess whether the answer is correct or not, and explain using the legal context and articles.
    - Provide the correct answer or explanation and back it up with legal sources from the context.
    """

    # Redact an answer
    feedback = chat(model=model,
                    messages=[{"role": "system", "content": system_prompt},
                              {"role": "user", "content": user_prompt}],
                    options={"num_predict": max_output_tokens}
                    )

    # Assemble final answer
    final_answer = f'{feedback['message']['content']}\n\nContext:{context_sources}'

    return final_answer


async def generate_feedback_stream(question: str, correct_answer: str, user_answer: str, knowledge_vector_db: FAISS) -> AsyncGenerator[str, None]:
    # Retrieve context
    question_context = get_context(question, 3, knowledge_vector_db)
    correct_answer_context = get_context(
        correct_answer, 3, knowledge_vector_db)
    user_answer_context = get_context(user_answer, 3, knowledge_vector_db)
    all_contexts = question_context + correct_answer_context + user_answer_context
    context = "\nExtracted documents:\n"
    context += "".join(
        [f'Content: {doc.page_content} \nSource: {doc.metadata["ref"]}\n\n' for doc in all_contexts])

    # Build prompt
    system_prompt = f"""You are an AI designed to provide feedback on legal answers..."""  # Same as before
    user_prompt = f"""### Context:\n{context}\n\n### Correct Answer:\n{correct_answer}\n\n### User's Answer:\n{user_answer}\n\n### Legal Question:\n{question}\n\n### Instructions:\n..."""  # Same as before

    # Stream response
    async for chunk in chat_stream(model=model, system_prompt=system_prompt, user_prompt=user_prompt, max_output_tokens=max_output_tokens):
        yield chunk


def chat_with_ai(history: str, user_message: str, knowledge_vector_db: FAISS) -> str:
    """
    Based on the history of the conversation, initialy filled with question, user_answer, feedback.

    Parameters:
    history (str): Initialy the quesiton, user_answer, feedback. The history is filled with new messages.
    user_message (str): New message from user.

    Returns:
    answer (str): The answer for the user_message, base on the context from history.
    context_sources (str): The context used to answer with real link.
    """

    # Retrieve context
    history_context = get_context(history, 5, knowledge_vector_db)
    user_message_context = get_context(user_message, 3, knowledge_vector_db)
    # Combine all retrieved contexts
    all_contexts = history_context + user_message_context
    context = "\nExtracted documents:\n"
    context += "".join([f'Content: {doc.page_content} \nSource: {doc.metadata['ref']}\n\n' for i,
                       doc in enumerate(all_contexts)])
    context_sources = "".join(
        [f'\nSource: {doc.metadata['ref']}, Url: {doc.metadata.get('url', 'N/A')}' for i, doc in enumerate(all_contexts)])

    # Build prompt
    system_prompt = f"""You are an AI specialized in helping users understand legal concepts and answer legal questions. The conversation history and legal texts provided are your sources for generating responses. Your role is to engage in an ongoing conversation with the user, answering their questions, explaining legal concepts, and clarifying misunderstandings based on the legal context provided.

    ### Instructions:
    1. **Conversation History**: Refer to the conversation history as context for understanding the user's current question or doubt. Always base your responses on the conversation history and legal texts provided.
    2. **Legal Context**: Use the legal context (texts, articles, or sections) provided to answer questions or clarify points. If needed, quote specific legal articles or reference them when explaining a concept.
    3. **Discussion Flow**: Engage with the user in a conversational style. If they ask why their answer isn't correct, provide a detailed explanation using the legal context and reasoning.
    4. **Interactive Exploration**: Encourage the user to ask follow-up questions or seek further clarification about specific parts of the legal text. Offer suggestions to explore the legal texts together and make sure to reference specific articles when necessary.
    5. **Supportive Dialogue**: If the user's understanding of a legal concept or their answer is incorrect, explain where they went wrong and guide them towards the correct interpretation of the law. Use the legal context to back up your explanation.

    ### Example Flow:
    User: "I think the contract is voidable due to duress. Isn't that right?"
    AI: "Let's take a look at the legal context. According to Article 123 of the Civil Code, a contract may be voidable if one party was under severe duress. However, for duress to be a valid reason to void the contract, it must meet specific criteria. Let me walk you through the exact conditions outlined in the law."

    User: "But the text just mentions duress, doesn't it?"
    AI: "Yes, the term 'duress' is mentioned, but it's crucial to understand that the law specifies the severity of duress required. For instance, Article 123 requires the duress to be 'so severe that it compromises the freedom of choice of the person involved.' This distinction is important. Let's dive deeper into what 'severe' means under the law."
    """

    user_prompt = f"""### Conversation History:
    {history}

    ### Legal Context:
    {context}

    ### User's Question:
    {user_message}

    ### Instructions:
    - Provide a conversational response based on the conversation history and the legal context.
    - If the user has a misunderstanding or an incorrect answer, explain why it is wrong using the relevant legal text and guide them to the correct understanding.
    - Encourage the user to ask more questions if they need further clarification on specific legal points or sections.
    - Reference legal articles and sections as needed to back up your explanation.
    - Keep the conversation open and interactive, so the user feels comfortable discussing and exploring the legal concepts.
    """

    # Redact an answer
    answer = chat(model=model,
                  messages=[{"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}],
                  options={"num_predict": max_output_tokens}
                  )

    # Assemble answer
    final_answer = f'{answer['message']['content']}\n\nContext:\n{context_sources}'

    return final_answer


async def chat_with_ai_stream(history: str, user_message: str, knowledge_vector_db: FAISS) -> AsyncGenerator[str, None]:
    # Retrieve context
    history_context = get_context(history, 5, knowledge_vector_db)
    user_message_context = get_context(user_message, 3, knowledge_vector_db)
    all_contexts = history_context + user_message_context
    context = "\nExtracted documents:\n"
    context += "".join(
        [f'Content: {doc.page_content} \nSource: {doc.metadata["ref"]}\n\n' for doc in all_contexts])

    # Build prompt
    system_prompt = f"""You are an AI specialized in helping users understand legal concepts..."""  # Same as before
    user_prompt = f"""### Conversation History:\n{history}\n\n### Legal Context:\n{context}\n\n### User's Question:\n{user_message}\n\n### Instructions:\n..."""  # Same as before

    # Stream response
    async for chunk in chat_stream(model=model, system_prompt=system_prompt, user_prompt=user_prompt, max_output_tokens=max_output_tokens):
        yield chunk


async def chat_stream(model, system_prompt: str, user_prompt: str, max_output_tokens: int) -> AsyncGenerator[str, None]:
    stream = chat(model=model,
                  messages=[{"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}],
                  options={"num_predict": max_output_tokens},
                  stream=True)

    for chunk in stream:
        yield chunk["message"]["content"]
