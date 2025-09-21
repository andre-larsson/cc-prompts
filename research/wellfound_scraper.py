#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from typing import List, Dict, Optional
from scraper import WebScraper


class WellfoundScraper(WebScraper):
    """Scraper for Wellfound (formerly AngelList) startup data"""

    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://wellfound.com"
        # Add browser-like headers to avoid blocks
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        })

    def get_job_listings_by_role(self, role: str = "software-engineer", location: str = None, limit: int = 20) -> List[Dict]:
        """Get job listings for a specific role"""
        # Wellfound uses URL patterns like: /role/l/software-engineer/python
        role_slug = role.lower().replace(' ', '-')

        if location:
            location_slug = location.lower().replace(' ', '-')
            url = f"{self.base_url}/role/{location_slug}/{role_slug}"
        else:
            url = f"{self.base_url}/role/l/{role_slug}"

        try:
            response = self.session.get(url, timeout=10)

            # Check if we're being blocked
            if response.status_code == 403:
                print("Wellfound is blocking requests. This site requires browser automation.")
                return []

            if response.status_code != 200:
                print(f"Wellfound returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find job listings - Wellfound uses React, so content might be dynamic
            jobs = []

            # Look for job cards with various possible selectors
            job_selectors = [
                'div[data-test*="JobCard"]',
                'div[class*="JobCard"]',
                'div[class*="job-card"]',
                'article[class*="job"]',
                'div[class*="styles_jobListing"]',
                'div[class*="styles_job"]'
            ]

            job_cards = []
            for selector in job_selectors:
                job_cards = soup.select(selector)
                if job_cards:
                    break

            if not job_cards:
                # Try to find any data in script tags (React might render data as JSON)
                script_tags = soup.find_all('script', type='application/json')
                for script in script_tags:
                    try:
                        data = json.loads(script.string)
                        # Look for job data in the JSON
                        if isinstance(data, dict):
                            # This would need reverse engineering of their data structure
                            pass
                    except:
                        continue

                print("Could not find job listings. Site may require JavaScript.")
                return []

            for card in job_cards[:limit]:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except:
                    continue

            return jobs

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Wellfound jobs: {e}")
            return []

    def _parse_job_card(self, card) -> Optional[Dict]:
        """Parse a job card element"""
        try:
            # Try various selectors for job details
            title = card.select_one('h2, h3, [class*="title"], [class*="jobTitle"]')
            company = card.select_one('[class*="company"], [class*="startup"], h4')
            location = card.select_one('[class*="location"], [class*="city"]')
            salary = card.select_one('[class*="salary"], [class*="compensation"]')

            job = {
                'title': title.text.strip() if title else '',
                'company': company.text.strip() if company else '',
                'location': location.text.strip() if location else '',
                'salary': salary.text.strip() if salary else '',
                'url': '',
                'scraped_at': datetime.now().isoformat()
            }

            # Try to find the job link
            link = card.select_one('a[href*="/job"], a[href*="/company"]')
            if link:
                href = link.get('href', '')
                if href.startswith('/'):
                    job['url'] = self.base_url + href
                else:
                    job['url'] = href

            return job if job['title'] else None

        except Exception as e:
            return None

    def search_companies(self, query: str, limit: int = 20) -> List[Dict]:
        """Alternative: Try to get company data from their discover page"""
        # Note: Wellfound heavily relies on JavaScript and may block scrapers
        # This is a best-effort attempt

        print("Note: Wellfound requires JavaScript and actively blocks scrapers.")
        print("For production use, consider using browser automation (Selenium/Playwright)")

        # Return empty for now since the site blocks most scraping attempts
        return []


def demo_wellfound():
    """Demo Wellfound scraping"""
    print("\n" + "="*70)
    print("WELLFOUND SCRAPER DEMO")
    print("="*70)

    scraper = WellfoundScraper()

    print("\n🚀 Attempting to fetch software engineer jobs...")
    print("-" * 40)
    jobs = scraper.get_job_listings_by_role("software-engineer", limit=5)

    if jobs:
        for job in jobs:
            print(f"\n{job['title']} at {job['company']}")
            print(f"  Location: {job['location']}")
            print(f"  Salary: {job['salary']}")
    else:
        print("No jobs found. Wellfound likely requires browser automation.")

    print("\n" + "="*70)
    print("NOTE: Wellfound (formerly AngelList) has strong anti-scraping measures.")
    print("They use Cloudflare protection and require JavaScript execution.")
    print("For reliable access, consider:")
    print("1. Using browser automation tools (Selenium, Playwright)")
    print("2. Looking for an official API if available")
    print("3. Using alternative data sources")
    print("="*70)


if __name__ == "__main__":
    demo_wellfound()