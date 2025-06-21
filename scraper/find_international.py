#!/usr/bin/env python3
"""Find international studies from AMED data."""

import requests
from bs4 import BeautifulSoup
from loguru import logger

def find_international_studies():
    """Find international studies from AMED."""
    url = "https://www.amed.go.jp/koubo/koubo_index.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://theta-tech.co.jp/bot)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    # International keywords
    international_keywords = [
        "国際共同", "外国人", "多国籍", "グローバル", "海外", "国際",
        "ASPIRE", "e-ASIA", "SICORP", "Interstellar",
        "日米", "日欧", "日中", "日韓", "日印", "日・カナダ", "日・スイス"
    ]
    
    try:
        logger.info(f"Fetching {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find all links containing '/koubo/'
        links = soup.select("a[href*='/koubo/']")
        
        international_studies = []
        total_checked = 0
        
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if (text and len(text) > 10 and '令和' in text and 
                not any(skip in href for skip in ['index', 'search', 'help'])):
                
                total_checked += 1
                
                # Check for international keywords
                is_international = False
                matched_keywords = []
                
                for keyword in international_keywords:
                    if keyword in text:
                        is_international = True
                        matched_keywords.append(keyword)
                
                if is_international:
                    international_studies.append({
                        'title': text,
                        'href': href,
                        'full_url': f"https://www.amed.go.jp{href}" if href.startswith('/') else href,
                        'keywords': matched_keywords
                    })
        
        logger.info(f"Checked {total_checked} studies")
        logger.info(f"Found {len(international_studies)} international studies")
        
        # Display international studies
        for i, study in enumerate(international_studies):
            print(f"{i+1}. {study['title'][:100]}...")
            print(f"   Keywords: {', '.join(study['keywords'])}")
            print(f"   URL: {study['full_url']}")
            print()
        
        return international_studies
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return []

if __name__ == "__main__":
    results = find_international_studies()
    print(f"\n🌍 Total international studies found: {len(results)}")
    
    if results:
        print(f"📊 International rate: {len(results)/682*100:.1f}%")
    
    # Show keyword frequency
    all_keywords = []
    for study in results:
        all_keywords.extend(study['keywords'])
    
    from collections import Counter
    keyword_counts = Counter(all_keywords)
    
    print("\n🔤 Most common international keywords:")
    for keyword, count in keyword_counts.most_common(10):
        print(f"   {keyword}: {count}")