import re
import requests
import time
import csv
from bs4 import BeautifulSoup
from utils import save_as_csv


def convert_gl_value(gl_value):
    """
    Converts a value like GLA_CI_1 to a format like EPC Guidelines PartAChapI(1), 
    or GLI_1 to EPC Guidelines GeneralPart(1), or GLA_CI to EPC Guidelines PartAChapI without numbers.
    
    Args:
        gl_value (str): The value to convert, such as "GLA_CI", "GLA_CI_1" or "GLI_1".
    
    Returns:
        str: The value converted to the format "EPC Guidelines PartAChapI" or "EPC Guidelines PartAChapI(1)".
    """
    # Check for GLI pattern (GeneralPart)
    if gl_value.startswith("GLI"):
        match = re.match(r"GLI_?((?:\d+_?)+)?", gl_value)
        if match:
            numbers = match.group(1)  # "1", "4_1_3_1" (etc.) or None if no numbers
            
            if numbers:
                # Split the numbers by underscores and format them in parentheses
                number_list = numbers.split('_')
                formatted_numbers = ''.join(f"({num})" for num in number_list)
                return f"EPC Guidelines GeneralPart{formatted_numbers}"
            else:
                return "EPC Guidelines GeneralPart"
    
    # Handle the other cases (GLA_CI, GLA_CII, etc.)
    match = re.match(r"GLA_C([A-Z]+)_?((?:\d+_?)+)?", gl_value)
    
    if match:
        part = match.group(1)  # "I", "II" (etc.)
        numbers = match.group(2)  # "1", "4_1_3_1" (etc.) or None if no numbers
        
        # Mapping for part names (like "I" → "PartAChapI", "II" → "PartAChapII")
        part_map = {
            "I": "PartAChapI",
            "II": "PartAChapII",
            # You can extend this map if there are more parts
        }
        
        # Get the part name (Chapter)
        part_name = part_map.get(part, f"PartAChap{part}")
        
        if numbers:
            # Split the numbers by underscores and format them in parentheses
            number_list = numbers.split('_')
            formatted_numbers = ''.join(f"({num})" for num in number_list)
            # Format and return the result string with numbers
            return f"EPC Guidelines {part_name}{formatted_numbers}"
        else:
            # Return the result without numbers
            return f"EPC Guidelines {part_name}"
    else:
        raise ValueError(f"The format of '{gl_value}' is incorrect.")


def parse_epc_guidelines(url):
    """
    Extracts information from EPC Guidelines on a webpage.
    
    For each ID starting with 'GL...', the function extracts:
    - The ID as a reference
    - The content of the corresponding <p> tag
    - The section title from the 'h1' tag with class 'h2'
    - The first paragraph text from each 'epolegal-content' div
    
    Args:
        url (str): URL of the page to analyze
        
    Returns:
        list[dict]: List of dictionaries containing extracted references and content
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []

    # Get section title from h1 with class 'h2', excluding 'Del' class elements
    section_title_tag = soup.find('h1', class_='h2')
    if section_title_tag:
        # Exclude 'Del' class elements
        for del_tag in section_title_tag.find_all(class_='Del'):
            del_tag.decompose()  # Remove the 'Del' elements
        section_title = section_title_tag.get_text(strip=True)
    else:
        section_title = ""
    

    for epolegal_div in soup.find_all('div', class_='epolegal-content'):
        div_title_tag = epolegal_div.find('p')
        div_title = div_title_tag.get_text(strip=True) if div_title_tag else ""
        
        reference = epolegal_div.get('id')
        if reference and reference.startswith('GL'):
            all_paragraphs = epolegal_div.find_all('p', class_=lambda x: x != 'Del')
            combined_text = ' '.join(p.get_text(strip=True) for p in all_paragraphs)
            content = f"{section_title} {div_title} {combined_text}"
            results.append({'ref': convert_gl_value(reference), 'url': url, 'content': content})

    return results


def url_exists(url):
    """
    Checks if a URL exists via an HTTP HEAD request.
    Returns True if the status_code is 200.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


def build_url(base_url, letter, roman, path=None):
    """
    Builds the URL from the prefix (letter and Roman numeral)
    and the list of numbers in the hierarchy.
    """
    if not path:
        if roman != '':
            return f"{base_url}{letter}_{roman}.html"
        else:
            return f"{base_url}{letter}.html"
    hierarchical_part = "_".join(map(str, path))
    if roman != '':
        return f"{base_url}{letter}_{roman}_{hierarchical_part}.html"
    else:
        return f"{base_url}{letter}_{hierarchical_part}.html"


def explore_hierarchy(base_url, letter, roman, path, all_guidelines):
    """
    Recursively explores the hierarchical branch for a given prefix.
    """
    url = build_url(base_url, letter, roman, path)
    
    if url_exists(url):
        # Read content and add it
        try:
            guidelines = parse_epc_guidelines(url)
            if guidelines:
                all_guidelines.extend(guidelines)
                print(f'Succeed {url}')
            else:
                print(f"No clauses found on {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
        # print(f'Url found: {url}')

        # Try to explore deeper
        explore_hierarchy(base_url, letter, roman, path + [1], all_guidelines)
        
        # Try next at the same level
        if path:
            next_path = path[:-1] + [path[-1] + 1]
            explore_hierarchy(base_url, letter, roman, next_path, all_guidelines)
    


def get_epc_guidelines_url(base_url='https://www.epo.org/en/legal/guidelines-epc/2024/'):
    """
    Returns all contents from all existing URLs for the EPC guidelines.
    
    Args:
        base_url (str): The base URL of the EPC guidelines.
        
    Returns:
        list: List of all valid guidelines found.
    """
    # List to store all found guidelines
    all_guidelines = []

    # Get General part Introduction
    explore_hierarchy(base_url, 'foreword', '', [], all_guidelines)

    # Get other parts
    # Letters to explore (based on EPC guidelines structure)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv']


    # Main loop to explore all letters and Roman numerals
    for letter in letters:
        for roman in romans:
            # Start with empty path to check if base exists
            explore_hierarchy(base_url, letter, roman, [], all_guidelines)

    return all_guidelines


if __name__ == '__main__':
    # # EPC Guidelines get urls
    # epc_guidelines = get_epc_guidelines_url()
    # save_as_csv(epc_guidelines, '../../outputs/EPC_guidelines.csv')


    # TEMP POUR TEST -----------------

    # Pour les tests je redirige les prints vers un fichier log.
    import sys
    import logging

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level to INFO (or DEBUG, ERROR as needed)
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Output to console
            logging.FileHandler('EPC_guidelines_get_data.log')  # Output to a log file
        ]
    )

    # Custom class to capture printed output and log it
    class PrintLogger:
        def write(self, message):
            if message != '\n':  # Avoid logging blank newlines
                logging.info(message.strip())  # Log the message

        def flush(self):  # Required method for file-like objects
            pass

    # Redirect print statements to the logging system
    sys.stdout = PrintLogger()

    print("Starting the EPC Guidelines processing...")
    
    # EPC Guidelines get urls (your function should have print statements)
    epc_guidelines = get_epc_guidelines_url()
    
    print("Saving EPC Guidelines to CSV...")
    save_as_csv(epc_guidelines, '../../outputs/EPC_guidelines.csv')
    
    print("EPC Guidelines processing complete.")
