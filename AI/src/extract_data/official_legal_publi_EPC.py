import requests
from bs4 import BeautifulSoup
import re
import csv
from utils import save_as_csv



def _parse_EPC(url):
    """
    Parses the given URL and extracts the section title and content from the page.
    - The section title is obtained from an <h1> tag with class 'h2', excluding elements with class 'Del'.
    - The content is extracted from a <div> with class 'epolegal-content', also excluding elements with class 'Del'.
    - If a number is found inside a tag with class 'footnote', it is prefixed with 'footnote '.
    
    Args:
        url (str): The webpage URL to parse.
    
    Returns:
        str: The concatenated section title and content.
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract section title
    section_title_tag = soup.find('h1', class_='h2')
    if section_title_tag:
        for del_tag in section_title_tag.find_all(class_='Del'):
            del_tag.decompose()  # Remove 'Del' class elements
        
        # Add 'footnote' before numbers inside footnote class elements in the title
        for footnote_tag in section_title_tag.find_all(class_='FootnoteRef'):
            if footnote_tag.string and footnote_tag.string.strip().isdigit():
                footnote_tag.string = f"FootnoteRef{footnote_tag.string.strip()}"
        
        section_title = section_title_tag.get_text(" ", strip=True)
    else:
        section_title = ""
        
    # Extract content
    content_div = soup.find('div', class_='epolegal-content')
    if content_div:
        for del_tag in content_div.find_all(class_='Del'):
            del_tag.decompose()  # Remove 'Del' class elements
        
        # Add 'footnote' before numbers inside footnote class elements in the content
        for footnote_tag in content_div.find_all(class_='FootnoteRef'):
            if footnote_tag.string and footnote_tag.string.strip().isdigit():
                footnote_tag.string = f"FootnoteRef{footnote_tag.string.strip()}"
        
        content = content_div.get_text(" ", strip=True)
    else:
        content = ""

    full_content = ''
    if section_title != '' or content != '':
        full_content = section_title + " " + content
        # Supprimer tous les \xa0
        full_content = re.sub(r'\xa0', ' ', full_content)
                    
    return full_content
    

def get_EPC():
    """
    """
    all_content = []
    
    # Process articles from a1.html to a178.html
    # for i in range(1, 179):
    for i in range(101, 107):
        url = f"https://www.epo.org/en/legal/epc/2020/a{i}.html"
        try:
            content = _parse_EPC(url)
            if content:
                print(f"Processing {url}...")
                all_content.append({'ref': f'EPC Article {i}', 'url': url, 'content': content})
        except Exception as e:
            print(f"Error processing {url}: {e}")
        
        # Gestion des sous parties
        sub_section = True
        letter = 97 # on commence à a
        while sub_section:
            url = f"https://www.epo.org/en/legal/epc/2020/a{i}{chr(letter)}.html"
            try:
                content = _parse_EPC(url)
                if content:
                    print(f"Processing {url}...")
                    all_content.append({'ref': f'EPC Article {i}{chr(letter)}', 'url': url, 'content': content})
                    letter += 1  # on passe à la lettre suivante
                else:
                    sub_section = False
            except Exception as e:
                print(f"Error processing {url}: {e}")



    # Process rules
    # for i in range(1, 166):
    for i in range(5, 9):
        url = f"https://www.epo.org/en/legal/epc/2020/r{i}.html"
        try:
            content = _parse_EPC(url)
            if content:
                print(f"Processing {url}...")
                all_content.append({'ref': f'EPC Rules {i}', 'url': url, 'content': content})
        except Exception as e:
            print(f"Error processing {url}: {e}")


        # Gestion des sous parties
        sub_section = True
        letter = 97 # on commence à a
        while sub_section:
            url = f"https://www.epo.org/en/legal/epc/2020/r{i}{chr(letter)}.html"
            try:
                content = _parse_EPC(url)
                if content:
                    print(f"Processing {url}...")
                    all_content.append({'ref': f'EPC Rules {i}{chr(letter)}', 'url': url, 'content': content})
                    letter += 1  # on passe à la lettre suivante
                else:
                    sub_section = False
            except Exception as e:
                print(f"Error processing {url}: {e}")


    print('EPC processed.')
    return all_content
    


if __name__ == '__main__':
    # EPC
    EPC = get_EPC()
    save_as_csv(EPC, '../../outputs/EPC.csv')