import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def clean_text(text):
    # Remove extra newlines and spaces
    cleaned_text = re.sub(r'\n+', '\n', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Remove wiki-specific text such as headings, links, categories, and special characters
    cleaned_text = re.sub(r'\[.*?\]', '', cleaned_text)  # Remove text within square brackets
    cleaned_text = re.sub(r'\{.*?\}', '', cleaned_text)  # Remove text within curly braces
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)  # Remove text within parentheses
    cleaned_text = re.sub(r'==.*?==', '', cleaned_text)  # Remove text within double equals
    # Remove special characters
    cleaned_text = re.sub(r'[\|•\t]', '', cleaned_text)
    return cleaned_text.strip()

def extract_website_data(url, start_time=0, level=0, max_level=3, visited_urls=None, host=None):
    if visited_urls is None:
        visited_urls = set()
    if time.time() - start_time > 40:
        return []

    print(url)

    if host is None:
        host = urlparse(url).netloc

    if level > max_level or urlparse(url).netloc != host:
        return []

    if url in visited_urls:
        return []
    else:
        visited_urls.add(url)

    try:
        response = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        data = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            base_url = urlparse(url)._replace(path='', query='', fragment='').geturl()
            current_data = {"url": url, "text": clean_text(soup.get_text().strip())}
            data.append(current_data)

            all_links = soup.find_all("a", href=True)
            for link in all_links:
                href = link.get("href")
                if href:
                    full_url = urljoin(base_url, href)
                    cleaned_url = urlparse(full_url)._replace(fragment='').geturl()
                    if cleaned_url not in visited_urls:
                        data.extend(extract_website_data(cleaned_url, start_time, level + 1, max_level, visited_urls, host))
            return data
        else:
            return []
    except requests.RequestException as e:
        print("Request to", url, "failed:", str(e))
        return []
    except Exception as e:
        print("An error occurred while processing", url, ":", str(e))
        return []