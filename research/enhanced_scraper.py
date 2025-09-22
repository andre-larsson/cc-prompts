#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin
from scraper import WebScraper, HackerNewsScraper, RedditScraper, GitHubTrendingScraper
from additional_scrapers import DevToScraper, ArXivScraper, ProductHuntScraper, PapersWithCodeScraper, LobstersScraper
from additional_scrapers_v2 import StackOverflowScraper, HuggingFaceScraper, HashnodeScraper, TechCrunchScraper, AngelListScraper
from additional_scrapers_v3 import KaggleScraper, IndieHackersScraper, TheVergeScraper, ArsTechnicaScraper, PyPIScraper, NPMScraper


class ContentFetcher(WebScraper):
    def __init__(self):
        super().__init__(delay=1.0)

    def fetch_article_content(self, url: str) -> Dict:
        """Fetch and extract main content from a URL"""
        try:
            html = self.fetch(url)
            if not html:
                return {'url': url, 'error': 'Failed to fetch content'}

            soup = self.parse_html(html)

            # Remove script and style elements
            for script in soup(["script", "style", "noscript"]):
                script.decompose()

            # Extract metadata
            title = self._extract_title(soup)
            description = self._extract_description(soup)
            author = self._extract_author(soup)
            date = self._extract_date(soup)

            # Extract main content
            content = self._extract_main_content(soup)

            # Extract key paragraphs
            paragraphs = soup.find_all('p')
            text_content = []
            for p in paragraphs[:20]:  # Limit to first 20 paragraphs
                text = p.get_text().strip()
                if len(text) > 50:  # Skip very short paragraphs
                    text_content.append(text)

            return {
                'url': url,
                'title': title,
                'description': description,
                'author': author,
                'date': date,
                'content_preview': '\n\n'.join(text_content[:5]),  # First 5 meaningful paragraphs
                'full_text': content[:5000] if content else '',  # Limit to 5000 chars
                'word_count': len(content.split()) if content else 0
            }

        except Exception as e:
            return {'url': url, 'error': str(e)}

    def _extract_title(self, soup):
        # Try multiple common title patterns
        title = soup.find('title')
        if title:
            return title.text.strip()

        h1 = soup.find('h1')
        if h1:
            return h1.text.strip()

        og_title = soup.find('meta', {'property': 'og:title'})
        if og_title:
            return og_title.get('content', '')

        return ''

    def _extract_description(self, soup):
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')

        og_desc = soup.find('meta', {'property': 'og:description'})
        if og_desc:
            return og_desc.get('content', '')

        return ''

    def _extract_author(self, soup):
        author_meta = soup.find('meta', {'name': 'author'})
        if author_meta:
            return author_meta.get('content', '')

        author_span = soup.find('span', {'class': re.compile('author|byline', re.I)})
        if author_span:
            return author_span.text.strip()

        return ''

    def _extract_date(self, soup):
        date_meta = soup.find('meta', {'property': 'article:published_time'})
        if date_meta:
            return date_meta.get('content', '')

        time_elem = soup.find('time')
        if time_elem:
            return time_elem.get('datetime', time_elem.text.strip())

        return ''

    def _extract_main_content(self, soup):
        # Try to find main content area
        main_selectors = [
            'main', 'article', '[role="main"]', '.content', '#content',
            '.post-content', '.entry-content', '.article-body'
        ]

        for selector in main_selectors:
            main = soup.select_one(selector)
            if main:
                return main.get_text(' ', strip=True)

        # Fallback to body text
        body = soup.find('body')
        if body:
            return body.get_text(' ', strip=True)

        return ''


class EnhancedHackerNewsScraper(HackerNewsScraper):
    def get_story_with_comments(self, story_id: str, comment_limit: int = 10) -> Dict:
        """Get story details with top comments"""
        url = f"{self.base_url}/item?id={story_id}"
        html = self.fetch(url)
        if not html:
            return {}

        soup = self.parse_html(html)

        # Get story details
        story = {
            'id': story_id,
            'url': url
        }

        title_elem = soup.select_one('.titleline > a')
        if title_elem:
            story['title'] = title_elem.text.strip()
            story['link'] = title_elem.get('href', '')
            if story['link'] and not story['link'].startswith('http'):
                story['link'] = urljoin(self.base_url, story['link'])

        # Get metadata
        subtext = soup.select_one('.subtext')
        if subtext:
            score_elem = subtext.select_one('.score')
            if score_elem:
                story['points'] = int(re.search(r'(\d+)', score_elem.text).group(1))

            user_elem = subtext.select_one('.hnuser')
            if user_elem:
                story['author'] = user_elem.text.strip()

            age_elem = subtext.select_one('.age')
            if age_elem:
                story['age'] = age_elem.text.strip()

        # Get top comments
        story['comments'] = self._extract_top_comments(soup, comment_limit)

        return story

    def _extract_top_comments(self, soup, limit: int = 10) -> List[Dict]:
        """Extract top-level comments with their replies"""
        comments = []
        comment_trees = soup.select('.comment-tree > tbody > tr.athing.comtr')

        for comment_elem in comment_trees[:limit]:
            comment = self._parse_comment_tree(comment_elem, soup)
            if comment:
                comments.append(comment)

        return comments

    def _parse_comment_tree(self, comment_elem, soup) -> Optional[Dict]:
        """Parse comment with nested replies"""
        try:
            comment_id = comment_elem.get('id')

            # Check indentation level
            indent_elem = comment_elem.select_one('.ind img')
            indent = 0
            if indent_elem and indent_elem.get('width'):
                indent = int(indent_elem['width']) // 40

            # Only process top-level comments (indent = 0)
            if indent > 0:
                return None

            # Get comment text
            text_elem = comment_elem.select_one('.commtext')
            text = ''
            if text_elem:
                for br in text_elem.find_all('br'):
                    br.replace_with('\n')
                text = text_elem.get_text().strip()

            # Get metadata
            user_elem = comment_elem.select_one('.hnuser')
            author = user_elem.text.strip() if user_elem else '[deleted]'

            age_elem = comment_elem.select_one('.age')
            age = age_elem.text.strip() if age_elem else ''

            # Count direct replies
            reply_count = 0
            next_elem = comment_elem.find_next_sibling('tr')
            while next_elem and 'athing' in next_elem.get('class', []):
                next_indent_elem = next_elem.select_one('.ind img')
                if next_indent_elem and next_indent_elem.get('width'):
                    next_indent = int(next_indent_elem['width']) // 40
                    if next_indent == 1:  # Direct reply
                        reply_count += 1
                    elif next_indent == 0:  # Next top-level comment
                        break
                next_elem = next_elem.find_next_sibling('tr')

            return {
                'id': comment_id,
                'author': author,
                'text': text[:1000],  # Limit comment text
                'age': age,
                'replies': reply_count
            }

        except Exception as e:
            print(f"Error parsing comment: {e}")
            return None

    def search_topics(self, topics: List[str], dateRange: str = 'week', limit: int = 10) -> Dict[str, List[Dict]]:
        """Search for multiple topics and organize results"""
        results = {}

        for topic in topics:
            print(f"Searching for: {topic}")
            stories = self.search_stories(topic, dateRange=dateRange)[:limit]
            results[topic] = stories

        return results


class EnhancedRedditScraper(RedditScraper):
    def get_post_with_comments(self, post_url: str, comment_limit: int = 10) -> Dict:
        """Get Reddit post with top comments"""
        if not post_url.endswith('.json'):
            post_url = post_url.rstrip('/') + '.json'

        try:
            response = self.session.get(post_url, params={'limit': comment_limit}, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Extract post data
            post_data = data[0]['data']['children'][0]['data']
            post = {
                'id': post_data['id'],
                'title': post_data['title'],
                'author': post_data['author'],
                'text': post_data.get('selftext', ''),
                'url': post_data['url'],
                'score': post_data['score'],
                'num_comments': post_data['num_comments'],
                'subreddit': post_data['subreddit'],
                'created_utc': datetime.fromtimestamp(post_data['created_utc']).isoformat()
            }

            # Extract top comments
            comments = []
            if len(data) > 1:
                comment_data = data[1]['data']['children']
                for comment in comment_data[:comment_limit]:
                    if comment['kind'] == 't1':  # t1 = comment
                        c = comment['data']
                        comments.append({
                            'id': c['id'],
                            'author': c['author'],
                            'text': c['body'][:500],  # Limit text length
                            'score': c['score'],
                            'replies': c.get('replies', {}).get('data', {}).get('count', 0) if isinstance(c.get('replies'), dict) else 0,
                            'created_utc': datetime.fromtimestamp(c['created_utc']).isoformat()
                        })

            post['top_comments'] = comments
            return post

        except Exception as e:
            print(f"Error fetching post with comments: {e}")
            return {}

    def search_multiple_topics(self, topics: List[str], subreddits: List[str] = None, time: str = 'week', limit: int = 10) -> Dict:
        """Search multiple topics across subreddits"""
        results = {}

        if not subreddits:
            subreddits = ['all']

        for topic in topics:
            results[topic] = {}
            for subreddit in subreddits:
                print(f"Searching r/{subreddit} for: {topic}")
                posts = self.search_posts(topic, subreddit=subreddit if subreddit != 'all' else None, time=time)[:limit]
                results[topic][subreddit] = posts

        return results


class ResearchAggregator:
    def __init__(self):
        self.hn = EnhancedHackerNewsScraper()
        self.reddit = EnhancedRedditScraper()
        self.github = GitHubTrendingScraper()
        # OpenAI Community scraper removed (was in separate file)
        self.devto = DevToScraper()
        self.arxiv = ArXivScraper()
        # self.producthunt = ProductHuntScraper()  # BLOCKED - 403
        self.paperswithcode = PapersWithCodeScraper()
        self.lobsters = LobstersScraper()
        self.stackoverflow = StackOverflowScraper()
        self.huggingface = HuggingFaceScraper()
        # self.hashnode = HashnodeScraper()  # BLOCKED - API issues
        self.techcrunch = TechCrunchScraper()
        # self.angellist = AngelListScraper()  # BLOCKED - Cloudflare

        # V3 scrapers
        self.kaggle = KaggleScraper()
        self.indiehackers = IndieHackersScraper()
        self.theverge = TheVergeScraper()
        self.arstechnica = ArsTechnicaScraper()
        self.pypi = PyPIScraper()
        self.npm = NPMScraper()

        self.fetcher = ContentFetcher()

    def research_topic(self, topic: str, fetch_content: bool = False, get_comments: bool = True) -> Dict:
        """Comprehensive research on a specific topic"""
        print(f"\n{'='*60}")
        print(f"RESEARCHING: {topic}")
        print('='*60)

        research = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'sources': {}
        }

        # Hacker News research
        print("\n📰 Searching Hacker News...")
        hn_stories = self.hn.search_stories(topic, dateRange='month')[:10]
        research['sources']['hackernews'] = {
            'stories': hn_stories,
            'top_story_with_comments': None
        }

        if hn_stories and get_comments:
            top_story = hn_stories[0]
            print(f"   Getting comments for top story: {top_story['title'][:60]}...")
            full_story = self.hn.get_story_with_comments(top_story['id'], comment_limit=5)
            research['sources']['hackernews']['top_story_with_comments'] = full_story

        # Reddit research
        print("\n📱 Searching Reddit...")
        reddit_results = self.reddit.search_posts(topic, time='month')[:10]
        research['sources']['reddit'] = {
            'posts': reddit_results,
            'top_post_with_comments': None
        }

        if reddit_results and get_comments:
            top_post = reddit_results[0]
            print(f"   Getting comments for: {top_post['title'][:60]}...")
            post_with_comments = self.reddit.get_post_with_comments(top_post['permalink'])
            research['sources']['reddit']['top_post_with_comments'] = post_with_comments

        # OpenAI Community scraper removed (was in separate file)

        # GitHub search using API
        print("\n🔧 Searching GitHub...")
        github_repos = self.github.search_repos(topic, sort='stars', limit=10)
        research['sources']['github'] = github_repos

        # Dev.to articles
        print("\n📝 Searching Dev.to...")
        devto_articles = self.devto.search_articles(topic, per_page=10)
        research['sources']['devto'] = devto_articles

        # ArXiv papers
        print("\n📚 Searching ArXiv...")
        arxiv_papers = self.arxiv.search_papers(topic, max_results=10)
        research['sources']['arxiv'] = arxiv_papers

        # Product Hunt - BLOCKED (403 Forbidden)
        # print("\n🚀 Checking Product Hunt...")
        # product_hunt_items = self.producthunt.get_trending_products(days_ago=0, limit=10)
        # research['sources']['product_hunt'] = product_hunt_items

        # Papers with Code
        print("\n🔬 Searching Papers with Code...")
        pwc_papers = self.paperswithcode.search_papers(topic, limit=10)
        research['sources']['papers_with_code'] = pwc_papers

        # Lobste.rs stories
        print("\n🦞 Searching Lobste.rs...")
        lobsters_stories = self.lobsters.search_stories(topic, limit=10)
        research['sources']['lobsters'] = lobsters_stories

        # Stack Overflow questions
        print("\n💻 Searching Stack Overflow...")
        so_questions = self.stackoverflow.search_questions(topic, limit=10)
        research['sources']['stackoverflow'] = so_questions

        # Hugging Face models and datasets
        print("\n🤗 Searching Hugging Face...")
        hf_models = self.huggingface.search_models(topic, limit=5)
        hf_datasets = self.huggingface.get_trending_datasets(limit=5)
        research['sources']['huggingface'] = {
            'models': hf_models,
            'datasets': hf_datasets
        }

        # Hashnode - BLOCKED (GraphQL API issues)
        # print("\n📝 Searching Hashnode...")
        # hashnode_posts = self.hashnode.search_posts(topic, limit=10)
        # research['sources']['hashnode'] = hashnode_posts

        # TechCrunch articles
        print("\n📰 Searching TechCrunch...")
        tc_articles = self.techcrunch.search_articles(topic, limit=10)
        research['sources']['techcrunch'] = tc_articles

        # AngelList/Wellfound - BLOCKED (Cloudflare 403)
        # print("\n🚀 Searching AngelList/Wellfound...")
        # al_startups = self.angellist.search_startups(topic, limit=10)
        # research['sources']['angellist'] = al_startups

        # Kaggle datasets
        print("\n📊 Searching Kaggle...")
        kaggle_datasets = self.kaggle.get_trending_datasets(limit=5)
        kaggle_competitions = self.kaggle.get_competitions(limit=5)
        research['sources']['kaggle'] = {
            'datasets': kaggle_datasets,
            'competitions': kaggle_competitions
        }

        # Indie Hackers posts
        print("\n💡 Searching Indie Hackers...")
        ih_posts = self.indiehackers.get_trending_posts(limit=10)
        research['sources']['indiehackers'] = ih_posts

        # The Verge articles
        print("\n📰 Searching The Verge...")
        verge_articles = self.theverge.get_latest_articles(category="tech", limit=10)
        research['sources']['theverge'] = verge_articles

        # Ars Technica articles
        print("\n🔬 Searching Ars Technica...")
        ars_articles = self.arstechnica.get_latest_articles(limit=10)
        research['sources']['arstechnica'] = ars_articles

        # PyPI packages
        print("\n🐍 Searching PyPI...")
        pypi_packages = self.pypi.search_packages(topic, limit=10) if topic else self.pypi.get_trending_packages(limit=10)
        research['sources']['pypi'] = pypi_packages

        # npm packages
        print("\n📦 Searching npm...")
        npm_packages = self.npm.search_packages(topic, limit=10)
        research['sources']['npm'] = npm_packages

        # Fetch content from top URLs if requested
        if fetch_content and hn_stories:
            print("\n📖 Fetching article content...")
            top_urls = [s['url'] for s in hn_stories[:3] if s.get('url') and not s['url'].startswith('https://news.ycombinator.com')]
            research['fetched_content'] = []
            for url in top_urls:
                print(f"   Fetching: {url[:60]}...")
                content = self.fetcher.fetch_article_content(url)
                research['fetched_content'].append(content)

        return research

    def multi_topic_research(self, topics: List[str], **kwargs) -> Dict:
        """Research multiple topics"""
        all_research = {}
        for topic in topics:
            all_research[topic] = self.research_topic(topic, **kwargs)
        return all_research