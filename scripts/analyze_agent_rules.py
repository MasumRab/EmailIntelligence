#!/usr/bin/env python3
"""
Agent Rules Analyzer — Browser Automation

Automates submission of config files to agentrulegen.com/analyze
since no API exists.

Requirements:
- playwright (npm install -g playwright)
- Or: npx playwright python

Usage:
    python3 analyze_agent_rules.py .ruler/AGENTS.md
    python3 analyze_agent_rules.py .claude/hooks.yaml
    python3 analyze_agent_rules.py rulesync.jsonc
"""

import sys
import json
import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("ERROR: playwright not installed")
    print("Install: pip install playwright && playwright install chromium")
    sys.exit(1)

ANALYZE_URL = "https://agentrulegen.com/analyze"
MAX_CHARS = 10000


async def analyze_rules(file_path: str) -> dict:
    """
    Submit file content to agentrulegen.com/analyze and scrape results.
    
    Args:
        file_path: Path to config file (.ruler/AGENTS.md, hooks.yaml, etc.)
    
    Returns:
        dict with keys: redundant, essential, improvable, missing
    """
    # Read file content
    content = Path(file_path).read_text()
    
    if len(content) > MAX_CHARS:
        print(f"WARNING: Content exceeds {MAX_CHARS} chars ({len(content)}), truncating")
        content = content[:MAX_CHARS]
    
    print(f"Analyzing: {file_path} ({len(content)} chars)")
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to analyze page
            print("Navigating to agentrulegen.com/analyze...")
            await page.goto(ANALYZE_URL, wait_until="networkidle")
            
            # Wait for text area to be visible
            text_area = await page.wait_for_selector("textarea", timeout=10000)
            
            # Fill in content
            print("Submitting content...")
            await text_area.fill(content)
            
            # Click analyze button (look for button with "Analyze" text)
            analyze_btn = await page.wait_for_selector("button:has-text('Analyze')", timeout=5000)
            await analyze_btn.click()
            
            # Wait for results (look for results container)
            print("Waiting for analysis results...")
            await page.wait_for_selector("[class*='result'], [class*='analysis'], :text('redundant'), :text('essential')", timeout=60000)
            
            # Scrape results
            print("Scraping results...")
            results_text = await page.inner_text("body")
            
            # Try to find structured results
            results = {
                "file": file_path,
                "char_count": len(content),
                "raw_response": results_text,
                "redundant": [],
                "essential": [],
                "improvable": [],
                "missing": []
            }
            
            # Parse common patterns in response
            # "Redundant rules:" section
            redundant_section = await page.query_selector(":text('Redundant') ~ *")
            if redundant_section:
                results["redundant"] = (await redundant_section.inner_text()).split("\n")
            
            essential_section = await page.query_selector(":text('Essential') ~ *")
            if essential_section:
                results["essential"] = (await essential_section.inner_text()).split("\n")
            
            improvable_section = await page.query_selector(":text('Improvable') ~ *")
            if improvable_section:
                results["improvable"] = (await improvable_section.inner_text()).split("\n")
            
            return results
            
        except Exception as e:
            return {
                "file": file_path,
                "error": str(e),
                "success": False
            }
        finally:
            await browser.close()


async def batch_analyze(files: list[str]) -> list[dict]:
    """Analyze multiple config files."""
    results = []
    for file_path in files:
        result = await analyze_rules(file_path)
        results.append(result)
        print(f"Complete: {file_path}")
        # Small delay between requests to avoid rate limiting
        await asyncio.sleep(2)
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_agent_rules.py <file> [file2] [file3]")
        print("Example: python3 analyze_agent_rules.py .ruler/AGENTS.md .claude/hooks.yaml")
        sys.exit(1)
    
    files = sys.argv[1:]
    
    # Validate files exist
    for f in files:
        if not Path(f).exists():
            print(f"ERROR: File not found: {f}")
            sys.exit(1)
    
    # Run analysis
    results = asyncio.run(batch_analyze(files))
    
    # Output JSON
    print("\n=== ANALYSIS RESULTS ===")
    print(json.dumps(results, indent=2))
    
    # Save to file
    output_file = "agent_rules_analysis.json"
    Path(output_file).write_text(json.dumps(results, indent=2))
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
