import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .models import FactualMetrics

def scrape_website(url: str) -> FactualMetrics:
    # Set a user-agent to avoid being blocked by basic bot-protection
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    domain = urlparse(url).netloc
    
    # 1. Meta Tags
    title_tag = soup.find('title')
    meta_title = title_tag.text if title_tag else None
    
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = desc_tag['content'] if desc_tag and 'content' in desc_tag.attrs else None
    
    # 2. Text & Word Count
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator=' ')
    clean_text = ' '.join(text.split())
    word_count = len(clean_text.split())
    
    # 3. Headings
    h1_count = len(soup.find_all('h1'))
    h2_count = len(soup.find_all('h2'))
    h3_count = len(soup.find_all('h3'))
    
    # 4. Links (Internal vs External)
    links = soup.find_all('a')
    internal_links = 0
    external_links = 0
    
    for link in links:
        href = link.get('href')
        if href:
            if href.startswith('#') or href.startswith('/') or domain in href:
                internal_links += 1
            else:
                external_links += 1
                
    # 5. CTAs (Approximation: buttons + links with typical CTA classes/text)
    # This is a basic heuristic. We count buttons and <a> tags that look like buttons.
    buttons = soup.find_all('button')
    cta_count = len(buttons)

    
    # 6. Images & Alt Text
    images = soup.find_all('img')
    total_images = len(images)
    images_missing_alt = sum(1 for img in images if not img.get('alt') or img.get('alt').strip() == '')
    
    missing_alt_percentage = 0.0
    if total_images > 0:
        missing_alt_percentage = round((images_missing_alt / total_images) * 100, 2)
        
    return FactualMetrics(
        total_word_count=word_count,
        h1_count=h1_count,
        h2_count=h2_count,
        h3_count=h3_count,
        internal_links=internal_links,
        external_links=external_links,
        cta_count=cta_count,
        total_images=total_images,
        images_missing_alt=images_missing_alt,
        images_missing_alt_percentage=missing_alt_percentage,
        meta_title=meta_title,
        meta_description=meta_description,
        clean_text=clean_text
    )