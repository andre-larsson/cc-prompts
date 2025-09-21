#!/usr/bin/env python3

from datetime import datetime, timedelta
import time
from typing import List, Dict, Optional
from scraper import HackerNewsScraper, RedditScraper, GitHubTrendingScraper


class DateTimeEnhancedHNScraper(HackerNewsScraper):
    """HN Scraper with consistent datetime handling"""

    def get_top_stories(self, limit: int = 30) -> List[Dict]:
        """Override to add datetime parsing"""
        stories = super().get_top_stories(limit)

        for story in stories:
            # Parse age string to approximate datetime
            if 'age' in story:
                story['created_at'] = self._parse_age_to_datetime(story['age'])
            story['scraped_at'] = datetime.now().isoformat()

        return stories

    def search_stories(self, query: str, sort: str = 'popularity', dateRange: str = 'week') -> List[Dict]:
        """Enhanced search with proper datetime"""
        stories = super().search_stories(query, sort, dateRange)

        for story in stories:
            # Ensure consistent datetime format
            if 'created_at' in story and story['created_at']:
                # Already in ISO format from API
                pass
            elif story.get('created_at_i'):
                # Convert Unix timestamp if available
                story['created_at'] = datetime.fromtimestamp(story['created_at_i']).isoformat()

            story['scraped_at'] = datetime.now().isoformat()

        return stories

    def _parse_age_to_datetime(self, age_str: str) -> str:
        """Convert HN age strings like '2 hours ago' to ISO datetime"""
        now = datetime.now()

        # Parse different age formats
        if 'minute' in age_str:
            minutes = int(age_str.split()[0])
            dt = now - timedelta(minutes=minutes)
        elif 'hour' in age_str:
            hours = int(age_str.split()[0])
            dt = now - timedelta(hours=hours)
        elif 'day' in age_str:
            days = int(age_str.split()[0])
            dt = now - timedelta(days=days)
        elif 'month' in age_str:
            months = int(age_str.split()[0])
            dt = now - timedelta(days=months*30)  # Approximate
        elif 'year' in age_str:
            years = int(age_str.split()[0])
            dt = now - timedelta(days=years*365)  # Approximate
        else:
            # If we have a timestamp like "2025-09-21T03:46:07 1758426367"
            if ' ' in age_str and len(age_str.split()[0]) > 10:
                try:
                    dt = datetime.fromisoformat(age_str.split()[0])
                except:
                    dt = now
            else:
                dt = now

        return dt.isoformat()

    def get_comments(self, story_id: str, limit: int = 10) -> List[Dict]:
        """Enhanced comments with datetime"""
        comments = super().get_comments(story_id, limit)

        for comment in comments:
            if 'age' in comment:
                comment['created_at'] = self._parse_age_to_datetime(comment['age'])
            comment['scraped_at'] = datetime.now().isoformat()

        return comments


class DateTimeEnhancedRedditScraper(RedditScraper):
    """Reddit Scraper with consistent datetime handling"""

    def get_subreddit_posts(self, subreddit: str, sort: str = 'hot', limit: int = 25) -> List[Dict]:
        """Enhanced with datetime fields"""
        posts = super().get_subreddit_posts(subreddit, sort, limit)

        for post in posts:
            # Ensure we have both Unix and ISO timestamps
            if 'created_utc' in post and isinstance(post['created_utc'], str):
                # Already converted to ISO
                pass
            elif 'created_utc' in post:
                post['created_at'] = datetime.fromtimestamp(post['created_utc']).isoformat()

            post['scraped_at'] = datetime.now().isoformat()

        return posts

    def search_posts(self, query: str, subreddit: Optional[str] = None, sort: str = 'relevance', time: str = 'week') -> List[Dict]:
        """Enhanced search with datetime"""
        posts = super().search_posts(query, subreddit, sort, time)

        for post in posts:
            # Ensure consistent datetime
            if 'created_utc' in post and not isinstance(post['created_utc'], str):
                unix_time = post['created_utc']
                post['created_utc_unix'] = unix_time
                post['created_at'] = datetime.fromtimestamp(unix_time).isoformat()

            post['scraped_at'] = datetime.now().isoformat()

        return posts


class DateTimeEnhancedGitHubScraper(GitHubTrendingScraper):
    """GitHub Scraper with datetime tracking"""

    def get_trending(self, language: Optional[str] = None, since: str = 'daily') -> List[Dict]:
        """Enhanced with datetime fields"""
        repos = super().get_trending(language, since)

        # Add datetime context
        for repo in repos:
            repo['scraped_at'] = datetime.now().isoformat()

            # Add time range context
            if since == 'daily':
                repo['trending_since'] = (datetime.now() - timedelta(days=1)).isoformat()
            elif since == 'weekly':
                repo['trending_since'] = (datetime.now() - timedelta(days=7)).isoformat()
            elif since == 'monthly':
                repo['trending_since'] = (datetime.now() - timedelta(days=30)).isoformat()

            repo['trending_period'] = since

        return repos


def analyze_datetime_coverage(data: List[Dict]) -> Dict:
    """Analyze datetime field coverage in scraped data"""
    total = len(data)
    if total == 0:
        return {'total': 0, 'with_datetime': 0, 'coverage': 0}

    with_created = sum(1 for item in data if item.get('created_at') or item.get('created_utc'))
    with_scraped = sum(1 for item in data if item.get('scraped_at'))

    return {
        'total': total,
        'with_created_datetime': with_created,
        'with_scraped_datetime': with_scraped,
        'created_coverage': f"{(with_created/total)*100:.1f}%",
        'scraped_coverage': f"{(with_scraped/total)*100:.1f}%"
    }


def demo_datetime_consistency():
    """Demo showing consistent datetime handling"""
    print("\n" + "="*60)
    print("DATETIME CONSISTENCY DEMO")
    print("="*60)

    # Test HN scraper
    hn = DateTimeEnhancedHNScraper()
    print("\n📰 Hacker News - Fetching stories with datetime...")
    stories = hn.get_top_stories(limit=5)

    print("\nSample HN story with datetime:")
    if stories:
        story = stories[0]
        print(f"Title: {story['title'][:60]}...")
        print(f"Created: {story.get('created_at', 'N/A')}")
        print(f"Scraped: {story.get('scraped_at', 'N/A')}")

    # Analyze coverage
    coverage = analyze_datetime_coverage(stories)
    print(f"\nDatetime coverage: {coverage['created_coverage']} have creation time")

    # Test Reddit scraper
    reddit = DateTimeEnhancedRedditScraper()
    print("\n📱 Reddit - Fetching posts with datetime...")
    posts = reddit.get_subreddit_posts('programming', limit=5)

    print("\nSample Reddit post with datetime:")
    if posts:
        post = posts[0]
        print(f"Title: {post['title'][:60]}...")
        print(f"Created: {post.get('created_at', 'N/A')}")
        print(f"Scraped: {post.get('scraped_at', 'N/A')}")

    # Test GitHub scraper
    github = DateTimeEnhancedGitHubScraper()
    print("\n🔧 GitHub - Fetching trending with datetime context...")
    repos = github.get_trending(since='daily', language='python')

    print("\nSample GitHub repo with datetime:")
    if repos:
        repo = repos[0]
        print(f"Repo: {repo['full_name']}")
        print(f"Trending since: {repo.get('trending_since', 'N/A')}")
        print(f"Scraped: {repo.get('scraped_at', 'N/A')}")

    # Save sample with all datetime fields
    import json
    sample_data = {
        'timestamp': datetime.now().isoformat(),
        'hackernews_sample': stories[:2] if stories else [],
        'reddit_sample': posts[:2] if posts else [],
        'github_sample': repos[:2] if repos else []
    }

    filename = f"datetime_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(sample_data, f, indent=2, default=str)

    print(f"\n✅ Sample data with datetime saved to: {filename}")

    return sample_data


if __name__ == "__main__":
    demo_datetime_consistency()