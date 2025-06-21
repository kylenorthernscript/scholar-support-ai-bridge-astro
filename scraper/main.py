#!/usr/bin/env python3
"""Main entry point for the research scraper."""

import json
import argparse
from datetime import datetime
from pathlib import Path
from loguru import logger
import pandas as pd

from src.config import ScraperConfig
from src.scraper import ResearchScraper
from src.models import ResearchStudy


def setup_logging(verbose: bool = False):
    """Configure logging."""
    level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(
        "logs/scraper_{time}.log",
        rotation="1 day",
        retention="30 days",
        level=level
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level=level,
        colorize=True
    )


def save_results(studies: list[ResearchStudy], output_format: str, output_dir: Path):
    """Save scraped results to file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Filter international studies
    international_studies = [s for s in studies if s.international_score > 0]
    
    logger.info(f"Saving {len(international_studies)} international studies "
               f"out of {len(studies)} total")
    
    if output_format == "json":
        output_file = output_dir / f"international_studies_{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(
                [study.model_dump() for study in international_studies],
                f,
                ensure_ascii=False,
                indent=2,
                default=str
            )
    
    elif output_format == "csv":
        output_file = output_dir / f"international_studies_{timestamp}.csv"
        
        # Flatten studies for CSV
        rows = []
        for study in international_studies:
            row = {
                "study_id": study.study_id,
                "title": study.title,
                "title_en": study.title_en,
                "source_site": study.source_site,
                "source_url": study.source_url,
                "status": study.status.value,
                "international_type": study.international_type.value,
                "international_score": study.international_score,
                "countries": ";".join(study.countries),
                "languages": ";".join(study.languages_supported),
                "application_deadline": study.application_deadline,
                "principal_investigator": study.principal_investigator,
                "keywords": ";".join(study.keywords),
                "description": study.description[:500] + "..." if len(study.description) > 500 else study.description
            }
            rows.append(row)
        
        df = pd.DataFrame(rows)
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
    
    elif output_format == "excel":
        output_file = output_dir / f"international_studies_{timestamp}.xlsx"
        
        # Create multiple sheets
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            # Main data
            main_df = pd.DataFrame([
                {
                    "研究ID": study.study_id,
                    "タイトル": study.title,
                    "英語タイトル": study.title_en,
                    "情報源": study.source_site,
                    "URL": study.source_url,
                    "ステータス": study.status.value,
                    "国際タイプ": study.international_type.value,
                    "国際スコア": study.international_score,
                    "対象国": ";".join(study.countries),
                    "対応言語": ";".join(study.languages_supported),
                    "応募締切": study.application_deadline,
                    "研究代表者": study.principal_investigator,
                }
                for study in international_studies
            ])
            main_df.to_excel(writer, sheet_name="研究一覧", index=False)
            
            # Summary statistics
            summary_data = {
                "総研究数": len(studies),
                "国際研究数": len(international_studies),
                "国際研究率": f"{len(international_studies)/len(studies)*100:.1f}%",
                "データ取得日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            summary_df = pd.DataFrame([summary_data])
            summary_df.to_excel(writer, sheet_name="サマリー", index=False)
    
    logger.success(f"Results saved to {output_file}")
    return output_file


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="Scrape research opportunities for international participants"
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=["AMED", "JST", "JSPS", "ALL"],
        default=["AMED"],
        help="Sources to scrape"
    )
    parser.add_argument(
        "--output",
        choices=["json", "csv", "excel"],
        default="json",
        help="Output format"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./data"),
        help="Output directory"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup
    setup_logging(args.verbose)
    args.output_dir.mkdir(exist_ok=True)
    
    # Initialize
    config = ScraperConfig()
    scraper = ResearchScraper(config)
    
    # Scrape
    all_studies = []
    
    if "ALL" in args.sources:
        logger.info("Scraping all configured sources...")
        results = scraper.scrape_all_sources()
    else:
        results = []
        for source in args.sources:
            logger.info(f"Scraping {source}...")
            if source == "AMED":
                result = scraper.scrape_amed()
                results.append(result)
    
    # Process results
    for result in results:
        if result.success:
            logger.success(f"{result.source_site}: Found {result.studies_found} studies, "
                         f"{result.international_studies} international")
        else:
            logger.error(f"{result.source_site}: Failed - {result.errors}")
    
    # Fetch actual studies from scraped data
    if any([r.success for r in results]):
        logger.info("Fetching scraped studies...")
        
        all_studies = []
        for result in results:
            if result.success and result.source_site == "AMED":
                # Get studies from scraper
                amed_studies = scraper.get_stored_studies()
                all_studies.extend(amed_studies)
        
        if not all_studies:
            logger.warning("No studies found, this may indicate scraping issues")
            all_studies = []
        
        # Save results
        output_file = save_results(all_studies, args.output, args.output_dir)
        
        logger.success(f"Scraping completed! Results saved to {output_file}")
    else:
        logger.error("Some sources failed to scrape. Check logs for details.")


if __name__ == "__main__":
    main()