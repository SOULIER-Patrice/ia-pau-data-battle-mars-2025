from ai.src.get_context import get_context
from ai.src.clean_output import clean_generate_mcq_output
from langchain_community.vectorstores import FAISS
from ollama import chat
import config.ai as ai


def generate_mcq(questions: str, knowledge_vector_db: FAISS, ollama_client) -> dict:
    """
    Generates an MCQ question.

    Parameters:
    questions (str): String of validated mcq questions from one subcategory as exemple.

    Returns:
    question (dict): {'question': '...',
                      'options': ['A ....', 'B ...', ...]}
    """
    # Retrieve context
    retrieved_docs = get_context(questions, 3, knowledge_vector_db)
    context = "\nExtracted documents:\n"
    context += "".join([f'Content: {doc.page_content} \nSource: {doc.metadata['ref']}\n\n' for i,
                       doc in enumerate(retrieved_docs)])

    # Build prompt
    system_prompt = f"""
    You are an AI specialized in generating multiple-choice legal questions based on given legal texts.
    ### Instructions:
    - Generate a new legal multiple-choice question based on the provided context.
    - Ensure the question aligns with the style and complexity of the given examples.
    - Provide four answer options (A, B, C, D), with only one being correct.
    - Format the output strictly as a JSON object with the following structure:
        ```json
        {{'question': '...', 'options': ['A ....', 'B ...', 'C ...', 'D ...']}}
    """

    user_prompt = f"""
    ### Context:
    {context}

    ### Examples of Previous Questions:
    {questions}

    Generate a new question that follows the same format and is correct based on the context. Write it in a json.
    """

    # Initial attempt to get the answer
    attempt_count = 0
    max_attempts = 5  # Limit number of attempts to prevent infinite loops

    while attempt_count < max_attempts:
        question_mcq = ollama_client.chat(model=ai.model,
                                          messages=[{"role": "system", "content": system_prompt},
                                                    {"role": "user", "content": user_prompt}],
                                          options={
                                              "num_predict": ai.max_output_tokens}
                                          )

        # Put question in correct json format
        try:
            cleaned_question_mcq = clean_generate_mcq_output(
                question_mcq['message']['content'], type='question', ollama_client=ollama_client)
            return cleaned_question_mcq  # If valid, return it
        except ValueError:
            attempt_count += 1  # Increment attempt count
            print(f"Attempt {attempt_count} failed. Retrying...")

    # If all attempts fail, raise an exception or return None
    raise ValueError("Failed to generate a valid MCQ after multiple attempts.")


def generate_open(questions: str, knowledge_vector_db: FAISS, ollama_client) -> str:
    """
    Generates an Open question.

    Parameters:
    questions (str): String of validated questions from one subcategory as exemple.

    Returns:
    question (str): The new question.
    """
    # Retrieve context
    retrieved_docs = get_context(questions, 5, knowledge_vector_db)
    context = "\nExtracted documents:\n"
    context += "".join([f'Content: {doc.page_content} \nSource: {doc.metadata['ref']}\n\n' for i,
                       doc in enumerate(retrieved_docs)])

    # Build prompt
    system_prompt = f"""You are an AI designed to generate legal questions based on the provided legal context. Your task is to generate a **detailed legal scenario** followed by **three to five structured questions**, ensuring that all questions can be answered using the given legal texts.

    ### **Instructions:**
    1. **Replicate the Structure**:
    - Review the example questions provided and follow the same format.
    - Start with a **detailed contextualization** of the scenario (at least 3-5 sentences).
    - Follow the scenario with **three to five sub-questions** labeled (a), (b), (c), etc.

    2. **Ensure Answerability**:
    - The generated questions must be fully answerable using the provided legal texts.
    - Ensure that each question directly relates to legal principles or procedures found in the given legal extracts.

    3. **Maintain Complexity & Relevance**:
    - Use real-world legal situations and terminology.
    - Keep the complexity and depth similar to the example questions.

    ### **Example Question Format:**
    *"On 12 August 2022, a divisional European patent application EP-F3 is filed in Italian per fax by three joint applicants: A, B, and C. On 12 September 2022, a translation of EP-F3 in the language of the proceedings of its parent application is filed. EP-F3's parent application is EP-F2, which is a divisional application of EP-F1. EP-F3 comprises 1 page abstract, 40 pages description, and 2 pages with 13 claims. A is an Italian university. B is an Italian enterprise which employs 500 persons, and which has an annual turnover of EUR 40 million and an annual balance sheet total of EUR 40 million. C is an Italian national resident in the USA. On 4 October 2022, a noting of loss of rights is sent because no fees have been paid. A transfer of rights is planned for 19 December 2022: Applicant B will transfer its rights in respect of EP-F3 to applicant C.*

    **a.** What procedural steps must be taken for the transfer of rights to be recorded?  
    **b.** Under what circumstances is the filing in Italian valid? What steps need to be taken and what fees need to be paid to ensure that EP-F3 remains pending?  
    **c.** What needs to be done if the applicants want to pay the examination fee at the reduced rate provided for in Article 14(1) of the Rules relating to Fees?"  
    """

    user_prompt = f"""### **Example Questions:**
    {questions}

    ### **Legal Text Extracts:**
    {context}

    ### **Generate a New Question:**
    - Create a **detailed scenario** (3-5 sentences) based on the provided legal context.
    - Follow the scenario with **three to five structured sub-questions** (labeled a, b, c, etc.).
    - Ensure that each sub-question is **answerable using the provided legal texts** and **maintains the complexity of the example questions**.
    - The output should **only contain the generated question**, without additional explanations.
    """

    # Redact an answer
    question_open = ollama_client.chat(model=ai.model,
                                       messages=[{"role": "system", "content": system_prompt},
                                                 {"role": "user", "content": user_prompt}],
                                       options={
                                           "num_predict": ai.max_output_tokens}
                                       )

    return question_open['message']['content']
