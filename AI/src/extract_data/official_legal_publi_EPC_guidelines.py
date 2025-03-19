import requests
import time
import csv


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
        return f"{base_url}{letter}_{roman}.html"
    hierarchical_part = "_".join(map(str, path))
    return f"{base_url}{letter}_{roman}_{hierarchical_part}.html"


def explore_hierarchy(base_url, letter, roman, path, all_urls):
    """
    Recursively explores the hierarchical branch for a given prefix.
    """
    url = build_url(base_url, letter, roman, path)
    
    if url_exists(url):
        print(f'Url found: {url}')
        all_urls.append(url)
        # Try to explore deeper
        explore_hierarchy(base_url, letter, roman, path + [1], all_urls)
        
        # Try next at the same level
        if path:
            next_path = path[:-1] + [path[-1] + 1]
            explore_hierarchy(base_url, letter, roman, next_path, all_urls)
    
    # time.sleep(0.2)  # To avoid overloading the server


def get_epc_guidelines_url(base_url='https://www.epo.org/en/legal/guidelines-epc/2024/'):
    """
    Returns all contents from all existing URLs for the EPC guidelines.
    
    Args:
        base_url (str): The base URL of the EPC guidelines.
        
    Returns:
        list: List of all valid URLs found.
    """
    # List to store all found URLs
    all_urls = []
    
    # Letters to explore (based on EPC guidelines structure)
    # letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    # romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv']
    letters = ['a', 'b']
    romans = ['i', 'ii', 'iii']


    # Main loop to explore all letters and Roman numerals
    for letter in letters:
        for roman in romans:
            # Start with empty path to check if base exists
            explore_hierarchy(base_url, letter, roman, [], all_urls)
    return all_urls


if __name__ == '__main__':
    # EPC Guidelines get urls
    epc_guidelines_url = get_epc_guidelines_url()

    # Écriture de la liste dans un fichier CSV
    path = './outputs/EPC_guidelines_url.csv'

    # Sauvegarde dans un fichier CSV
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for url in epc_guidelines_url:
            writer.writerow([url])

    print(f"Le fichier a été créé avec succès dans {path} !")