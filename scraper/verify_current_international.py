#!/usr/bin/env python3
"""Verify current international opportunities using AMED search."""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import datetime
import re

def search_amed_current():
    """Search AMED for current opportunities."""
    
    # Search for all current opportunities
    base_url = "https://www.amed.go.jp/search.php"
    
    # Parameters for current opportunities only
    params = {
        'keyword': '',
        'search': 'search',
        'order_by': '',
        'stage[]': '現在公募中'
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://theta-tech.co.jp/bot)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    # International keywords
    intl_keywords = [
        "国際", "海外", "グローバル", "外国", "多国籍",
        "ASPIRE", "e-ASIA", "SICORP", "Interstellar", "SATREPS",
        "日米", "日欧", "日中", "日・", "日本・",
        "国際共同", "国際科学", "国際協力",
        "international", "global", "overseas"
    ]
    
    try:
        # Get all current opportunities
        print("🔍 現在公募中の案件を検索中...")
        url = f"{base_url}?{urlencode(params, doseq=True)}"
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find total count
        count_text = soup.find(text=re.compile(r'検索結果.*件中'))
        total_count = 0
        if count_text:
            match = re.search(r'(\d+)件中', str(count_text))
            if match:
                total_count = int(match.group(1))
        
        print(f"📊 現在公募中の総件数: {total_count}件")
        
        # Now search for international opportunities
        print("\n🌍 国際関連の公募を検索中...")
        
        international_results = {}
        
        for keyword in ["国際", "海外", "グローバル", "ASPIRE", "SICORP", "e-ASIA", "Interstellar"]:
            params['keyword'] = keyword
            url = f"{base_url}?{urlencode(params, doseq=True)}"
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            
            # Find count
            count_text = soup.find(text=re.compile(r'検索結果.*件中'))
            if count_text:
                match = re.search(r'(\d+)件中', str(count_text))
                if match:
                    count = int(match.group(1))
                    if count > 0:
                        international_results[keyword] = count
                        print(f"  '{keyword}': {count}件")
        
        # Get unique international opportunities
        # (Note: This is an approximation as some may overlap)
        total_international = max(international_results.values()) if international_results else 0
        
        print(f"\n📈 分析結果:")
        print(f"  現在公募中: {total_count}件")
        print(f"  国際関連（推定）: {total_international}件")
        print(f"  国際研究率: {total_international/total_count*100:.1f}%" if total_count > 0 else "N/A")
        
        # Get details of international opportunities
        if total_international > 0:
            print(f"\n📋 国際関連公募の詳細:")
            
            # Search for "国際" to get the main international calls
            params['keyword'] = '国際'
            url = f"{base_url}?{urlencode(params, doseq=True)}"
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            
            # Find result items
            results = soup.find_all('div', class_='searchResultItem') or soup.find_all('li', class_='result')
            
            if not results:
                # Try alternative parsing
                links = soup.find_all('a', href=re.compile(r'/koubo/'))
                for i, link in enumerate(links[:10], 1):
                    title = link.get_text(strip=True)
                    if len(title) > 10:
                        print(f"\n{i}. {title[:100]}...")
                        
                        # Check which international keywords it contains
                        found_keywords = [kw for kw in intl_keywords if kw in title]
                        if found_keywords:
                            print(f"   キーワード: {', '.join(found_keywords[:5])}")
        
        return {
            'total_current': total_count,
            'international_estimated': total_international,
            'international_keywords': international_results
        }
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def check_specific_international():
    """Check specific international programs."""
    programs = {
        'ASPIRE': '先端国際共同研究推進プログラム',
        'SICORP': '戦略的国際共同研究プログラム',
        'e-ASIA': 'e-ASIA共同研究プログラム',
        'Interstellar': 'Interstellar Initiative',
        'SATREPS': '地球規模課題対応国際科学技術協力プログラム'
    }
    
    print("\n🔎 主要国際プログラムの確認:")
    
    for eng_name, jp_name in programs.items():
        print(f"\n{eng_name} ({jp_name}):")
        # This would require checking each program's status
        print(f"  → 検索システムで確認が必要")

if __name__ == "__main__":
    print("AMED現在公募中の国際研究機会 検証ツール")
    print("=" * 50)
    
    results = search_amed_current()
    
    if results:
        print("\n" + "=" * 50)
        print("✅ 検証完了")
        print(f"\n最終結果:")
        print(f"  現在公募中の総数: {results['total_current']}件")
        print(f"  うち国際関連: {results['international_estimated']}件以上")
    
    check_specific_international()