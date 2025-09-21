#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re


class WebScraper:
    def __init__(self, delay: float = 1.0):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay
        self.last_request_time = 0

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

    def fetch(self, url: str) -> Optional[str]:
        self._rate_limit()
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')


class HackerNewsScraper(WebScraper):
    def __init__(self):
        super().__init__(delay=0.5)
        self.base_url = "https://news.ycombinator.com"
        self.api_url = "https://hacker-news.firebaseio.com/v0"

    def get_top_stories(self, limit: int = 30) -> List[Dict]:
        stories = []

        html = self.fetch(self.base_url)
        if not html:
            return stories

        soup = self.parse_html(html)

        items = soup.select('.athing')
        for item in items[:limit]:
            story = self._parse_story_item(item, soup)
            if story:
                stories.append(story)

        return stories

    def _parse_story_item(self, item, soup) -> Optional[Dict]:
        try:
            story_id = item.get('id')

            title_elem = item.select_one('.titleline > a')
            if not title_elem:
                return None

            title = title_elem.text.strip()
            url = title_elem.get('href', '')

            if url and not url.startswith('http'):
                url = urljoin(self.base_url, url)

            domain = ''
            if url:
                parsed = urlparse(url)
                domain = parsed.netloc

            subtext = soup.find('td', class_='subtext', id=f'score_{story_id}')
            if subtext:
                parent_tr = subtext.parent
            else:
                meta_elem = item.find_next_sibling('tr')
                if meta_elem:
                    subtext = meta_elem.select_one('.subtext')

            points = 0
            comments = 0
            age = ''
            author = ''

            if subtext:
                score_elem = subtext.select_one('.score')
                if score_elem:
                    points_text = score_elem.text
                    points_match = re.search(r'(\d+)', points_text)
                    if points_match:
                        points = int(points_match.group(1))

                user_elem = subtext.select_one('.hnuser')
                if user_elem:
                    author = user_elem.text.strip()

                age_elem = subtext.select_one('.age')
                if age_elem:
                    age = age_elem.get('title', age_elem.text.strip())

                comment_links = subtext.select('a')
                for link in comment_links:
                    if 'comment' in link.text:
                        comments_match = re.search(r'(\d+)', link.text)
                        if comments_match:
                            comments = int(comments_match.group(1))
                        break

            return {
                'id': story_id,
                'title': title,
                'url': url,
                'domain': domain,
                'points': points,
                'author': author,
                'age': age,
                'comments': comments,
                'hn_url': f"{self.base_url}/item?id={story_id}" if story_id else ''
            }

        except Exception as e:
            print(f"Error parsing story item: {e}")
            return None

    def search_stories(self, query: str, sort: str = 'popularity', dateRange: str = 'week') -> List[Dict]:
        search_url = "https://hn.algolia.com/api/v1/search"

        date_filters = {
            'day': 86400,
            'week': 604800,
            'month': 2592000,
            'year': 31536000
        }

        params = {
            'query': query,
            'tags': 'story',
            'hitsPerPage': 30
        }

        if dateRange in date_filters:
            timestamp = int(time.time()) - date_filters[dateRange]
            params['numericFilters'] = f'created_at_i>{timestamp}'

        if sort == 'date':
            search_url = "https://hn.algolia.com/api/v1/search_by_date"

        try:
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            stories = []
            for hit in data.get('hits', []):
                stories.append({
                    'id': hit.get('objectID'),
                    'title': hit.get('title', ''),
                    'url': hit.get('url', ''),
                    'author': hit.get('author', ''),
                    'points': hit.get('points', 0),
                    'comments': hit.get('num_comments', 0),
                    'created_at': hit.get('created_at', ''),
                    'hn_url': f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
                })

            return stories

        except Exception as e:
            print(f"Error searching stories: {e}")
            return []

    def get_comments(self, story_id: str, limit: int = 10) -> List[Dict]:
        url = f"{self.base_url}/item?id={story_id}"
        html = self.fetch(url)
        if not html:
            return []

        soup = self.parse_html(html)
        comments = []

        comment_trees = soup.select('.comment-tree .athing.comtr')

        for comment in comment_trees[:limit]:
            parsed = self._parse_comment(comment)
            if parsed:
                comments.append(parsed)

        return comments

    def _parse_comment(self, comment_elem) -> Optional[Dict]:
        try:
            comment_id = comment_elem.get('id')

            indent_elem = comment_elem.select_one('.ind img')
            indent = 0
            if indent_elem and indent_elem.get('width'):
                indent = int(indent_elem['width']) // 40

            text_elem = comment_elem.select_one('.commtext')
            text = ''
            if text_elem:
                for br in text_elem.find_all('br'):
                    br.replace_with('\n')
                text = text_elem.get_text().strip()

            user_elem = comment_elem.select_one('.hnuser')
            author = user_elem.text.strip() if user_elem else '[deleted]'

            age_elem = comment_elem.select_one('.age')
            age = age_elem.text.strip() if age_elem else ''

            return {
                'id': comment_id,
                'author': author,
                'text': text,
                'age': age,
                'indent': indent
            }

        except Exception as e:
            print(f"Error parsing comment: {e}")
            return None


class RedditScraper(WebScraper):
    def __init__(self):
        super().__init__(delay=2.0)
        self.base_url = "https://www.reddit.com"

    def get_subreddit_posts(self, subreddit: str, sort: str = 'hot', limit: int = 25) -> List[Dict]:
        url = f"{self.base_url}/r/{subreddit}/{sort}.json"
        params = {'limit': limit, 'raw_json': 1}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            posts = []
            for child in data['data']['children']:
                post = child['data']
                posts.append({
                    'id': post['id'],
                    'title': post['title'],
                    'author': post['author'],
                    'url': post['url'],
                    'text': post.get('selftext', ''),
                    'score': post['score'],
                    'comments': post['num_comments'],
                    'created_utc': datetime.fromtimestamp(post['created_utc']).isoformat(),
                    'subreddit': post['subreddit'],
                    'permalink': f"https://reddit.com{post['permalink']}"
                })

            return posts

        except Exception as e:
            print(f"Error fetching subreddit posts: {e}")
            return []

    def search_posts(self, query: str, subreddit: Optional[str] = None, sort: str = 'relevance', time: str = 'week') -> List[Dict]:
        if subreddit:
            url = f"{self.base_url}/r/{subreddit}/search.json"
            params = {'q': query, 'restrict_sr': 'on', 'sort': sort, 't': time, 'limit': 25}
        else:
            url = f"{self.base_url}/search.json"
            params = {'q': query, 'sort': sort, 't': time, 'limit': 25}

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            posts = []
            for child in data['data']['children']:
                post = child['data']
                posts.append({
                    'id': post['id'],
                    'title': post['title'],
                    'author': post['author'],
                    'url': post['url'],
                    'score': post['score'],
                    'comments': post['num_comments'],
                    'subreddit': post['subreddit'],
                    'created_utc': datetime.fromtimestamp(post['created_utc']).isoformat(),
                    'permalink': f"https://reddit.com{post['permalink']}"
                })

            return posts

        except Exception as e:
            print(f"Error searching Reddit: {e}")
            return []


class GitHubTrendingScraper(WebScraper):
    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://github.com"
        self.api_url = "https://api.github.com"
        # Get GitHub token from environment
        import os
        self.token = os.environ.get('GITHUB_TOKEN')
        if self.token:
            self.session.headers.update({
                'Authorization': f'token {self.token}',
                'Accept': 'application/vnd.github.v3+json'
            })

    def get_trending(self, language: Optional[str] = None, since: str = 'daily') -> List[Dict]:
        if language:
            url = f"{self.base_url}/trending/{language}?since={since}"
        else:
            url = f"{self.base_url}/trending?since={since}"

        html = self.fetch(url)
        if not html:
            return []

        soup = self.parse_html(html)
        repos = []

        for article in soup.select('article.Box-row'):
            repo = self._parse_repo(article)
            if repo:
                repos.append(repo)

        return repos

    def _parse_repo(self, article) -> Optional[Dict]:
        try:
            h2 = article.select_one('h2')
            if not h2:
                return None

            repo_link = h2.select_one('a')
            repo_path = repo_link['href'].strip('/')
            owner, name = repo_path.split('/')[:2]

            description_elem = article.select_one('p')
            description = description_elem.text.strip() if description_elem else ''

            language_elem = article.select_one('[itemprop="programmingLanguage"]')
            language = language_elem.text.strip() if language_elem else ''

            stars_elem = article.select_one('svg.octicon-star').parent
            stars_text = stars_elem.text.strip()
            stars = self._parse_number(stars_text)

            forks_elem = article.select_one('svg.octicon-repo-forked')
            forks = 0
            if forks_elem:
                forks_text = forks_elem.parent.text.strip()
                forks = self._parse_number(forks_text)

            stars_today_elem = article.select_one('span.d-inline-block.float-sm-right')
            stars_today = 0
            if stars_today_elem:
                match = re.search(r'([\d,]+)\s+stars', stars_today_elem.text)
                if match:
                    stars_today = self._parse_number(match.group(1))

            return {
                'owner': owner,
                'name': name,
                'full_name': f"{owner}/{name}",
                'description': description,
                'language': language,
                'stars': stars,
                'forks': forks,
                'stars_today': stars_today,
                'url': f"{self.base_url}/{repo_path}"
            }

        except Exception as e:
            print(f"Error parsing repo: {e}")
            return None

    def _parse_number(self, text: str) -> int:
        text = text.replace(',', '').strip()
        match = re.search(r'(\d+)', text)
        if match:
            return int(match.group(1))
        return 0

    def search_repos(self, query: str, sort: str = 'stars', order: str = 'desc', limit: int = 30) -> List[Dict]:
        """Search GitHub repositories using the API
        sort: stars, forks, updated, help-wanted-issues
        order: desc, asc
        """
        url = f"{self.api_url}/search/repositories"
        params = {
            'q': query,
            'sort': sort,
            'order': order,
            'per_page': min(limit, 100)  # GitHub API max is 100
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            repos = []
            for repo in data.get('items', []):
                repos.append({
                    'owner': repo['owner']['login'],
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'description': repo.get('description', ''),
                    'url': repo['html_url'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'language': repo.get('language', ''),
                    'created_at': repo['created_at'],
                    'updated_at': repo['updated_at'],
                    'topics': repo.get('topics', []),
                    'license': repo.get('license', {}).get('spdx_id', '') if repo.get('license') else '',
                    'scraped_at': datetime.now().isoformat()
                })

            return repos

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"GitHub API rate limit exceeded. Token: {'Yes' if self.token else 'No'}")
            else:
                print(f"GitHub API error: {e}")
            return []
        except Exception as e:
            print(f"Error searching GitHub: {e}")
            return []


def export_results(data: List[Dict], filename: str, format: str = 'json'):
    if format == 'json':
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    elif format == 'csv':
        import csv
        if data:
            keys = data[0].keys()
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
    else:
        raise ValueError(f"Unsupported format: {format}")