import aiohttp
from bs4 import BeautifulSoup
import re
from website_viewer import fetch_website_content

async def search_n_browse(search_phrase: str) -> dict:
    url = "https://lite.duckduckgo.com/lite/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "q": search_phrase,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    body = await response.text()
                    soup = BeautifulSoup(body, 'html.parser')
                    
                    # Extract links
                    links = [a['href'] for a in soup.find_all('a', href=True) 
                            if not a['href'].startswith('#')]
                    links = [link if link.startswith('http') else '' for link in links]

                    # Extract titles
                    titles = [a.text.strip() for a in soup.select('tr > td > a')]

                    # Extract snippets
                    snippets = [td.text.strip() for td in soup.select('td.result-snippet')]

                    # Extract link texts
                    link_texts = [span.text for span in soup.select('td > span.link-text')]

                    # Process results
                    json_data = {}
                    if snippets:
                        for index, snippet in enumerate(snippets):
                            json_data[f"Item_{index + 1}"] = {
                                "title": titles[index] if index < len(titles) else "",
                                "snippet": snippet,
                                "linkText": link_texts[index] if index < len(link_texts) else "",
                            }
                    else:
                        json_data["Result"] = {
                            "title": "No results were found.",
                            "snippet": "Our search engine could not find what you are looking for.",
                            "linkText": "Thank you for using our search engine.",
                        }

                    return json_data
                else:
                    raise Exception(f"Search API error. Status code: {response.status}")
    except Exception as e:
        raise Exception(f"Error during search: {str(e)}")

async def search_with_content(search_phrase: str, top_n: int = 5) -> dict:
    """
    Search for content and retrieve the content of the top N results
    """
    try:
        # First, get the search results
        search_results = await search_n_browse(search_phrase)
        
        # Process only the top N results
        top_results = {}
        count = 0
        
        for key, result in search_results.items():
            if key.startswith("Item_") and count < top_n:
                try:
                    # Get the URL from linkText
                    url = result.get("linkText", "")
                    if url:
                        # Fetch the content of the page
                        content = await fetch_website_content(url)
                        
                        # Add the content to the result
                        top_results[key] = {
                            "title": result.get("title", ""),
                            "snippet": result.get("snippet", ""),
                            "linkText": result.get("linkText", ""),
                            "content": content
                        }
                        count += 1
                except Exception as e:
                    # If we can't fetch the content, still include the basic result
                    top_results[key] = {
                        "title": result.get("title", ""),
                        "snippet": result.get("snippet", ""),
                        "linkText": result.get("linkText", ""),
                        "error": f"Could not fetch content: {str(e)}"
                    }
                    count += 1
        
        return top_results
    except Exception as e:
        raise Exception(f"Error during search with content: {str(e)}") 