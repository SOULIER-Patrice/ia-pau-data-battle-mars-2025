import requests
from bs4 import BeautifulSoup
import re
import csv
import logging
from typing import Dict, List, Optional
from pathlib import Path
from utils import save_as_csv

# Configure logging to save to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("epc_scraper.log"),  # Save logs to this file
        logging.StreamHandler()  # Also output to console
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.epo.org/en/legal/epc/2020"

def parse_epc_page(url: str) -> Optional[str]:
    """
    Parse an EPC webpage and extract section title and content.
    
    Args:
        url: The webpage URL to parse
        
    Returns:
        Concatenated section title and content, or None if page couldn't be parsed
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad responses
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract section title
        section_title = extract_text_content(soup.find('h1', class_='h2'))
            
        # Extract content
        content = extract_text_content(soup.find('div', class_='epolegal-content'))
        
        # Combine title and content if either exists
        if section_title or content:
            full_content = f"{section_title} {content}".strip()
            # Replace non-breaking spaces
            return re.sub(r'\xa0', ' ', full_content)
        
        return None
    except requests.RequestException as e:
        return None
    except Exception as e:
        logger.error(f"Error processing {url}: {e}")
        return None


def extract_text_content(element) -> str:
    """
    Extract text content from a BeautifulSoup element, handling special cases.
    
    Args:
        element: BeautifulSoup element to process
        
    Returns:
        Processed text content
    """
    if not element:
        return ""
    
    # Create a copy to avoid modifying the original
    element_copy = BeautifulSoup(str(element), 'html.parser')
    
    # Remove 'Del' class elements
    for del_tag in element_copy.find_all(class_='Del'):
        del_tag.decompose()
    
    # Process footnote references
    for footnote_tag in element_copy.find_all(class_='FootnoteRef'):
        if footnote_tag.string and footnote_tag.string.strip().isdigit():
            footnote_tag.string = f"FootnoteRef{footnote_tag.string.strip()}"
    
    return element_copy.get_text(" ", strip=True)


def process_url_range(url_pattern: str, start: int, end: int, ref_prefix: str) -> List[Dict[str, str]]:
    """
    Process a range of URLs using a pattern and collect content.
    
    Args:
        url_pattern: URL pattern with {} placeholder for the index
        start: Starting index
        end: Ending index (inclusive)
        ref_prefix: Prefix for reference IDs
        
    Returns:
        List of dictionaries containing reference, URL, and content
    """
    results = []
    
    for i in range(start, end + 1):
        main_url = url_pattern.format(i)
        content = parse_epc_page(main_url)
        
        if content:
            logger.info(f"Processed {main_url}")
            results.append({
                'ref': f'{ref_prefix} {i}',
                'url': main_url,
                'content': content
            })
        
        # Process sub-sections (a, b, c, etc.)
        process_subsections(url_pattern.format(f"{i}{{}}"), ref_prefix, i, results)
    
    return results


def process_subsections(url_pattern: str, ref_prefix: str, parent_num: int, results: List[Dict[str, str]]):
    """
    Process subsections of EPC articles or rules.
    
    Args:
        url_pattern: URL pattern with {} placeholder for the subsection letter
        ref_prefix: Prefix for reference IDs
        parent_num: Parent article or rule number
        results: List to append results to
    """
    for letter_code in range(97, 123):  # ASCII codes for a-z
        letter = chr(letter_code)
        url = url_pattern.format(letter)
        content = parse_epc_page(url)
        
        if content:
            logger.info(f"Processed {url}")
            results.append({
                'ref': f'{ref_prefix} {parent_num}{letter}',
                'url': url,
                'content': content
            })
        else:
            # Stop if a page is not found - assuming consecutive lettering
            break


def get_epc_content(article_range: tuple = (1, 178), rule_range: tuple = (1, 165), fee_range: tuple = (1, 15)) -> List[Dict[str, str]]:
    """
    Fetch content from EPC articles and rules.
    
    Args:
        article_range: Tuple of (start, end) for article numbers
        rule_range: Tuple of (start, end) for rule numbers
        
    Returns:
        List of dictionaries containing reference, URL, and content
    """
    all_content = []
    
    # Process articles
    article_start, article_end = article_range
    all_content.extend(
        process_url_range(
            f"{BASE_URL}/a{{}}.html",
            article_start,
            article_end,
            "EPC Article"
        )
    )
    
    # Process rules
    rule_start, rule_end = rule_range
    all_content.extend(
        process_url_range(
            f"{BASE_URL}/r{{}}.html",
            rule_start,
            rule_end,
            "EPC Rules"
        )
    )

    # Process fees
    fee_start, fee_end = fee_range
    all_content.extend(
        process_url_range(
            f"{BASE_URL}/f{{}}.html",
            fee_start,
            fee_end,
            "EPC Fees"
        )
    )
    
    logger.info(f"EPC processing complete. Collected {len(all_content)} items.")
    return all_content


if __name__ == '__main__':
    # Use full ranges for production
    article_range = (1, 178)
    rule_range = (1, 165)
    fee_range = (1, 15)
    
    epc_content = get_epc_content(article_range, rule_range, fee_range)
    
    output_path = Path('../../outputs/EPC.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    save_as_csv(epc_content, output_path)
    logger.info(f"Data saved to {output_path}")