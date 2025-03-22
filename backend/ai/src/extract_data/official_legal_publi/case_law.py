import re
import requests
import time
import csv
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import save_as_csv


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler('case_law_guidelines_scraper.log')  # Output to a log file
    ]
)
logger = logging.getLogger(__name__)


class ClReferenceConverter:
    """Gère la conversion des identifiants CLR en références lisibles au format Case Law."""
    
    @staticmethod
    def convert(cl_string: str) -> str:
        """
        Convertit une chaîne CLR en référence Case Law.

        Exemples:
            CLR_VII_2        -> "Case Law VII, 2"
            CLR_VI_1         -> "Case Law VI, 1"
            CLR_I_A_1        -> "Case Law I-a, 1"
            CLR_I_B_2_1_2    -> "Case Law I-b, 2.1.2"

        Args:
            cl_string: Référence CLR à convertir.

        Returns:
            Référence Case Law formatée.
        """
        # Découper la chaîne sur le séparateur "_"
        parts = cl_string.split("_")
        
        # Vérifier le format de base : doit contenir au moins ["CLR", section, numéro(s)]
        if len(parts) < 3 or parts[0] != "CLR":
            return "Invalid format"
        
        # La première partie (après "CLR") est la section en chiffres romains
        section = parts[1]
        
        # Initialisation pour la sous-section éventuelle et index de départ pour les numéros
        sub_section = ""
        numbers_start_index = 2
        
        # Si le troisième élément est une lettre (par exemple "A" ou "B"), c'est la sous-section
        if len(parts) >= 4 and parts[2].isalpha() and len(parts[2]) == 1:
            sub_section = parts[2].lower()  # convertir en minuscule pour correspondre au format "I-a"
            numbers_start_index = 3
        
        # Construire la référence de base
        result = f"Case Law {section}"
        if sub_section:
            result += f"-{sub_section}"
        
        # Si des parties numériques supplémentaires existent, les joindre avec des points
        if len(parts) > numbers_start_index:
            numbers = parts[numbers_start_index:]
            result += ", " + ".".join(numbers)
        
        return result
    

class CaseLawParser:
    """Handles the parsing of EPC Guidelines web pages."""
    
    def __init__(self, base_url: str):
        """
        Initialize the parser with a base URL.
        
        Args:
            base_url: The base URL for EPC guidelines
        """
        self.base_url = base_url
        self.session = requests.Session()
        # Setting reasonable timeout and headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def parse_page(self, url: str) -> List[Dict[str, str]]:
        """
        Extract information from EPC Guidelines on a webpage.
        
        For each ID starting with 'GL...', extracts:
        - The ID as a reference (converted to human-readable format)
        - The content of the corresponding <p> tags
        - The section title from the 'h1' tag with class 'h2'
        
        Args:
            url: URL of the page to analyze
            
        Returns:
            List of dictionaries containing extracted references and content
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  # Raise exception for bad responses
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.content, 'html.parser')
            results = []

            # Get section title from h1 with class 'h2', excluding 'Del' class elements
            section_title = self._extract_section_title(soup)

            # Process each legal content div
            for epolegal_div in soup.find_all('div', class_='epolegal-content'):
                reference = epolegal_div.get('id')
                if reference and reference.startswith('CLR'):
                    # Extract all non-deleted paragraphs
                    content = self._extract_content(epolegal_div, section_title)
                    readable_ref = ClReferenceConverter.convert(reference)
                    results.append({
                        'ref': readable_ref, 
                        'url': url, 
                        'content':  f'Title: {readable_ref}. Content: {content}'
                    })

            return results
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")
            return []
    
    def _extract_section_title(self, soup: BeautifulSoup) -> str:
        """
        Extract section title from the page, filtering out deleted content.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Extracted section title
        """
        section_title_tag = soup.find('h1', class_='h2')
        if not section_title_tag:
            return ""
            
        # Exclude 'Del' class elements
        for del_tag in section_title_tag.find_all(class_='Del'):
            del_tag.decompose()
            
        return section_title_tag.get_text(strip=True)
    
    def _extract_content(self, div: BeautifulSoup, section_title: str) -> str:
        """
        Extract content from a div, combining with section title.
        
        Args:
            div: BeautifulSoup div object containing content
            section_title: Section title to prepend to content
            
        Returns:
            Combined text content
        """
        # Find the first paragraph for div title
        div_title_tag = div.find('p')
        div_title = div_title_tag.get_text(strip=True) if div_title_tag else ""
        
        # Gather all paragraphs except those with class 'Del'
        all_paragraphs = div.find_all('p', class_=lambda x: x != 'Del')
        combined_text = ' '.join(p.get_text(strip=True) for p in all_paragraphs)
        
        # Combine all parts
        return f"{section_title} {div_title} {combined_text}"

    def url_exists(self, url: str) -> bool:
        """
        Check if a URL exists via an HTTP HEAD request.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL exists and returns 200 status
        """
        try:
            response = self.session.head(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False



class CaseLawExplorer:
    """Explores the hierarchy of Case Law URLs."""
    
    def __init__(self, base_url: str):
        """
        Initialize the explorer with a base URL.
        
        Args:
            base_url: Base URL for the Case law.
        """
        self.base_url = base_url
        self.parser = CaseLawParser(base_url)

        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                        'y', 'z']
        self.romans = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii']
    
    def build_url(self, letter: str, roman: str, path: List[int] = None) -> str:
        """
        Build a URL from components.
        
        Args:
            letter: Letter part of the reference (e.g., 'a', 'b')
            roman: Roman numeral part (e.g., 'i', 'ii')
            path: List of numbers representing the hierarchical path
            
        Returns:
            Complete URL
        """
        if not path:
            if letter:
                return f"{self.base_url}_{roman}_{letter}.html"
            else:
                return f"{self.base_url}_{roman}.html"


        hierarchical_part = "_".join(map(str, path))

        if letter:
            return f"{self.base_url}_{roman}_{letter}_{hierarchical_part}.html"
        else:
            return f"{self.base_url}_{roman}_{hierarchical_part}.html"
        

    
    def explore_hierarchy(self, letter: str, roman: str, path: List[int], 
                          results: List[Dict[str, str]]):
        """
        Recursively explore the hierarchical branch for a given prefix.
        
        Args:
            letter: Letter component
            roman: Roman numeral component
            path: Current hierarchical path as list of integers
            results: List to collect results
        """
        url = self.build_url(letter, roman, path)
        
        if self.parser.url_exists(url):
            # Read content and add it
            guidelines = self.parser.parse_page(url)
            if guidelines:
                results.extend(guidelines)
                logger.info(f'Processed: {url}')
            else:
                logger.info(f"No guidelines found on {url}")
        
            # Try to explore deeper (add a '1' to the path)
            self.explore_hierarchy(letter, roman, path + [1], results)
            
            # Try next at the same level (increment the last number)
            if path:
                next_path = path[:-1] + [path[-1] + 1]
                self.explore_hierarchy(letter, roman, next_path, results)

    
    def get_all_guidelines(self) -> List[Dict[str, str]]:
        """
        Explore all possible URLs and collect guidelines.
        
        Returns:
            List of dictionaries with reference, URL, and content
        """
        all_guidelines = []
        
        # Get foreword
        logger.info("Exploring foreword section...")
        self.explore_hierarchy('foreword', '', [1], all_guidelines)
        
        # Explore all letter and Roman numeral combinations
        for letter in self.letters:
            logger.info(f"Exploring part {letter.upper()}...")
            for roman in self.romans:
                self.explore_hierarchy(letter, roman, [], all_guidelines)
        
        logger.info(f"Found {len(all_guidelines)} guidelines in total.")
        return all_guidelines


if __name__ == '__main__':
    base_url = 'https://www.epo.org/en/legal/case-law/2022'
    
    logger.info("Starting EPC Guidelines scraper...")
    
    explorer = CaseLawExplorer(base_url)
    epc_guidelines = explorer.get_all_guidelines()
    
    # Ensure output directory exists
    output_path = Path('../../outputs/EPC_guidelines.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving {len(epc_guidelines)} guidelines to CSV...")
    save_as_csv(epc_guidelines, output_path)
    
    logger.info("EPC Guidelines processing complete.")