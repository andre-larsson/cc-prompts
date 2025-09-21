#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Optional
import re
from urllib.parse import quote, urljoin
from scraper import WebScraper


class StackOverflowScraper(WebScraper):
    """Scraper for Stack Overflow using Stack Exchange API"""

    def __init__(self):
        super().__init__(delay=0.5)
        self.base_url = "https://stackoverflow.com"
        self.api_url = "https://api.stackexchange.com/2.3"
        self.site = "stackoverflow"

    def get_trending_questions(self, tagged: str = None, sort: str = "hot", limit: int = 30) -> List[Dict]:
        """Get trending questions from Stack Overflow
        sort: hot, week, month, interesting, featured
        """
        url = f"{self.api_url}/questions"
        params = {
            'order': 'desc',
            'sort': sort,
            'site': self.site,
            'pagesize': min(limit, 100),
            'filter': '!9_bDE(fI5'  # Include body in response
        }

        if tagged:
            params['tagged'] = tagged

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            questions = []
            for item in data.get('items', []):
                questions.append({
                    'id': item.get('question_id'),
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'score': item.get('score', 0),
                    'answer_count': item.get('answer_count', 0),
                    'view_count': item.get('view_count', 0),
                    'is_answered': item.get('is_answered', False),
                    'tags': item.get('tags', []),
                    'owner': item.get('owner', {}).get('display_name', 'anonymous'),
                    'creation_date': datetime.fromtimestamp(item.get('creation_date', 0)).isoformat(),
                    'last_activity': datetime.fromtimestamp(item.get('last_activity_date', 0)).isoformat(),
                    'body_preview': item.get('body', '')[:500],
                    'scraped_at': datetime.now().isoformat()
                })

            return questions

        except Exception as e:
            print(f"Error fetching Stack Overflow questions: {e}")
            return []

    def search_questions(self, query: str, tagged: str = None, sort: str = "relevance", limit: int = 30) -> List[Dict]:
        """Search for questions on Stack Overflow
        sort: activity, votes, creation, relevance
        """
        url = f"{self.api_url}/search/advanced"
        params = {
            'order': 'desc',
            'sort': sort,
            'q': query,
            'site': self.site,
            'pagesize': min(limit, 100),
            'filter': '!9_bDE(fI5'
        }

        if tagged:
            params['tagged'] = tagged

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            questions = []
            for item in data.get('items', []):
                questions.append({
                    'id': item.get('question_id'),
                    'title': item.get('title'),
                    'link': item.get('link'),
                    'score': item.get('score', 0),
                    'answer_count': item.get('answer_count', 0),
                    'view_count': item.get('view_count', 0),
                    'is_answered': item.get('is_answered', False),
                    'tags': item.get('tags', []),
                    'owner': item.get('owner', {}).get('display_name', 'anonymous'),
                    'creation_date': datetime.fromtimestamp(item.get('creation_date', 0)).isoformat(),
                    'body_preview': item.get('body', '')[:500],
                    'scraped_at': datetime.now().isoformat()
                })

            return questions

        except Exception as e:
            print(f"Error searching Stack Overflow: {e}")
            return []

    def get_question_with_answers(self, question_id: int, limit: int = 5) -> Dict:
        """Get a question with its top answers"""
        url = f"{self.api_url}/questions/{question_id}"
        params = {
            'site': self.site,
            'filter': '!9_bDE(fI5'
        }

        try:
            # Get question details
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('items'):
                return {}

            question = data['items'][0]
            result = {
                'id': question.get('question_id'),
                'title': question.get('title'),
                'link': question.get('link'),
                'score': question.get('score', 0),
                'body': question.get('body', '')[:2000],
                'tags': question.get('tags', []),
                'owner': question.get('owner', {}).get('display_name', 'anonymous'),
                'creation_date': datetime.fromtimestamp(question.get('creation_date', 0)).isoformat(),
                'answers': []
            }

            # Get answers
            answers_url = f"{self.api_url}/questions/{question_id}/answers"
            answers_params = {
                'order': 'desc',
                'sort': 'votes',
                'site': self.site,
                'pagesize': min(limit, 100),
                'filter': '!9_bDE(fI5'
            }

            answers_response = self.session.get(answers_url, params=answers_params, timeout=10)
            answers_response.raise_for_status()
            answers_data = answers_response.json()

            for answer in answers_data.get('items', []):
                result['answers'].append({
                    'id': answer.get('answer_id'),
                    'score': answer.get('score', 0),
                    'is_accepted': answer.get('is_accepted', False),
                    'body': answer.get('body', '')[:1000],
                    'owner': answer.get('owner', {}).get('display_name', 'anonymous'),
                    'creation_date': datetime.fromtimestamp(answer.get('creation_date', 0)).isoformat()
                })

            result['scraped_at'] = datetime.now().isoformat()
            return result

        except Exception as e:
            print(f"Error fetching question with answers: {e}")
            return {}


class HuggingFaceScraper(WebScraper):
    """Scraper for Hugging Face models, datasets, and spaces"""

    def __init__(self):
        super().__init__(delay=0.5)
        self.base_url = "https://huggingface.co"
        self.api_url = f"{self.base_url}/api"

    def get_trending_models(self, sort: str = "downloads", limit: int = 30) -> List[Dict]:
        """Get trending models from Hugging Face
        sort: downloads, likes, modified, created
        """
        url = f"{self.api_url}/models"
        params = {
            'sort': sort,
            'direction': -1,
            'limit': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            models = response.json()

            result = []
            for model in models:
                result.append({
                    'id': model.get('id'),
                    'name': model.get('id', '').split('/')[-1] if '/' in model.get('id', '') else model.get('id'),
                    'author': model.get('id', '').split('/')[0] if '/' in model.get('id', '') else '',
                    'url': f"{self.base_url}/{model.get('id')}",
                    'downloads': model.get('downloads', 0),
                    'likes': model.get('likes', 0),
                    'task': model.get('pipeline_tag', ''),
                    'tags': model.get('tags', []),
                    'library': model.get('library_name', ''),
                    'created_at': model.get('created_at', ''),
                    'modified_at': model.get('lastModified', ''),
                    'private': model.get('private', False),
                    'scraped_at': datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"Error fetching Hugging Face models: {e}")
            return []

    def search_models(self, query: str, limit: int = 30) -> List[Dict]:
        """Search for models on Hugging Face"""
        url = f"{self.api_url}/models"
        params = {
            'search': query,
            'limit': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            models = response.json()

            result = []
            for model in models:
                result.append({
                    'id': model.get('id'),
                    'name': model.get('id', '').split('/')[-1] if '/' in model.get('id', '') else model.get('id'),
                    'author': model.get('id', '').split('/')[0] if '/' in model.get('id', '') else '',
                    'url': f"{self.base_url}/{model.get('id')}",
                    'downloads': model.get('downloads', 0),
                    'likes': model.get('likes', 0),
                    'task': model.get('pipeline_tag', ''),
                    'tags': model.get('tags', []),
                    'scraped_at': datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"Error searching Hugging Face models: {e}")
            return []

    def get_trending_datasets(self, sort: str = "downloads", limit: int = 30) -> List[Dict]:
        """Get trending datasets from Hugging Face"""
        url = f"{self.api_url}/datasets"
        params = {
            'sort': sort,
            'direction': -1,
            'limit': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            datasets = response.json()

            result = []
            for dataset in datasets:
                result.append({
                    'id': dataset.get('id'),
                    'name': dataset.get('id', '').split('/')[-1] if '/' in dataset.get('id', '') else dataset.get('id'),
                    'author': dataset.get('id', '').split('/')[0] if '/' in dataset.get('id', '') else '',
                    'url': f"{self.base_url}/datasets/{dataset.get('id')}",
                    'downloads': dataset.get('downloads', 0),
                    'likes': dataset.get('likes', 0),
                    'task_categories': dataset.get('task_categories', []),
                    'tags': dataset.get('tags', []),
                    'size_categories': dataset.get('size_categories', []),
                    'created_at': dataset.get('created_at', ''),
                    'modified_at': dataset.get('lastModified', ''),
                    'scraped_at': datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"Error fetching Hugging Face datasets: {e}")
            return []

    def get_trending_spaces(self, sort: str = "likes", limit: int = 30) -> List[Dict]:
        """Get trending spaces (apps) from Hugging Face"""
        url = f"{self.api_url}/spaces"
        params = {
            'sort': sort,
            'direction': -1,
            'limit': limit
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            spaces = response.json()

            result = []
            for space in spaces:
                result.append({
                    'id': space.get('id'),
                    'name': space.get('id', '').split('/')[-1] if '/' in space.get('id', '') else space.get('id'),
                    'author': space.get('id', '').split('/')[0] if '/' in space.get('id', '') else '',
                    'url': f"{self.base_url}/spaces/{space.get('id')}",
                    'likes': space.get('likes', 0),
                    'sdk': space.get('sdk', ''),
                    'tags': space.get('tags', []),
                    'created_at': space.get('created_at', ''),
                    'modified_at': space.get('lastModified', ''),
                    'scraped_at': datetime.now().isoformat()
                })

            return result

        except Exception as e:
            print(f"Error fetching Hugging Face spaces: {e}")
            return []


class HashnodeScraper(WebScraper):
    """Scraper for Hashnode blog platform"""

    def __init__(self):
        super().__init__(delay=0.5)
        self.base_url = "https://hashnode.com"
        self.api_url = "https://gql.hashnode.com"

    def get_trending_posts(self, period: str = "7", limit: int = 20) -> List[Dict]:
        """Get trending posts from Hashnode
        period: 7 (week), 30 (month), 365 (year)
        """
        query = """
        query GetTrendingPosts($first: Int!) {
            feed(first: $first, filter: {type: FEATURED}) {
                edges {
                    node {
                        id
                        title
                        brief
                        slug
                        url
                        author {
                            username
                            name
                        }
                        publication {
                            domain
                        }
                        tags {
                            name
                        }
                        reactionCount
                        responseCount
                        views
                        publishedAt
                    }
                }
            }
        }
        """

        variables = {"first": limit}

        try:
            response = self.session.post(
                self.api_url,
                json={'query': query, 'variables': variables},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            posts = []
            for edge in data.get('data', {}).get('feed', {}).get('edges', []):
                node = edge['node']
                posts.append({
                    'id': node.get('id'),
                    'title': node.get('title'),
                    'brief': node.get('brief', '')[:500],
                    'url': node.get('url'),
                    'author': node.get('author', {}).get('username', ''),
                    'author_name': node.get('author', {}).get('name', ''),
                    'tags': [tag['name'] for tag in node.get('tags', [])],
                    'reactions': node.get('reactionCount', 0),
                    'responses': node.get('responseCount', 0),
                    'views': node.get('views', 0),
                    'published_at': node.get('publishedAt'),
                    'scraped_at': datetime.now().isoformat()
                })

            return posts

        except Exception as e:
            print(f"Error fetching Hashnode trending posts: {e}")
            return []

    def search_posts(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for posts on Hashnode"""
        graphql_query = """
        query SearchPosts($query: String!, $first: Int!) {
            searchPostsOfPublication(
                filter: {query: $query}
                first: $first
            ) {
                edges {
                    node {
                        id
                        title
                        brief
                        slug
                        url
                        author {
                            username
                            name
                        }
                        tags {
                            name
                        }
                        reactionCount
                        responseCount
                        publishedAt
                    }
                }
            }
        }
        """

        variables = {
            "query": query,
            "first": limit
        }

        try:
            response = self.session.post(
                self.api_url,
                json={'query': graphql_query, 'variables': variables},
                timeout=10
            )

            if response.status_code != 200:
                # Fallback to web scraping
                return self._search_posts_web(query, limit)

            data = response.json()
            posts = []

            edges = data.get('data', {}).get('searchPostsOfPublication', {}).get('edges', [])
            for edge in edges:
                node = edge['node']
                posts.append({
                    'id': node.get('id'),
                    'title': node.get('title'),
                    'brief': node.get('brief', '')[:500],
                    'url': node.get('url'),
                    'author': node.get('author', {}).get('username', ''),
                    'tags': [tag['name'] for tag in node.get('tags', [])],
                    'reactions': node.get('reactionCount', 0),
                    'responses': node.get('responseCount', 0),
                    'published_at': node.get('publishedAt'),
                    'scraped_at': datetime.now().isoformat()
                })

            return posts

        except Exception as e:
            print(f"Error searching Hashnode: {e}")
            return self._search_posts_web(query, limit)

    def _search_posts_web(self, query: str, limit: int) -> List[Dict]:
        """Fallback web search"""
        try:
            # Use explore page as fallback
            url = f"{self.base_url}/explore"
            html = self.fetch(url)
            if not html:
                return []

            soup = self.parse_html(html)
            posts = []

            # Find article cards
            article_cards = soup.select('article')[:limit]
            for card in article_cards:
                title_elem = card.select_one('h2')
                if title_elem and query.lower() in title_elem.text.lower():
                    posts.append({
                        'title': title_elem.text.strip(),
                        'url': card.select_one('a')['href'] if card.select_one('a') else '',
                        'scraped_at': datetime.now().isoformat()
                    })

            return posts

        except Exception as e:
            print(f"Error in web fallback: {e}")
            return []


class TechCrunchScraper(WebScraper):
    """Scraper for TechCrunch tech news"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://techcrunch.com"

    def get_latest_articles(self, category: str = None, limit: int = 20) -> List[Dict]:
        """Get latest articles from TechCrunch
        category: startups, venture, security, crypto, apps, etc.
        """
        if category:
            url = f"{self.base_url}/category/{category}/"
        else:
            url = self.base_url

        try:
            html = self.fetch(url)
            if not html:
                return []

            soup = self.parse_html(html)
            articles = []

            # Find article containers
            article_items = soup.select('.post-block, article.post')[:limit]

            for item in article_items:
                try:
                    title_elem = item.select_one('h2.post-block__title, h2')
                    link_elem = item.select_one('a.post-block__title__link, h2 a')
                    excerpt_elem = item.select_one('.post-block__content, .excerpt')
                    author_elem = item.select_one('.river-byline__authors, .byline')
                    time_elem = item.select_one('time')

                    if title_elem and link_elem:
                        articles.append({
                            'title': title_elem.text.strip(),
                            'url': link_elem.get('href', ''),
                            'excerpt': excerpt_elem.text.strip()[:500] if excerpt_elem else '',
                            'author': author_elem.text.strip() if author_elem else '',
                            'published_at': time_elem.get('datetime', '') if time_elem else '',
                            'category': category or 'general',
                            'scraped_at': datetime.now().isoformat()
                        })
                except:
                    continue

            return articles

        except Exception as e:
            print(f"Error fetching TechCrunch articles: {e}")
            return []

    def search_articles(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for articles on TechCrunch"""
        url = f"{self.base_url}/search/{quote(query)}"

        try:
            html = self.fetch(url)
            if not html:
                return []

            soup = self.parse_html(html)
            articles = []

            # Find search results
            result_items = soup.select('.post-block, article')[:limit]

            for item in result_items:
                try:
                    title_elem = item.select_one('h2')
                    link_elem = item.select_one('h2 a')
                    excerpt_elem = item.select_one('.post-block__content, p')
                    time_elem = item.select_one('time')

                    if title_elem:
                        articles.append({
                            'title': title_elem.text.strip(),
                            'url': link_elem.get('href', '') if link_elem else '',
                            'excerpt': excerpt_elem.text.strip()[:500] if excerpt_elem else '',
                            'published_at': time_elem.get('datetime', '') if time_elem else '',
                            'scraped_at': datetime.now().isoformat()
                        })
                except:
                    continue

            return articles

        except Exception as e:
            print(f"Error searching TechCrunch: {e}")
            return []

    def get_article_content(self, article_url: str) -> Dict:
        """Get full article content"""
        try:
            html = self.fetch(article_url)
            if not html:
                return {}

            soup = self.parse_html(html)

            # Extract article details
            title = soup.select_one('h1')
            author = soup.select_one('.article__byline__author, .byline')
            time_elem = soup.select_one('time')
            content_elem = soup.select_one('.article-content, .entry-content')

            # Extract paragraphs
            paragraphs = []
            if content_elem:
                for p in content_elem.find_all('p')[:10]:
                    text = p.get_text().strip()
                    if len(text) > 50:
                        paragraphs.append(text)

            return {
                'url': article_url,
                'title': title.text.strip() if title else '',
                'author': author.text.strip() if author else '',
                'published_at': time_elem.get('datetime', '') if time_elem else '',
                'content': '\n\n'.join(paragraphs[:5]),
                'scraped_at': datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error fetching article content: {e}")
            return {}


class AngelListScraper(WebScraper):
    """Scraper for AngelList/Wellfound startup data"""

    def __init__(self):
        super().__init__(delay=2.0)  # Be respectful
        self.base_url = "https://wellfound.com"
        # Add common browser headers to avoid blocks
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def get_trending_startups(self, location: str = None, market: str = None, limit: int = 20) -> List[Dict]:
        """Get trending startups from AngelList"""
        # Note: AngelList has moved to Wellfound.com
        # Using web scraping approach for public data
        url = "https://wellfound.com/startups"

        try:
            params = {}
            if location:
                params['location'] = location
            if market:
                params['market'] = market

            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            startups = []

            # Find startup cards
            startup_cards = soup.select('[data-test="StartupCard"], .startup-card, div[class*="startup"]')[:limit]

            for card in startup_cards:
                try:
                    name_elem = card.select_one('h4, h3, .startup-name')
                    tagline_elem = card.select_one('.tagline, .description, p')
                    link_elem = card.select_one('a[href*="/company"]')

                    # Extract funding info
                    funding_elem = card.select_one('[class*="funding"], .raised')
                    team_size_elem = card.select_one('[class*="employees"], .team-size')

                    startup = {
                        'name': name_elem.text.strip() if name_elem else '',
                        'tagline': tagline_elem.text.strip()[:200] if tagline_elem else '',
                        'url': f"https://wellfound.com{link_elem.get('href', '')}" if link_elem else '',
                        'funding': funding_elem.text.strip() if funding_elem else '',
                        'team_size': team_size_elem.text.strip() if team_size_elem else '',
                        'location': location or '',
                        'market': market or '',
                        'scraped_at': datetime.now().isoformat()
                    }

                    if startup['name']:  # Only add if we got a name
                        startups.append(startup)

                except Exception as e:
                    continue

            return startups

        except Exception as e:
            print(f"Error fetching AngelList/Wellfound startups: {e}")
            return []

    def search_startups(self, query: str, limit: int = 20) -> List[Dict]:
        """Search for startups on AngelList/Wellfound"""
        url = f"https://wellfound.com/search"
        params = {'q': query, 'type': 'companies'}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            startups = []

            # Find search results
            result_items = soup.select('.search-result, [data-test*="Company"]')[:limit]

            for item in result_items:
                try:
                    name_elem = item.select_one('h4, h3, .company-name')
                    tagline_elem = item.select_one('.tagline, p')
                    link_elem = item.select_one('a')

                    startups.append({
                        'name': name_elem.text.strip() if name_elem else '',
                        'tagline': tagline_elem.text.strip()[:200] if tagline_elem else '',
                        'url': f"https://wellfound.com{link_elem.get('href', '')}" if link_elem else '',
                        'scraped_at': datetime.now().isoformat()
                    })

                except:
                    continue

            return startups

        except Exception as e:
            print(f"Error searching AngelList/Wellfound: {e}")
            return []

    def get_job_listings(self, role: str = None, location: str = None, limit: int = 20) -> List[Dict]:
        """Get job listings from AngelList/Wellfound"""
        url = "https://wellfound.com/jobs"
        params = {}

        if role:
            params['role'] = role
        if location:
            params['location'] = location

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            jobs = []

            # Find job cards
            job_cards = soup.select('[data-test="JobCard"], .job-listing, div[class*="job"]')[:limit]

            for card in job_cards:
                try:
                    title_elem = card.select_one('.job-title, h3')
                    company_elem = card.select_one('.company-name, h4')
                    location_elem = card.select_one('.location, [class*="location"]')
                    salary_elem = card.select_one('.salary, [class*="compensation"]')
                    link_elem = card.select_one('a')

                    jobs.append({
                        'title': title_elem.text.strip() if title_elem else '',
                        'company': company_elem.text.strip() if company_elem else '',
                        'location': location_elem.text.strip() if location_elem else '',
                        'salary': salary_elem.text.strip() if salary_elem else '',
                        'url': f"https://wellfound.com{link_elem.get('href', '')}" if link_elem else '',
                        'scraped_at': datetime.now().isoformat()
                    })

                except:
                    continue

            return jobs

        except Exception as e:
            print(f"Error fetching job listings: {e}")
            return []


def demo_additional_scrapers_v2():
    """Demo the new scrapers"""
    print("\n" + "="*70)
    print("ADDITIONAL SCRAPERS V2 DEMO")
    print("="*70)

    # Stack Overflow
    print("\n💻 Stack Overflow Trending:")
    print("-" * 40)
    so = StackOverflowScraper()
    questions = so.get_trending_questions(tagged="python", sort="hot", limit=3)
    for q in questions:
        print(f"\n{q['title']}")
        print(f"  Score: {q['score']} | Answers: {q['answer_count']} | Views: {q['view_count']}")
        print(f"  Tags: {', '.join(q['tags'])}")

    # Hugging Face
    print("\n🤗 Hugging Face Trending Models:")
    print("-" * 40)
    hf = HuggingFaceScraper()
    models = hf.get_trending_models(sort="downloads", limit=3)
    for model in models:
        print(f"\n{model['id']}")
        print(f"  Downloads: {model['downloads']:,} | Likes: {model['likes']}")
        print(f"  Task: {model['task']} | Library: {model['library']}")

    # Hashnode
    print("\n📝 Hashnode Trending Posts:")
    print("-" * 40)
    hn = HashnodeScraper()
    posts = hn.get_trending_posts(limit=3)
    for post in posts:
        if post.get('title'):
            print(f"\n{post['title']}")
            print(f"  Author: {post['author']} | Reactions: {post['reactions']} | Views: {post.get('views', 0)}")

    # TechCrunch
    print("\n📰 TechCrunch Latest:")
    print("-" * 40)
    tc = TechCrunchScraper()
    articles = tc.get_latest_articles(limit=3)
    for article in articles:
        if article.get('title'):
            print(f"\n{article['title']}")
            print(f"  {article['excerpt'][:100]}..." if article.get('excerpt') else "")

    # AngelList/Wellfound
    print("\n🚀 AngelList/Wellfound Startups:")
    print("-" * 40)
    al = AngelListScraper()
    startups = al.get_trending_startups(limit=3)
    for startup in startups:
        if startup.get('name'):
            print(f"\n{startup['name']}")
            print(f"  {startup['tagline']}")
            print(f"  Funding: {startup.get('funding', 'N/A')}")

    # Save sample data
    sample_data = {
        'timestamp': datetime.now().isoformat(),
        'stackoverflow_questions': questions[:2],
        'huggingface_models': models[:2],
        'hashnode_posts': posts[:2],
        'techcrunch_articles': articles[:2],
        'angellist_startups': startups[:2]
    }

    filename = f"scrapers_v2_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(sample_data, f, indent=2, default=str)

    print(f"\n\n✅ Sample data saved to: {filename}")


if __name__ == "__main__":
    demo_additional_scrapers_v2()