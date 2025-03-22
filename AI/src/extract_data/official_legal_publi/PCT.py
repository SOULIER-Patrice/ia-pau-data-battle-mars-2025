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
        logging.FileHandler("logs/pct_scraper.log"),  # Save logs to this file
        logging.StreamHandler()  # Also output to console
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.wipo.int/pct/en/texts/"

def parse_pct_page(url: str) -> Optional[str]:
    """
    Parse an PCT webpage and extract section title and content.
    
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
        
        # Replace <br /> tags with spaces in the HTML
        for br in soup.find_all('br'):
            br.replace_with(' ')
            
        article_div = soup.find("div", class_="content--article")
        content = ""
        
        if article_div:
            # Add space between text extracted from the tags
            content = " ".join(tag.get_text(strip=False) for tag in article_div.find_all(["p", "h1", "h2", "h3"]))

            # Remove multiple spaces (replace with a single space)
            content = re.sub(r'\s+', ' ', content)

            # Strip leading and trailing spaces
            content = content.strip()
            
            return content
        
        else:
            return None
    except requests.RequestException as e:
        return None
    except Exception as e:
        logger.error(f"Error processing {url}: {e}")
        return None


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
        content = parse_pct_page(main_url)
        
        if content:
            logger.info(f"Processed {main_url}")
            results.append({
                'ref': f'{ref_prefix} {i}',
                'url': main_url,
                'content': f'Title: {ref_prefix} {i}. Content: {content}'
            })
    
    return results


def get_pct_content(article_range: tuple = (1, 69), rule_range: tuple = (1, 96)) -> List[Dict[str, str]]:
    """
    Fetch content from PCT articles and rules.
    
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
            f"{BASE_URL}/articles/a{{}}.html",
            article_start,
            article_end,
            "PCT Article"
        )
    )
    
    # Process rules
    rule_start, rule_end = rule_range
    all_content.extend(
        process_url_range(
            f"{BASE_URL}/rules/r{{}}.html",
            rule_start,
            rule_end,
            "PCT Rule"
        )
    )

    
    logger.info(f"PCT processing complete. Collected {len(all_content)} items.")
    return all_content


if __name__ == '__main__':
    # Use full ranges for production
    article_range = (1, 69)
    rule_range = (1, 96)
    
    pct_content = get_pct_content(article_range, rule_range)
    
    output_path = Path('../../../outputs/PCT.csv')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    save_as_csv(pct_content, output_path)
    logger.info(f"Data saved to {output_path}")