#!/usr/bin/env python3
"""Verify the actual counts of AMED recruitment data."""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from collections import defaultdict

def verify_amed_counts():
    """Verify actual counts and status of AMED recruitments."""
    url = "https://www.amed.go.jp/koubo/koubo_index.html"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://theta-tech.co.jp/bot)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "lxml")
        full_text = soup.get_text()
        
        # Analysis results
        results = {
            'total_links': 0,
            'active_recruitments': 0,
            'ended_recruitments': 0,
            'international_active': 0,
            'international_ended': 0,
            'international_keywords_found': defaultdict(int),
            'date_analysis': {
                'future_deadlines': 0,
                'past_deadlines': 0,
                'no_deadline': 0
            }
        }
        
        # International keywords
        intl_keywords = [
            "国際共同", "外国人", "多国籍", "グローバル", "海外", "国際",
            "ASPIRE", "e-ASIA", "SICORP", "Interstellar",
            "日米", "日欧", "日中", "日韓", "日印", "日・カナダ", "日・スイス",
            "日・英国", "日・フランス", "日・ドイツ", "日・オーストラリア"
        ]
        
        # Find all recruitment links
        all_links = soup.select("a[href*='/koubo/']")
        
        # Separate sections
        sections = {
            'active': [],
            'ended': []
        }
        
        # Try to identify sections
        current_section = 'unknown'
        
        # Look for section markers
        if "終了した公募" in full_text:
            # Find position of "終了した公募"
            ended_marker = full_text.find("終了した公募")
            
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if not text or len(text) < 10 or not '令和' in text:
                    continue
                
                # Get position in page
                link_text_pos = full_text.find(text)
                
                if link_text_pos > 0:
                    if link_text_pos < ended_marker:
                        sections['active'].append((link, text))
                    else:
                        sections['ended'].append((link, text))
        else:
            # If no clear section markers, check dates
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                if not text or len(text) < 10 or not '令和' in text:
                    continue
                
                # Check if deadline is mentioned
                deadline_match = re.search(r"令和(\d+)年(\d{1,2})月(\d{1,2})日", text)
                if deadline_match:
                    year = 2018 + int(deadline_match.group(1))
                    month = int(deadline_match.group(2))
                    day = int(deadline_match.group(3))
                    
                    try:
                        deadline_date = datetime(year, month, day)
                        if deadline_date > datetime.now():
                            sections['active'].append((link, text))
                            results['date_analysis']['future_deadlines'] += 1
                        else:
                            sections['ended'].append((link, text))
                            results['date_analysis']['past_deadlines'] += 1
                    except:
                        results['date_analysis']['no_deadline'] += 1
                else:
                    results['date_analysis']['no_deadline'] += 1
        
        # Count results
        results['active_recruitments'] = len(sections['active'])
        results['ended_recruitments'] = len(sections['ended'])
        results['total_links'] = len(sections['active']) + len(sections['ended'])
        
        # Check international keywords
        for section_name, links in sections.items():
            for link, text in links:
                for keyword in intl_keywords:
                    if keyword in text:
                        results['international_keywords_found'][keyword] += 1
                        if section_name == 'active':
                            results['international_active'] += 1
                        else:
                            results['international_ended'] += 1
                        break  # Count each link only once
        
        # Print detailed results
        print("🔍 AMED公募情報検証結果")
        print("=" * 50)
        print(f"📊 総リンク数: {results['total_links']}")
        print(f"✅ 現在募集中: {results['active_recruitments']}")
        print(f"❌ 募集終了: {results['ended_recruitments']}")
        print()
        
        print("🌍 国際研究関連")
        print(f"現在募集中の国際研究: {results['international_active']}")
        print(f"募集終了の国際研究: {results['international_ended']}")
        print(f"国際研究率（全体）: {(results['international_active'] + results['international_ended']) / results['total_links'] * 100:.1f}%")
        print(f"国際研究率（募集中）: {results['international_active'] / results['active_recruitments'] * 100:.1f}%" if results['active_recruitments'] > 0 else "N/A")
        print()
        
        print("📅 締切日分析")
        print(f"将来の締切: {results['date_analysis']['future_deadlines']}")
        print(f"過去の締切: {results['date_analysis']['past_deadlines']}")
        print(f"締切不明: {results['date_analysis']['no_deadline']}")
        print()
        
        print("🔤 検出された国際キーワード（上位）")
        sorted_keywords = sorted(results['international_keywords_found'].items(), 
                               key=lambda x: x[1], reverse=True)[:10]
        for keyword, count in sorted_keywords:
            print(f"  {keyword}: {count}回")
        
        # Show sample active international studies
        print("\n📌 現在募集中の国際研究（サンプル）")
        count = 0
        for link, text in sections['active']:
            for keyword in intl_keywords:
                if keyword in text:
                    print(f"{count+1}. {text[:80]}...")
                    count += 1
                    break
            if count >= 5:
                break
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    verify_amed_counts()