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


def extract_question_data(text):
    """
    Extracts questions, answers, and justifications from the provided text.

    Args:
        text (str): The extracted text from the PDF.

    Returns:
        list: A list of dictionaries, where each dictionary contains the question,
              answer, and justification.
    """
    questions_data = []

    
                  
    # Regular expression to match Question number and Answer
    question_answer_regex = re.compile(r"Question (\d+): (\w)\s+(.*?)(?=(Question \d+:|$))", re.DOTALL)
    print(question_answer_regex)
    matches = question_answer_regex.findall(text)

    for match in matches:
        question_number = match[0]
        answer = match[1]
        justification = match[2].strip()

        justification_lines = justification.split('\n')
        justification = " ".join([line.strip() for line in justification_lines if line.strip()])  # Clean each line
        
        # Store in the dictionary
        question_dict = {
            "Question Number": question_number,
            "Answer": answer,
            "Justification": justification
        }

        questions_data.append(question_dict)

    return questions_data

if __name__ == "__main__":
    pdf_file_path = "Datasets - v1/EPAC Exams/2024 - EPAC_solution_mcq.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        questions_data = extract_question_data(extracted_text)

        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2024_EPAC_solution_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")

    pdf_file_path = "Datasets - v1/EPAC Exams/2023 - EPAC_solution_mcq.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        questions_data = extract_question_data(extracted_text)

        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2023_EPAC_solution_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")

    pdf_file_path = "Datasets - v1/EPAC Exams/2022 - EPAC_Solution_mcq&open.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        questions_data = extract_question_data(extracted_text)

        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2022_EPAC_solution_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")


    pdf_file_path = "Datasets - v1/EPAC Exams/MOCK2 - mock_mcq_solutions_en.pdf"  # Replace with the path to your PDF file
    extracted_text = extract_text_pypdf2(pdf_file_path)

    if extracted_text:
        questions_data = extract_question_data(extracted_text)

        print(json.dumps(questions_data, indent=4, ensure_ascii=False))
        json_filename = "outputs/2022_MOCK_solution_mcq.json"

        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(questions_data, json_file, indent=4, ensure_ascii=False)

        print(f"File {json_filename} saved successfully!")