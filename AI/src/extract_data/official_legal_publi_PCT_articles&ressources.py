import requests
from bs4 import BeautifulSoup
import re
import csv


# Utils -----------------------------------------------------------------------------------------------------
def save_as_csv(data, csv_filename):
    """
    Save data to a CSV file.
    
    Args:
        data (list[dict]): List of dictionaries to save
        csv_filename (str): Path to save the CSV file
    """
    # Write to CSV file
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        # Define column names from the keys of the first dictionary
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write header (column names)
        writer.writeheader()
        
        # Write data rows
        writer.writerows(data)
        
    print(f"File {csv_filename} saved successfully!")


# PCT articles -----------------------------------------------------------------------------------------------------
def _parse_pct_articles(url):
    """
    Extract information from PCT article tags on a webpage.
    
    For each tag found, the function extracts:
    - Article number and reference level from the 'name' attribute of the <a> tag
    - Paragraph content with the initial reference text removed
    
    Args:
        url (str): URL of the page to analyze
        
    Returns:
        list[dict]: List of dictionaries containing extracted references and content
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    
    for p_tag in soup.find_all('p'):
        a_tag = p_tag.find('a')
        if a_tag and a_tag.has_attr('name'):
            name_value = a_tag['name'].lstrip('_')
            parts = [part for part in name_value.split('_') if part]
            
            if len(parts) >= 2:
                article_number = parts[0]
                clause_parts = parts[1:]
                reference = f"Article {article_number}" + "".join(f"({part})" for part in clause_parts)
                full_text = p_tag.get_text().strip()
                
                # Remove redundant numbering at the beginning
                content = re.sub(r'^(?:\([^)]*\)\s*)+', '', full_text).rstrip(';').strip()
                results.append({'ref': reference, 'url': url, 'content': content})
                
    return results


def get_pct_articles():
    """
    Retrieve all PCT articles from the WIPO website.
    
    Processes articles from a1.html to a69.html and handles a special case for Article 26(1).
    
    Returns:
        list[dict]: List of dictionaries containing all article references and content
    """
    all_clauses = []
    
    # Process articles from a1.html to a69.html
    for i in range(1, 70):
        url = f"https://www.wipo.int/pct/en/texts/articles/a{i}.html"
        print(f"Processing {url}...")
        
        try:
            clauses = _parse_pct_articles(url)
            if clauses:
                all_clauses.extend(clauses)
            else:
                print(f"No clauses found on {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    print('Articles processed.')
    
    # Manual correction for Article 26(1) due to unique HTML error
    print('Processing special case: Article 26(1)')
    for clause in all_clauses:
        if clause['ref'] == "Article 26(1)":
            clause['content'] = ('No designated Office shall reject an international application on the grounds of '
                               'non-compliance with the requirements of this Treaty and the Regulations without '
                               'first giving the applicant the opportunity to correct the said application to the '
                               'extent and according to the procedure provided by the national law for the same or '
                               'comparable situations in respect of national applications.')
    
    return all_clauses


# PCT rules -----------------------------------------------------------------------------------------------------
def _parse_pct_rules(url):
    """
    Extract information from PCT rule tags on a webpage.

    For each tag found, the function extracts:
    - Rule number and reference level from the 'name' attribute of the <a> tag
    - Paragraph content with the initial reference text removed

    Args:
        url (str): URL of the page to analyze

    Returns:
        list[dict]: List of dictionaries containing extracted references and content
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    
    # Trouver la div content--article
    content_div = soup.find('div', class_='content--article')
    if not content_div:
        return results  # Retourner une liste vide si la div n'est pas trouvée
    
    for p_tag in content_div.find_all('p'):
        a_tag = p_tag.find('a')
        if a_tag and a_tag.has_attr('name'):
            name_value = a_tag['name'].lstrip('_')
            parts = [part for part in name_value.split('_') if part]
            
            if len(parts) >= 2:
                article_number = parts[0]
                clause_parts = parts[1:]
                reference = f"Rule {article_number}" + "".join(f"({part})" for part in clause_parts)
                full_text = p_tag.get_text().strip()
                
                # Remove redundant numbering at the beginning
                content = re.sub(r'^(?:\s*(?:\d+(?:\.\d+)?(?:bis)?|\(\w+\))\s+)+', '', full_text).rstrip(';').strip()
                # Supprimer tous les \xa0
                content = re.sub(r'\xa0', ' ', content)       
                
                results.append({'ref': reference, 'url': url, 'content': content})
        else:
            # Si la balise <p> ne contient pas une balise <a> avec un 'name', on concatène son contenu au dernier enregistré
            full_text = p_tag.get_text().strip()

            if results:  # Vérifier si on a déjà un résultat dans la liste
                last_result = results[-1]  # Prendre le dernier résultat
                last_result['content'] += ' ' + full_text  # Concaténer au contenu précédent
            else:
                # Si aucun résultat précédent n'existe, on ajoute un nouveau dictionnaire avec le contenu
                results.append({'ref': '', 'content': content})
    
    return results


def get_pct_rules():
    """
    Retrieve all PCT rules from the WIPO website.
    
    Processes articles from r1.html to r96.html.
    
    Returns:
        list[dict]: List of dictionaries containing all rules references and content
    """
    all_clauses = []
    
    # Process articles from a1.html to a96.html
    for i in range(1, 97):
        url = f"https://www.wipo.int/pct/en/texts/rules/r{i}.html"
        print(f"Processing {url}...")
        
        try:
            clauses = _parse_pct_rules(url)
            if clauses:
                all_clauses.extend(clauses)
            else:
                print(f"No clauses found on {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    print('Rules processed.')

    return all_clauses


if __name__ == '__main__':
    # PCT Articles
    pct_articles = get_pct_articles()
    save_as_csv(pct_articles, './outputs/PCT_articles.csv')

    # PCT Rules
    pct_rules = get_pct_rules()
    save_as_csv(pct_rules, './outputs/PCT_rules.csv')