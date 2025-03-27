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


def create_question_dict(lines):
    """
    Creates a Python dictionary with questions and their choices.

    Args:
        lines (list): A list of strings, where each string is a line of text
                      extracted from the PDF.

    Returns:
        dict: A dictionary where keys are question numbers and values are
              dictionaries containing 'question' and 'options'.
    """
    questions_dict = {}
    current_question_number = None
    current_question_text = ""
    current_options = []
    option_count = 0  # Compteur pour suivre le nombre d'options

    for line in lines:
        question_match = re.search(r"(?:^|\s)(\d{1,2})\.\s+(.*)", line)
        option_match = re.search(r"([A-D])\.\s*(.*)", line)  # Limité à A-D
        if question_match:
            # On ignore un nouveau question_match si on n'a pas atteint D.
            if current_question_number is not None and option_count < 4:
                continue  # Ignore cette question
            
            # Sauvegarde de la question précédente
            if current_question_number is not None:
                questions_dict[current_question_number] = {
                    "question": current_question_text.strip(),
                    "options": [option.strip() for option in current_options]
                }

            # Initialisation d'une nouvelle question
            current_question_number = int(question_match.group(1))
            current_question_text = question_match.group(2).strip()
            current_options = []
            option_count = 0  # Réinitialisation du compteur d'options

        elif option_match:
            current_options.append(line.strip())
            option_count += 1  # Incrémentation du compteur d'options

        elif current_question_number is not None:
            # Gestion des questions ou options sur plusieurs lignes
            if not current_options:
                current_question_text += " " + line.strip()
            else:
                current_options[-1] += " " + line.strip()

    # Ajouter la dernière question si elle est valide (a atteint D.)
    if current_question_number is not None and option_count >= 4:
        questions_dict[current_question_number] = {
            "question": current_question_text.strip(),
            "options": [option.strip() for option in current_options]
        }

    return questions_dict

if __name__ == "__main__":
    pdf_file_path = "Datasets - v1/EPAC Exams/2024 - EPAC_exam_mcq.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = create_question_dict(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2024_EPAC_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")


    pdf_file_path = "Datasets - v1/EPAC Exams/2023 - EPAC_exam_MCQ_EN.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = create_question_dict(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2023_EPAC_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")

    
    pdf_file_path = "Datasets - v1/EPAC Exams/2022 - EPAC_exam_mcq_en.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = create_question_dict(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2022_EPAC_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")

    pdf_file_path = "Datasets - v1/EPAC Exams/MOCK2 - mock_mcq_en.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        lines = split_text_to_lines(extracted_text)
        questions_data = create_question_dict(lines)
        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2022_MOCK_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")
        