import logging
import aiohttp
from bs4 import BeautifulSoup
from html2text import HTML2Text
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
from crawl4ai import *


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebsiteViewerError(Exception):
    pass

async def fetch_website_content(url: str) -> Dict:
    """
    Fetch website content using aiohttp and BeautifulSoup.
    
    Args:
        url (str): The URL of the website to fetch
        
    Returns:
        Dict: A dictionary containing:
            - title: The page title (str)
            - content: The main content in markdown format (str)
            - links: List of absolute URLs found on the page (List[str])
            - images: List of image URLs found on the page (List[str])
            - url: The original URL (str)
    """
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(
                url=url,
            )
            soup = BeautifulSoup(result.html, 'html.parser')
            
            # Process links - convert relative URLs to absolute
            links = result.links
            
            # Process images - get src attributes
            media = result.media

            
            # Get title
            title = soup.title.string if soup.title else ''
            
            output = {
                "title": title,
                "markdown": result.markdown,
                "links": links,
                "media": media,
                "url": url
            }
            
            return output
        
    except Exception as e:
        logger.error(f"Error fetching website content: {str(e)}")
        raise WebsiteViewerError(f"Failed to fetch website content: {str(e)}") 