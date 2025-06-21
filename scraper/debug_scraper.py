#!/usr/bin/env python3
"""Debug version of scraper for testing."""

import requests
from bs4 import BeautifulSoup
from loguru import logger

def debug_amed_scraping():
    """Debug AMED scraping."""
    url = "https://www.amed.go.jp/koubo/koubo_index.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://theta-tech.co.jp/bot)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        logger.info(f"Fetching {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find all links containing '/koubo/'
        links = soup.select("a[href*='/koubo/']")
        logger.info(f"Found {len(links)} total koubo links")
        
        # Filter for recruitment links
        recruitment_links = []
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if (text and len(text) > 10 and '令和' in text and 
                not any(skip in href for skip in ['index', 'search', 'help'])):
                recruitment_links.append({
                    'title': text,
                    'href': href,
                    'full_url': f"https://www.amed.go.jp{href}" if href.startswith('/') else href
                })
        
        logger.info(f"Found {len(recruitment_links)} recruitment links")
        
        # Display first 10
        for i, link in enumerate(recruitment_links[:10]):
            print(f"{i+1}. {link['title'][:80]}...")
            print(f"   URL: {link['full_url']}")
            print()
        
        return recruitment_links
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return []

if __name__ == "__main__":
    results = debug_amed_scraping()
    print(f"\nTotal found: {len(results)} recruitment opportunities")