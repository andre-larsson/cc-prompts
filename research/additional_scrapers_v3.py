#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from typing import List, Dict, Optional
from scraper import WebScraper
import re


class KaggleScraper(WebScraper):
    """Scraper for Kaggle datasets, competitions, and notebooks"""

    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://www.kaggle.com"
        self.api_url = "https://www.kaggle.com/api/v1"

    def get_trending_datasets(self, limit: int = 20) -> List[Dict]:
        """Get trending datasets"""
        url = f"{self.base_url}/datasets"
        params = {
            'sort': 'hottest',
            'page': 1,
            'pageSize': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"Kaggle returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for dataset cards in the page
            datasets = []

            # Try to find JSON data in script tags
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'Kaggle.State.push' in script.string:
                    # Extract JSON data from Kaggle state
                    match = re.search(r'Kaggle\.State\.push\((.*?)\);', script.string, re.DOTALL)
                    if match:
                        try:
                            data = json.loads(match.group(1))
                            if 'datasetListItems' in str(data):
                                # Parse dataset items from the state
                                pass
                        except:
                            continue

            # Fallback to HTML parsing
            dataset_cards = soup.select('div[data-testid*="dataset-card"], li[role="listitem"]')

            for card in dataset_cards[:limit]:
                try:
                    title_elem = card.select_one('h6, div[title]')
                    title = title_elem.text.strip() if title_elem else ''

                    author_elem = card.select_one('a[href*="/datasets/"]')
                    author = ''
                    dataset_url = ''
                    if author_elem:
                        href = author_elem.get('href', '')
                        if href:
                            parts = href.split('/')
                            if len(parts) >= 3:
                                author = parts[2]
                            dataset_url = self.base_url + href

                    downloads_elem = card.select_one('span:contains("downloads"), div:contains("downloads")')
                    downloads = 0
                    if downloads_elem:
                        match = re.search(r'([\d,]+)', downloads_elem.text)
                        if match:
                            downloads = int(match.group(1).replace(',', ''))

                    datasets.append({
                        'title': title,
                        'author': author,
                        'url': dataset_url,
                        'downloads': downloads,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return datasets

        except Exception as e:
            print(f"Error fetching Kaggle datasets: {e}")
            return []

    def get_competitions(self, limit: int = 20) -> List[Dict]:
        """Get active competitions"""
        url = f"{self.base_url}/competitions"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"Kaggle returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            competitions = []
            comp_cards = soup.select('div.competition-tile, a[href*="/competitions/"]')

            for card in comp_cards[:limit]:
                try:
                    title_elem = card.select_one('h6, .competition-tile__title')
                    title = title_elem.text.strip() if title_elem else ''

                    prize_elem = card.select_one('.competition-tile__prize, span:contains("$")')
                    prize = prize_elem.text.strip() if prize_elem else ''

                    teams_elem = card.select_one('span:contains("teams"), div:contains("teams")')
                    teams = 0
                    if teams_elem:
                        match = re.search(r'([\d,]+)', teams_elem.text)
                        if match:
                            teams = int(match.group(1).replace(',', ''))

                    href = card.get('href', '')
                    if not href and card.name != 'a':
                        link_elem = card.select_one('a[href*="/competitions/"]')
                        if link_elem:
                            href = link_elem.get('href', '')

                    comp_url = self.base_url + href if href else ''

                    competitions.append({
                        'title': title,
                        'prize': prize,
                        'teams': teams,
                        'url': comp_url,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return competitions

        except Exception as e:
            print(f"Error fetching Kaggle competitions: {e}")
            return []


class IndieHackersScraper(WebScraper):
    """Scraper for Indie Hackers posts and discussions"""

    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://www.indiehackers.com"

    def get_trending_posts(self, limit: int = 20) -> List[Dict]:
        """Get trending posts from Indie Hackers"""
        url = f"{self.base_url}/posts"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"Indie Hackers returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            posts = []

            # Look for post items
            post_items = soup.select('article, div[class*="post"], div[class*="feed-item"]')

            for item in post_items[:limit]:
                try:
                    title_elem = item.select_one('h2, h3, a[class*="title"]')
                    title = title_elem.text.strip() if title_elem else ''

                    author_elem = item.select_one('a[href*="/user/"], span[class*="author"]')
                    author = author_elem.text.strip() if author_elem else ''

                    upvotes_elem = item.select_one('button[class*="upvote"], span[class*="vote"]')
                    upvotes = 0
                    if upvotes_elem:
                        match = re.search(r'(\d+)', upvotes_elem.text)
                        if match:
                            upvotes = int(match.group(1))

                    comments_elem = item.select_one('a[href*="#comments"], span:contains("comment")')
                    comments = 0
                    if comments_elem:
                        match = re.search(r'(\d+)', comments_elem.text)
                        if match:
                            comments = int(match.group(1))

                    link_elem = item.select_one('a[href*="/post/"]')
                    post_url = ''
                    if link_elem:
                        href = link_elem.get('href', '')
                        post_url = self.base_url + href if href.startswith('/') else href

                    posts.append({
                        'title': title,
                        'author': author,
                        'upvotes': upvotes,
                        'comments': comments,
                        'url': post_url,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return posts

        except Exception as e:
            print(f"Error fetching Indie Hackers posts: {e}")
            return []

    def get_groups_discussions(self, group: str = "startup", limit: int = 20) -> List[Dict]:
        """Get discussions from specific groups"""
        url = f"{self.base_url}/group/{group}"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')
            discussions = []

            # Parse group discussions
            discussion_items = soup.select('div[class*="discussion"], article')

            for item in discussion_items[:limit]:
                try:
                    title_elem = item.select_one('h3, a[class*="title"]')
                    title = title_elem.text.strip() if title_elem else ''

                    discussions.append({
                        'title': title,
                        'group': group,
                        'scraped_at': datetime.now().isoformat()
                    })
                except:
                    continue

            return discussions

        except Exception as e:
            print(f"Error fetching group discussions: {e}")
            return []


class TheVergeScraper(WebScraper):
    """Scraper for The Verge tech news"""

    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://www.theverge.com"

    def get_latest_articles(self, category: str = "tech", limit: int = 20) -> List[Dict]:
        """Get latest articles from The Verge"""
        url = f"{self.base_url}/{category}"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"The Verge returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            articles = []

            # Find article elements
            article_elems = soup.select('article, div[class*="story"], div[class*="entry"]')

            for article in article_elems[:limit]:
                try:
                    title_elem = article.select_one('h2, h3, a[class*="title"]')
                    title = title_elem.text.strip() if title_elem else ''

                    author_elem = article.select_one('a[href*="/authors/"], span[class*="author"]')
                    author = author_elem.text.strip() if author_elem else ''

                    time_elem = article.select_one('time, span[class*="time"]')
                    published_at = ''
                    if time_elem:
                        published_at = time_elem.get('datetime', time_elem.text.strip())

                    link_elem = article.select_one('a[href*="/2024/"], a[href*="/2025/"]')
                    article_url = ''
                    if link_elem:
                        href = link_elem.get('href', '')
                        article_url = self.base_url + href if href.startswith('/') else href

                    excerpt_elem = article.select_one('p, div[class*="excerpt"]')
                    excerpt = excerpt_elem.text.strip()[:200] if excerpt_elem else ''

                    articles.append({
                        'title': title,
                        'author': author,
                        'excerpt': excerpt,
                        'url': article_url,
                        'published_at': published_at,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return articles

        except Exception as e:
            print(f"Error fetching The Verge articles: {e}")
            return []


class ArsTechnicaScraper(WebScraper):
    """Scraper for Ars Technica technical articles"""

    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://arstechnica.com"

    def get_latest_articles(self, category: str = "information-technology", limit: int = 20) -> List[Dict]:
        """Get latest technical articles"""
        url = f"{self.base_url}/{category}/"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"Ars Technica returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            articles = []

            # Find article listings
            article_elems = soup.select('article, li[class*="article"], div[class*="listing"]')

            for article in article_elems[:limit]:
                try:
                    title_elem = article.select_one('h2, h3, a[class*="title"]')
                    title = title_elem.text.strip() if title_elem else ''

                    author_elem = article.select_one('a[href*="/author/"], p[class*="byline"]')
                    author = author_elem.text.strip() if author_elem else ''
                    author = author.replace('- ', '').replace(',', '').strip()

                    time_elem = article.select_one('time')
                    published_at = ''
                    if time_elem:
                        published_at = time_elem.get('datetime', '')

                    excerpt_elem = article.select_one('p[class*="excerpt"], p:not([class*="byline"])')
                    excerpt = excerpt_elem.text.strip()[:200] if excerpt_elem else ''

                    link_elem = article.select_one('a[href*="arstechnica.com"]')
                    article_url = ''
                    if link_elem:
                        article_url = link_elem.get('href', '')

                    comment_elem = article.select_one('a[class*="comment"], span[class*="comment"]')
                    comments = 0
                    if comment_elem:
                        match = re.search(r'(\d+)', comment_elem.text)
                        if match:
                            comments = int(match.group(1))

                    articles.append({
                        'title': title,
                        'author': author,
                        'excerpt': excerpt,
                        'url': article_url,
                        'comments': comments,
                        'published_at': published_at,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return articles

        except Exception as e:
            print(f"Error fetching Ars Technica articles: {e}")
            return []


class NPMScraper(WebScraper):
    """Scraper for npm package trends"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://www.npmjs.com"
        self.api_url = "https://registry.npmjs.org"
        self.search_api = "https://api.npms.io/v2"

    def search_packages(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for packages on npm using npms.io API"""
        url = f"{self.search_api}/search"
        params = {
            'q': query,
            'size': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"npm search returned status {response.status_code}")
                return []

            data = response.json()
            packages = []

            for result in data.get('results', []):
                pkg = result.get('package', {})
                score = result.get('score', {})

                packages.append({
                    'name': pkg.get('name'),
                    'version': pkg.get('version'),
                    'description': pkg.get('description'),
                    'keywords': pkg.get('keywords', []),
                    'author': pkg.get('author', {}).get('name') if isinstance(pkg.get('author'), dict) else pkg.get('author'),
                    'publisher': pkg.get('publisher', {}).get('username') if pkg.get('publisher') else '',
                    'date': pkg.get('date'),
                    'links': pkg.get('links', {}),
                    'score_final': score.get('final'),
                    'score_quality': score.get('detail', {}).get('quality'),
                    'score_popularity': score.get('detail', {}).get('popularity'),
                    'score_maintenance': score.get('detail', {}).get('maintenance'),
                    'url': f"{self.base_url}/package/{pkg.get('name')}",
                    'scraped_at': datetime.now().isoformat()
                })

            return packages

        except Exception as e:
            print(f"Error searching npm: {e}")
            return []

    def get_package_info(self, package_name: str) -> Optional[Dict]:
        """Get detailed info for a specific package"""
        url = f"{self.api_url}/{package_name}"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()
            latest = data.get('dist-tags', {}).get('latest', '')
            latest_info = data.get('versions', {}).get(latest, {})

            return {
                'name': data.get('name'),
                'description': data.get('description'),
                'latest_version': latest,
                'homepage': data.get('homepage'),
                'repository': data.get('repository'),
                'keywords': data.get('keywords', []),
                'author': data.get('author'),
                'license': data.get('license'),
                'dependencies': latest_info.get('dependencies', {}),
                'devDependencies': latest_info.get('devDependencies', {}),
                'created': data.get('time', {}).get('created'),
                'modified': data.get('time', {}).get('modified'),
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error fetching package info: {e}")
            return None

    def get_downloads_stats(self, package_name: str, period: str = 'last-week') -> Optional[Dict]:
        """Get download statistics for a package
        period: last-day, last-week, last-month, last-year
        """
        url = f"https://api.npmjs.org/downloads/point/{period}/{package_name}"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()

            return {
                'package': data.get('package'),
                'downloads': data.get('downloads'),
                'period': period,
                'start': data.get('start'),
                'end': data.get('end'),
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error fetching download stats: {e}")
            return None


class PyPIScraper(WebScraper):
    """Scraper for PyPI package trends"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://pypi.org"
        self.api_url = "https://pypi.org/pypi"

    def get_trending_packages(self, limit: int = 20) -> List[Dict]:
        """Get trending/recently updated packages"""
        # PyPI RSS feed for newest packages
        url = f"{self.base_url}/rss/packages.xml"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"PyPI RSS returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'xml')

            packages = []
            items = soup.find_all('item')

            for item in items[:limit]:
                try:
                    title = item.find('title').text if item.find('title') else ''
                    description = item.find('description').text if item.find('description') else ''
                    link = item.find('link').text if item.find('link') else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') else ''

                    # Extract package name and version from title
                    match = re.match(r'(.+?)\s+([\d.]+)', title)
                    if match:
                        package_name = match.group(1)
                        version = match.group(2)
                    else:
                        package_name = title
                        version = ''

                    packages.append({
                        'name': package_name,
                        'version': version,
                        'description': description,
                        'url': link,
                        'published_at': pub_date,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return packages

        except Exception as e:
            print(f"Error fetching PyPI packages: {e}")
            return []

    def search_packages(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for packages on PyPI"""
        # Use PyPI's search endpoint
        url = f"{self.base_url}/search/"
        params = {'q': query}

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code != 200:
                print(f"PyPI search returned status {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            packages = []
            results = soup.select('a[class*="package-snippet"]')

            for result in results[:limit]:
                try:
                    name_elem = result.select_one('h3 span[class*="package-snippet__name"]')
                    name = name_elem.text.strip() if name_elem else ''

                    version_elem = result.select_one('span[class*="package-snippet__version"]')
                    version = version_elem.text.strip() if version_elem else ''

                    desc_elem = result.select_one('p[class*="package-snippet__description"]')
                    description = desc_elem.text.strip() if desc_elem else ''

                    href = result.get('href', '')
                    package_url = self.base_url + href if href else ''

                    packages.append({
                        'name': name,
                        'version': version,
                        'description': description,
                        'url': package_url,
                        'scraped_at': datetime.now().isoformat()
                    })
                except Exception as e:
                    continue

            return packages

        except Exception as e:
            print(f"Error searching PyPI: {e}")
            return []

    def get_package_stats(self, package_name: str) -> Optional[Dict]:
        """Get detailed stats for a specific package"""
        url = f"{self.api_url}/{package_name}/json"

        try:
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                return None

            data = response.json()
            info = data.get('info', {})

            return {
                'name': info.get('name'),
                'version': info.get('version'),
                'summary': info.get('summary'),
                'author': info.get('author'),
                'license': info.get('license'),
                'home_page': info.get('home_page'),
                'keywords': info.get('keywords'),
                'requires_python': info.get('requires_python'),
                'downloads': data.get('downloads', {}),
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error fetching package stats: {e}")
            return None


def demo_scrapers_v3():
    """Demo all v3 scrapers"""
    print("\n" + "="*70)
    print("ADDITIONAL SCRAPERS V3 DEMO")
    print("="*70)

    # Test Kaggle
    print("\n📊 Testing Kaggle Scraper...")
    print("-" * 40)
    kaggle = KaggleScraper()
    datasets = kaggle.get_trending_datasets(limit=3)
    if datasets:
        for ds in datasets:
            print(f"Dataset: {ds['title']}")
            print(f"  Author: {ds['author']}")
            print(f"  Downloads: {ds['downloads']:,}" if ds['downloads'] else "  Downloads: N/A")
    else:
        print("No datasets found (may require authentication)")

    competitions = kaggle.get_competitions(limit=3)
    if competitions:
        print("\nCompetitions:")
        for comp in competitions:
            print(f"- {comp['title']} ({comp['prize']})")

    # Test Indie Hackers
    print("\n💡 Testing Indie Hackers Scraper...")
    print("-" * 40)
    ih = IndieHackersScraper()
    posts = ih.get_trending_posts(limit=3)
    if posts:
        for post in posts:
            print(f"Post: {post['title']}")
            print(f"  Author: {post['author']}, Upvotes: {post['upvotes']}, Comments: {post['comments']}")
    else:
        print("No posts found")

    # Test The Verge
    print("\n📰 Testing The Verge Scraper...")
    print("-" * 40)
    verge = TheVergeScraper()
    articles = verge.get_latest_articles(limit=3)
    if articles:
        for article in articles:
            print(f"Article: {article['title']}")
            print(f"  Author: {article['author']}")
            print(f"  Published: {article['published_at']}")
    else:
        print("No articles found")

    # Test Ars Technica
    print("\n🔬 Testing Ars Technica Scraper...")
    print("-" * 40)
    ars = ArsTechnicaScraper()
    articles = ars.get_latest_articles(limit=3)
    if articles:
        for article in articles:
            print(f"Article: {article['title']}")
            print(f"  Author: {article['author']}")
            print(f"  Comments: {article['comments']}")
    else:
        print("No articles found")

    # Test PyPI
    print("\n🐍 Testing PyPI Scraper...")
    print("-" * 40)
    pypi = PyPIScraper()
    packages = pypi.get_trending_packages(limit=3)
    if packages:
        for pkg in packages:
            print(f"Package: {pkg['name']} v{pkg['version']}")
            print(f"  {pkg['description'][:100]}...")
    else:
        print("No packages found")

    # Test npm
    print("\n📦 Testing npm Scraper...")
    print("-" * 40)
    npm = NPMScraper()
    packages = npm.search_packages("react", limit=3)
    if packages:
        for pkg in packages:
            print(f"Package: {pkg['name']} v{pkg['version']}")
            print(f"  Score: {pkg['score_final']:.2f}" if pkg['score_final'] else "  Score: N/A")
            print(f"  {pkg['description'][:100]}..." if pkg['description'] else "")
    else:
        print("No packages found")

    print("\n" + "="*70)
    print("V3 SCRAPERS TEST COMPLETE")
    print("="*70)


if __name__ == "__main__":
    demo_scrapers_v3()