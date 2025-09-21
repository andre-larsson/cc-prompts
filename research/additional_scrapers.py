#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from typing import List, Dict, Optional
import re
import xml.etree.ElementTree as ET
from urllib.parse import quote
from scraper import WebScraper


class DevToScraper(WebScraper):
    """Scraper for Dev.to articles using their public API"""

    def __init__(self):
        super().__init__(delay=0.5)
        self.base_url = "https://dev.to"
        self.api_url = "https://dev.to/api"

    def get_articles(self, page: int = 1, per_page: int = 30, tag: str = None, state: str = "rising") -> List[Dict]:
        """Get articles from Dev.to
        state can be: fresh, rising, all
        """
        url = f"{self.api_url}/articles"
        params = {
            'page': page,
            'per_page': min(per_page, 100),  # API max is 100
            'state': state
        }

        if tag:
            params['tag'] = tag

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json()

            result = []
            for article in articles:
                result.append({
                    'id': article.get('id'),
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'canonical_url': article.get('canonical_url'),
                    'author': article.get('user', {}).get('username'),
                    'author_name': article.get('user', {}).get('name'),
                    'tags': article.get('tag_list', []),
                    'published_at': article.get('published_at'),
                    'created_at': article.get('created_at'),
                    'reading_time_minutes': article.get('reading_time_minutes'),
                    'positive_reactions': article.get('positive_reactions_count', 0),
                    'comments_count': article.get('comments_count', 0),
                    'scraped_at': datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"Error fetching Dev.to articles: {e}")
            return []

    def search_articles(self, query: str, page: int = 1, per_page: int = 30) -> List[Dict]:
        """Search for articles on Dev.to"""
        url = f"{self.api_url}/articles"
        params = {
            'page': page,
            'per_page': min(per_page, 100),
            'tag': query  # Dev.to search is mainly tag-based via API
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            articles = response.json()

            result = []
            for article in articles:
                result.append({
                    'id': article.get('id'),
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'author': article.get('user', {}).get('username'),
                    'tags': article.get('tag_list', []),
                    'published_at': article.get('published_at'),
                    'positive_reactions': article.get('positive_reactions_count', 0),
                    'comments_count': article.get('comments_count', 0),
                    'reading_time_minutes': article.get('reading_time_minutes'),
                    'scraped_at': datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"Error searching Dev.to: {e}")
            return []

    def get_article_with_content(self, article_id: int) -> Dict:
        """Get full article content"""
        url = f"{self.api_url}/articles/{article_id}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            article = response.json()

            return {
                'id': article.get('id'),
                'title': article.get('title'),
                'description': article.get('description'),
                'url': article.get('url'),
                'author': article.get('user', {}).get('username'),
                'tags': article.get('tag_list', []),
                'published_at': article.get('published_at'),
                'body_markdown': article.get('body_markdown', '')[:5000],  # Limit size
                'body_html': article.get('body_html', '')[:5000],
                'positive_reactions': article.get('positive_reactions_count', 0),
                'comments_count': article.get('comments_count', 0),
                'reading_time_minutes': article.get('reading_time_minutes'),
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error fetching Dev.to article: {e}")
            return {}


class ArXivScraper(WebScraper):
    """Scraper for ArXiv preprint papers"""

    def __init__(self):
        super().__init__(delay=3.0)  # ArXiv requests 3 second delay
        self.base_url = "http://export.arxiv.org/api/query"

    def search_papers(self, query: str, max_results: int = 20, sort_by: str = "relevance", sort_order: str = "descending") -> List[Dict]:
        """Search ArXiv papers
        sort_by: relevance, lastUpdatedDate, submittedDate
        sort_order: ascending, descending
        """
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': sort_by,
            'sortOrder': sort_order
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)

            # Define namespaces
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }

            papers = []
            for entry in root.findall('atom:entry', ns):
                paper = {
                    'id': entry.find('atom:id', ns).text.replace('http://arxiv.org/abs/', ''),
                    'title': entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                    'summary': entry.find('atom:summary', ns).text.strip()[:500],
                    'authors': [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
                    'published': entry.find('atom:published', ns).text,
                    'updated': entry.find('atom:updated', ns).text,
                    'categories': [cat.get('term') for cat in entry.findall('atom:category', ns)],
                    'pdf_url': None,
                    'url': None,
                    'scraped_at': datetime.now().isoformat()
                }

                # Get links
                for link in entry.findall('atom:link', ns):
                    if link.get('type') == 'application/pdf':
                        paper['pdf_url'] = link.get('href')
                    elif link.get('type') == 'text/html':
                        paper['url'] = link.get('href')

                papers.append(paper)

            return papers

        except Exception as e:
            print(f"Error searching ArXiv: {e}")
            return []

    def get_category_papers(self, category: str = "cs.AI", max_results: int = 20) -> List[Dict]:
        """Get recent papers from specific category
        Common categories: cs.AI, cs.LG, cs.CL, cs.CV
        """
        params = {
            'search_query': f'cat:{category}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }

        try:
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            papers = []
            for entry in root.findall('atom:entry', ns):
                paper = {
                    'id': entry.find('atom:id', ns).text.replace('http://arxiv.org/abs/', ''),
                    'title': entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                    'summary': entry.find('atom:summary', ns).text.strip()[:500],
                    'authors': [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
                    'published': entry.find('atom:published', ns).text,
                    'updated': entry.find('atom:updated', ns).text,
                    'categories': [cat.get('term') for cat in entry.findall('atom:category', ns)],
                    'scraped_at': datetime.now().isoformat()
                }

                for link in entry.findall('atom:link', ns):
                    if link.get('type') == 'application/pdf':
                        paper['pdf_url'] = link.get('href')
                    elif link.get('type') == 'text/html':
                        paper['url'] = link.get('href')

                papers.append(paper)

            return papers

        except Exception as e:
            print(f"Error fetching ArXiv category: {e}")
            return []


class ProductHuntScraper(WebScraper):
    """Scraper for Product Hunt launches"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://www.producthunt.com"
        self.api_url = "https://api.producthunt.com/v2/api/graphql"

    def get_trending_products(self, days_ago: int = 0, limit: int = 20) -> List[Dict]:
        """Get trending products from Product Hunt
        days_ago: 0 for today, 1 for yesterday, etc.
        """
        # Calculate date
        from datetime import timedelta
        target_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')

        # GraphQL query
        query = """
        query($date: String!, $first: Int!) {
          posts(order: VOTES, postedAfter: $date, first: $first) {
            edges {
              node {
                id
                name
                tagline
                description
                url
                website
                votesCount
                commentsCount
                createdAt
                topics {
                  edges {
                    node {
                      name
                    }
                  }
                }
                user {
                  username
                  name
                }
              }
            }
          }
        }
        """

        variables = {
            "date": target_date,
            "first": limit
        }

        headers = {
            'Content-Type': 'application/json',
        }

        try:
            # Note: Product Hunt API requires authentication for full access
            # This is a simplified version - in production, you'd need API token
            response = self.session.post(
                self.api_url,
                json={'query': query, 'variables': variables},
                headers=headers,
                timeout=10
            )

            if response.status_code == 401:
                print("Product Hunt API requires authentication. Using web scraping fallback...")
                return self._scrape_trending_web(days_ago, limit)

            response.raise_for_status()
            data = response.json()

            products = []
            for edge in data.get('data', {}).get('posts', {}).get('edges', []):
                node = edge['node']
                products.append({
                    'id': node.get('id'),
                    'name': node.get('name'),
                    'tagline': node.get('tagline'),
                    'description': node.get('description', ''),
                    'url': f"{self.base_url}/posts/{node.get('slug', '')}",
                    'website': node.get('website'),
                    'votes': node.get('votesCount', 0),
                    'comments': node.get('commentsCount', 0),
                    'topics': [t['node']['name'] for t in node.get('topics', {}).get('edges', [])],
                    'maker': node.get('user', {}).get('name', ''),
                    'created_at': node.get('createdAt'),
                    'scraped_at': datetime.now().isoformat()
                })

            return products

        except Exception as e:
            print(f"Error with Product Hunt API: {e}")
            return self._scrape_trending_web(days_ago, limit)

    def _scrape_trending_web(self, days_ago: int = 0, limit: int = 20) -> List[Dict]:
        """Fallback web scraping method"""
        url = self.base_url
        if days_ago > 0:
            from datetime import timedelta
            date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            url = f"{self.base_url}/time-travel/{date}"

        try:
            html = self.fetch(url)
            if not html:
                return []

            soup = self.parse_html(html)
            products = []

            # Find product cards
            product_cards = soup.select('[data-test="post-item"]')[:limit]

            for card in product_cards:
                try:
                    title_elem = card.select_one('h3')
                    tagline_elem = card.select_one('p')
                    votes_elem = card.select_one('[data-test="vote-button"]')

                    products.append({
                        'name': title_elem.text.strip() if title_elem else '',
                        'tagline': tagline_elem.text.strip() if tagline_elem else '',
                        'votes': votes_elem.text.strip() if votes_elem else '0',
                        'url': self.base_url + card.get('href', ''),
                        'scraped_at': datetime.now().isoformat()
                    })
                except:
                    continue

            return products

        except Exception as e:
            print(f"Error scraping Product Hunt: {e}")
            return []


class PapersWithCodeScraper(WebScraper):
    """Scraper for Papers with Code"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://paperswithcode.com"

    def get_trending_papers(self, limit: int = 20) -> List[Dict]:
        """Get trending papers from Papers with Code"""
        url = f"{self.base_url}/trending"

        try:
            html = self.fetch(url)
            if not html:
                return []

            soup = self.parse_html(html)
            papers = []

            # Find paper items
            paper_items = soup.select('.paper-card, .infinite-item')[:limit]

            for item in paper_items:
                try:
                    title_elem = item.select_one('h1, .item-content h2')
                    abstract_elem = item.select_one('.item-content p, .paper-abstract')

                    # Extract stars/likes
                    stars_elem = item.select_one('.entity-stars, .stars')
                    stars = 0
                    if stars_elem:
                        stars_text = stars_elem.text.strip()
                        stars_match = re.search(r'(\d+)', stars_text)
                        if stars_match:
                            stars = int(stars_match.group(1))

                    # Extract paper link
                    link_elem = item.select_one('a[href*="/paper/"]')
                    paper_url = ''
                    if link_elem:
                        paper_url = self.base_url + link_elem.get('href', '')

                    # Extract code link
                    code_elem = item.select_one('a[href*="github.com"]')
                    code_url = code_elem.get('href', '') if code_elem else ''

                    # Extract date
                    date_elem = item.select_one('.item-date, time')
                    published_date = date_elem.text.strip() if date_elem else ''

                    papers.append({
                        'title': title_elem.text.strip() if title_elem else '',
                        'abstract': abstract_elem.text.strip()[:500] if abstract_elem else '',
                        'url': paper_url,
                        'code_url': code_url,
                        'stars': stars,
                        'published': published_date,
                        'scraped_at': datetime.now().isoformat()
                    })

                except Exception as e:
                    print(f"Error parsing paper item: {e}")
                    continue

            return papers

        except Exception as e:
            print(f"Error fetching Papers with Code: {e}")
            return []

    def search_papers(self, query: str, limit: int = 20) -> List[Dict]:
        """Search papers on Papers with Code"""
        url = f"{self.base_url}/search"
        params = {'q': query}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            papers = []

            # Find search results
            result_items = soup.select('.infinite-container .row, .paper-card')[:limit]

            for item in result_items:
                try:
                    title_elem = item.select_one('h1, h2, .paper-title')
                    abstract_elem = item.select_one('.paper-abstract, p')

                    # Extract paper link
                    link_elem = item.select_one('a[href*="/paper/"]')
                    paper_url = ''
                    if link_elem:
                        paper_url = self.base_url + link_elem.get('href', '')

                    # Extract metrics
                    metrics_elem = item.select_one('.paper-metrics')
                    stars = 0
                    if metrics_elem:
                        stars_match = re.search(r'(\d+)\s*stars?', metrics_elem.text)
                        if stars_match:
                            stars = int(stars_match.group(1))

                    papers.append({
                        'title': title_elem.text.strip() if title_elem else '',
                        'abstract': abstract_elem.text.strip()[:500] if abstract_elem else '',
                        'url': paper_url,
                        'stars': stars,
                        'scraped_at': datetime.now().isoformat()
                    })

                except:
                    continue

            return papers

        except Exception as e:
            print(f"Error searching Papers with Code: {e}")
            return []


class LobstersScraper(WebScraper):
    """Scraper for Lobste.rs community"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://lobste.rs"

    def get_hottest_stories(self, limit: int = 25) -> List[Dict]:
        """Get hottest stories from Lobste.rs"""
        url = f"{self.base_url}/hottest.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            stories = response.json()

            result = []
            for story in stories[:limit]:
                # Handle both dict and string response
                if isinstance(story, dict):
                    result.append({
                        'id': story.get('short_id'),
                        'title': story.get('title'),
                        'url': story.get('url'),
                        'score': story.get('score', 0),
                        'comments_count': story.get('comment_count', 0),
                        'description': story.get('description', ''),
                        'author': story.get('submitter_user', {}).get('username', '') if isinstance(story.get('submitter_user'), dict) else '',
                        'tags': story.get('tags', []),
                        'created_at': story.get('created_at'),
                        'comments_url': story.get('comments_url'),
                        'scraped_at': datetime.now().isoformat()
                    })

            return result

        except Exception as e:
            print(f"Error fetching Lobste.rs hottest: {e}")
            return []

    def get_newest_stories(self, limit: int = 25) -> List[Dict]:
        """Get newest stories from Lobste.rs"""
        url = f"{self.base_url}/newest.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            stories = response.json()

            result = []
            for story in stories[:limit]:
                # Handle both dict and string response
                if isinstance(story, dict):
                    result.append({
                        'id': story.get('short_id'),
                        'title': story.get('title'),
                        'url': story.get('url'),
                        'score': story.get('score', 0),
                        'comments_count': story.get('comment_count', 0),
                        'description': story.get('description', ''),
                        'author': story.get('submitter_user', {}).get('username', '') if isinstance(story.get('submitter_user'), dict) else '',
                        'tags': story.get('tags', []),
                        'created_at': story.get('created_at'),
                        'comments_url': story.get('comments_url'),
                        'scraped_at': datetime.now().isoformat()
                    })

            return result

        except Exception as e:
            print(f"Error fetching Lobste.rs newest: {e}")
            return []

    def search_stories(self, query: str, limit: int = 25) -> List[Dict]:
        """Search stories on Lobste.rs"""
        url = f"{self.base_url}/search"
        params = {'q': query, 'what': 'stories', 'order': 'relevance'}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            stories = []

            # Find story items
            story_items = soup.select('.story')[:limit]

            for item in story_items:
                try:
                    title_elem = item.select_one('.link a')
                    score_elem = item.select_one('.score')
                    tags = [tag.text.strip() for tag in item.select('.tags a')]
                    author_elem = item.select_one('.byline a.u-author')
                    comments_elem = item.select_one('.comments_label a')

                    story_url = title_elem.get('href', '') if title_elem else ''
                    comments_url = ''
                    comments_count = 0

                    if comments_elem:
                        comments_url = self.base_url + comments_elem.get('href', '')
                        comments_text = comments_elem.text.strip()
                        comments_match = re.search(r'(\d+)', comments_text)
                        if comments_match:
                            comments_count = int(comments_match.group(1))

                    stories.append({
                        'title': title_elem.text.strip() if title_elem else '',
                        'url': story_url,
                        'score': int(score_elem.text.strip()) if score_elem else 0,
                        'comments_count': comments_count,
                        'comments_url': comments_url,
                        'author': author_elem.text.strip() if author_elem else '',
                        'tags': tags,
                        'scraped_at': datetime.now().isoformat()
                    })

                except:
                    continue

            return stories

        except Exception as e:
            print(f"Error searching Lobste.rs: {e}")
            return []

    def get_story_with_comments(self, story_id: str, limit: int = 10) -> Dict:
        """Get a story with its comments"""
        url = f"{self.base_url}/s/{story_id}.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            story = {
                'id': data.get('short_id'),
                'title': data.get('title'),
                'url': data.get('url'),
                'score': data.get('score', 0),
                'author': data.get('submitter_user', {}).get('username', ''),
                'tags': data.get('tags', []),
                'created_at': data.get('created_at'),
                'description': data.get('description', ''),
                'comments': []
            }

            # Parse comments
            for comment in data.get('comments', [])[:limit]:
                story['comments'].append({
                    'id': comment.get('short_id'),
                    'author': comment.get('commenting_user', {}).get('username', ''),
                    'content': comment.get('comment', '')[:1000],
                    'score': comment.get('score', 0),
                    'created_at': comment.get('created_at'),
                    'indent_level': comment.get('indent_level', 0)
                })

            story['scraped_at'] = datetime.now().isoformat()
            return story

        except Exception as e:
            print(f"Error fetching Lobste.rs story: {e}")
            return {}


def demo_additional_scrapers():
    """Demo the new scrapers"""
    print("\n" + "="*70)
    print("ADDITIONAL SCRAPERS DEMO")
    print("="*70)

    # Dev.to
    print("\n📝 Dev.to Articles:")
    print("-" * 40)
    devto = DevToScraper()
    articles = devto.get_articles(per_page=3, state='rising')
    for article in articles:
        print(f"\n{article['title']}")
        print(f"  Author: {article['author']} | Reactions: {article['positive_reactions']} | Comments: {article['comments_count']}")
        print(f"  Tags: {', '.join(article['tags'])}")

    # ArXiv
    print("\n📚 ArXiv Papers (AI):")
    print("-" * 40)
    arxiv = ArXivScraper()
    papers = arxiv.search_papers("large language models", max_results=3)
    for paper in papers:
        print(f"\n{paper['title']}")
        print(f"  Authors: {', '.join(paper['authors'][:3])}")
        print(f"  Categories: {', '.join(paper['categories'])}")
        print(f"  Published: {paper['published'][:10]}")

    # Product Hunt
    print("\n🚀 Product Hunt Launches:")
    print("-" * 40)
    ph = ProductHuntScraper()
    products = ph.get_trending_products(days_ago=0, limit=3)
    for product in products:
        if product.get('name'):
            print(f"\n{product['name']}: {product.get('tagline', '')}")
            print(f"  Votes: {product.get('votes', 0)}")

    # Papers with Code
    print("\n🔬 Papers with Code Trending:")
    print("-" * 40)
    pwc = PapersWithCodeScraper()
    trending = pwc.get_trending_papers(limit=3)
    for paper in trending:
        if paper.get('title'):
            print(f"\n{paper['title']}")
            print(f"  Stars: {paper['stars']} | Code: {'Yes' if paper.get('code_url') else 'No'}")

    # Lobste.rs
    print("\n🦞 Lobste.rs Hottest:")
    print("-" * 40)
    lobsters = LobstersScraper()
    stories = lobsters.get_hottest_stories(limit=3)
    for story in stories:
        print(f"\n{story['title']}")
        print(f"  Score: {story['score']} | Comments: {story['comments_count']}")
        print(f"  Tags: {', '.join(story['tags'])}")

    # Save sample data
    sample_data = {
        'timestamp': datetime.now().isoformat(),
        'devto_articles': articles[:2],
        'arxiv_papers': papers[:2],
        'product_hunt': products[:2],
        'papers_with_code': trending[:2],
        'lobsters_stories': stories[:2]
    }

    filename = f"additional_scrapers_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(sample_data, f, indent=2, default=str)

    print(f"\n\n✅ Sample data saved to: {filename}")


if __name__ == "__main__":
    demo_additional_scrapers()