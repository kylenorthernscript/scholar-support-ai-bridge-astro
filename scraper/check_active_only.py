#!/usr/bin/env python3
"""Check only currently active recruitments."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def check_active_recruitments():
    """Check only active recruitments with detailed analysis."""
    url = "https://www.amed.go.jp/koubo/koubo_index.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://theta-tech.co.jp/bot)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # Find main content area
        content = soup.get_text()
        
        # Find the "終了した公募" marker position
        ended_marker = content.find("終了した公募")
        if ended_marker == -1:
            print("警告: '終了した公募'セクションが見つかりません")
            ended_marker = len(content)  # Use full content
        
        # Extract only the active section
        active_section_text = content[:ended_marker]
        
        # Create a new soup with only active section
        active_soup = BeautifulSoup(response.text, "lxml")
        
        # Find all links
        all_links = active_soup.select("a[href*='/koubo/']")
        
        active_recruitments = []
        
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Skip if not a recruitment link
            if not text or len(text) < 10 or not '令和' in text:
                continue
            
            # Skip if it's an index or search page
            if any(skip in href for skip in ['index', 'search', 'help']):
                continue
            
            # Check if this link appears in active section
            if text in active_section_text:
                # Extract deadline
                parent_text = ""
                if link.parent:
                    parent_text = link.parent.get_text()
                
                # Look for deadline in various formats
                deadline = None
                deadline_patterns = [
                    r"締切[：:]\s*令和(\d+)年(\d{1,2})月(\d{1,2})日",
                    r"公募締切[：:]\s*令和(\d+)年(\d{1,2})月(\d{1,2})日",
                    r"応募締切[：:]\s*令和(\d+)年(\d{1,2})月(\d{1,2})日",
                    r"令和(\d+)年(\d{1,2})月(\d{1,2})日.*締切",
                ]
                
                for pattern in deadline_patterns:
                    match = re.search(pattern, parent_text)
                    if match:
                        year = 2018 + int(match.group(1))
                        month = int(match.group(2))
                        day = int(match.group(3))
                        deadline = f"{year}年{month}月{day}日"
                        break
                
                # Check if international
                intl_keywords = ["国際", "海外", "グローバル", "ASPIRE", "SICORP", 
                               "e-ASIA", "Interstellar", "日米", "日・", "外国"]
                is_international = any(kw in text for kw in intl_keywords)
                
                active_recruitments.append({
                    'title': text,
                    'url': f"https://www.amed.go.jp{href}" if href.startswith('/') else href,
                    'deadline': deadline,
                    'is_international': is_international,
                    'keywords': [kw for kw in intl_keywords if kw in text]
                })
        
        # Print results
        print("🔍 AMED現在募集中の公募（詳細分析）")
        print("=" * 70)
        print(f"📊 現在募集中の総数: {len(active_recruitments)}件")
        
        intl_count = sum(1 for r in active_recruitments if r['is_international'])
        print(f"🌍 国際研究: {intl_count}件 ({intl_count/len(active_recruitments)*100:.1f}%)" if active_recruitments else "0件")
        
        print("\n📋 募集中の全公募リスト:")
        for i, recruit in enumerate(active_recruitments, 1):
            print(f"\n{i}. {recruit['title'][:80]}...")
            print(f"   締切: {recruit['deadline'] or '不明'}")
            print(f"   国際: {'✓' if recruit['is_international'] else '✗'}")
            if recruit['is_international']:
                print(f"   キーワード: {', '.join(recruit['keywords'])}")
            print(f"   URL: {recruit['url']}")
        
        print("\n🌍 国際研究のみ:")
        intl_recruits = [r for r in active_recruitments if r['is_international']]
        for i, recruit in enumerate(intl_recruits, 1):
            print(f"\n{i}. {recruit['title'][:100]}...")
            print(f"   締切: {recruit['deadline'] or '不明'}")
            print(f"   キーワード: {', '.join(recruit['keywords'])}")
        
        return active_recruitments
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    check_active_recruitments()