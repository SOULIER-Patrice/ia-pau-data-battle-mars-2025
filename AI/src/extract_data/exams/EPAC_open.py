from PyPDF2 import PdfReader
import re
import json


def extract_text_pypdf2(pdf_path):
    """
    Extracts text content from a PDF file using PyPDF2.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str or None: The extracted text as a single string, or None if an error occurs.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except FileNotFoundError:
        print(f"Error: The file '{pdf_path}' was not found.")
        return None
    return text

def split_text_to_lines(text):
    """
    Splits a string of text into a list of individual lines.

    Args:
        text (str): The input text.

    Returns:
        list: A list where each element is a line of the input text.
    """
    return text.splitlines() if text else []


def extract_questions(lines):
    """
    Extracts questions from the given lines of text.
    Assumes that questions are numbered and followed by their content.

    Args:
        lines (list): List of text lines.

    Returns:
        dict: A dictionary where keys are question numbers and values are question content.
    """
    questions = {}
    current_question_number = None
    current_question_content = ""

    question_pattern = re.compile(r"\s*(\d+)\.\s*\((\d+)\s*points?\)\s*")

    for line in lines:
        # If the line matches the pattern of a question

        if question_pattern.search(line) :
            if current_question_number is not None:
                # If we already have a question, add it to the dictionary
                questions[current_question_number] = current_question_content
            
            # Start a new question
            parts = line.split(')')  # Split at the closing parenthesis to separate points
            current_question_number = parts[0].strip()[0]  # Get the question number
            current_question_content = parts[1].strip()  # Get the question content (after the closing parenthesis)
        
        elif current_question_number is not None:
            # Continue appending content to the current question if it's not a new question
            current_question_content += " " + line.strip()

    # Add the last question if it exists
    if current_question_number is not None:
        questions[current_question_number] = current_question_content

    return questions



if __name__ == "__main__":
    pdf_file_path = "Datasets - v1/EPAC Exams/2024 - EPAC_exam_open.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = extract_questions(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2024_EPAC_open.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")

    
    pdf_file_path = "Datasets - v1/EPAC Exams/2023 - EPAC_exam_open_EN.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = extract_questions(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2023_EPAC_open.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")
        
    pdf_file_path = "Datasets - v1/EPAC Exams/2022 - EPAC_exam_open_en.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)
    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = extract_questions(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2022_EPAC_open.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")
        