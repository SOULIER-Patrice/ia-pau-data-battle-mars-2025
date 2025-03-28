import re
import json
from ollama import chat
from config.config import model, ollama_client


def validate_json_format_mcq(llm_output, type):
    """
    Attempts to extract and validate a JSON structure from the LLM output.

    Parameters:
    llm_output (str): Raw output from the LLM.
    type (str): question or answer

    Returns:
    dict: A valid JSON object if found and correctly formatted, otherwise None.
    """

    if type == 'question':
        try:
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                cleaned_json = json.loads(json_match.group())
                if "question" in cleaned_json and "options" in cleaned_json:
                    return cleaned_json
        except json.JSONDecodeError:
            pass
        return None
    
    elif type == 'answer':
        try:
            json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
            if json_match:
                cleaned_json = json.loads(json_match.group())
                if "Answer" in cleaned_json and "Justification" in cleaned_json:
                    answer = cleaned_json["Answer"]
                    # Check if answer in 'A', 'B', 'C', or 'D'.
                    if answer not in {'A', 'B', 'C', 'D'}:
                        # check for a valid letter isolated
                        match = re.search(r'\b[A-D]\b', answer)
                        if match:
                            cleaned_json["Answer"] = match.group()
                        else:
                            return None
                    return cleaned_json
        except json.JSONDecodeError:
            pass
        return None


def call_formatting_llm_mcq(llm_output, type):
    """
    Calls an LLM specialized in formatting text into the correct JSON format.

    Parameters:
    llm_output (str): Raw output from the initial LLM.
    type (str): question or answer

    Returns:
    dict: A valid JSON object containing the question and options.
    """
    if type == 'question':
        system_prompt = """You are an AI specialized in converting multiple-choice legal questions into JSON format.
        Ensure the output strictly follows this structure:
        ```json
        {"question": "...", "options": ["A ....", "B ...", "C ...", "D ..."]}
        """

    elif type == 'answer':
        system_prompt = """You are an AI specialized in converting legal answer into JSON format.
        Ensure the output strictly follows this structure:
        ```json
        {
        "Answer": "...", 
        "Justification": "..."
        }
        """

    user_prompt = f"""
        The following text needs to be formatted as a valid JSON:
        {llm_output}
        
        Please convert it into the required JSON format.
        """

    response = ollama_client.chat(model=model, messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    
    if type == 'answer':
        return response['message']['content']
    elif type == 'question':
        return validate_json_format_mcq(response['message']['content'], type)


def clean_generate_mcq_output(llm_output, type):
    """
    Cleans and extracts a valid JSON multiple-choice question from the LLM output.
    If the initial output is not valid JSON, a specialized LLM is called to correct it.

    Parameters:
    llm_output (str): Raw output from the LLM.

    Returns:
    dict: A properly formatted multiple-choice question.
    """
    result = validate_json_format_mcq(llm_output, type)
    if result:
        return result
    
    # If not valid, call formatting LLM
    formatted_result = call_formatting_llm_mcq(llm_output, type)
    if formatted_result:
        return formatted_result
    
    raise ValueError("Failed to convert LLM output into valid JSON format.")


def clean_output_v2(text, type):
    """ 
    Fist we call small model to translate in json style.
    If it's parsable we get the json. If not, we do regex.
    """

    if type == 'answer':
        text_json_like = call_formatting_llm_mcq(text, type)

        # Regex pattern to capture the content of "Answer" and "Justification"
        pattern = r'"Answer":\s*"([^"]+)"\s*,\s*"Justification":\s*"([^"]+)"'

        matches = re.search(pattern, text_json_like)

        if matches:
            answer = matches.group(1)
            # check for a valid letter isolated
            match = re.search(r'\b[A-D]\b', answer)
            if match:
                answer = match.group()

            justification = matches.group(2)
        else:
            raise ValueError("Can't extract data.")
        
        return {'Answer': answer, 'Justification': justification}