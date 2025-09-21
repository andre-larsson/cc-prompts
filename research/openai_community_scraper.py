#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin, quote
from scraper import WebScraper


class OpenAICommunityScrapser(WebScraper):
    """Scraper for OpenAI Developer Forum (Discourse-based)"""

    def __init__(self):
        super().__init__(delay=1.0)
        self.base_url = "https://community.openai.com"
        self.api_url = f"{self.base_url}"

    def get_latest_topics(self, category: Optional[str] = None, limit: int = 30) -> List[Dict]:
        """Get latest topics from the forum"""
        if category:
            url = f"{self.base_url}/c/{category}.json"
        else:
            url = f"{self.base_url}/latest.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            topics = []
            for topic in data.get('topic_list', {}).get('topics', [])[:limit]:
                topics.append(self._parse_topic(topic))

            return topics

        except Exception as e:
            print(f"Error fetching latest topics: {e}")
            return []

    def get_top_topics(self, period: str = 'weekly', category: Optional[str] = None, limit: int = 30) -> List[Dict]:
        """Get top topics for a period (daily, weekly, monthly, yearly, all)"""
        if category:
            url = f"{self.base_url}/c/{category}/top/{period}.json"
        else:
            url = f"{self.base_url}/top/{period}.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            topics = []
            for topic in data.get('topic_list', {}).get('topics', [])[:limit]:
                topics.append(self._parse_topic(topic))

            return topics

        except Exception as e:
            print(f"Error fetching top topics: {e}")
            return []

    def search_topics(self, query: str, order: str = 'latest', limit: int = 30) -> List[Dict]:
        """Search for topics in the forum"""
        # Use the Discourse search endpoint
        url = f"{self.base_url}/search.json"
        params = {
            'q': query,
            'order': order  # latest, likes, views, latest_topic
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            topics = []
            posts = data.get('posts', [])
            topics_data = data.get('topics', [])

            # Map topics by ID for easy lookup
            topic_map = {t['id']: t for t in topics_data}

            # Process posts and group by topic
            seen_topics = set()
            for post in posts[:limit]:
                topic_id = post.get('topic_id')
                if topic_id and topic_id not in seen_topics:
                    seen_topics.add(topic_id)
                    topic_data = topic_map.get(topic_id, {})

                    topics.append({
                        'id': topic_id,
                        'title': topic_data.get('title', post.get('topic_title_headline', '')),
                        'slug': topic_data.get('slug', ''),
                        'category_id': topic_data.get('category_id'),
                        'posts_count': topic_data.get('posts_count', 0),
                        'reply_count': topic_data.get('reply_count', 0),
                        'views': topic_data.get('views', 0),
                        'like_count': topic_data.get('like_count', 0),
                        'created_at': topic_data.get('created_at', ''),
                        'last_posted_at': topic_data.get('last_posted_at', ''),
                        'url': f"{self.base_url}/t/{topic_data.get('slug', '')}/{topic_id}",
                        'excerpt': post.get('blurb', ''),
                        'username': post.get('username', ''),
                        'scraped_at': datetime.now().isoformat()
                    })

            return topics

        except Exception as e:
            print(f"Error searching topics: {e}")
            return []

    def get_topic_with_replies(self, topic_id: int, limit: int = 20) -> Dict:
        """Get a topic with its replies"""
        url = f"{self.base_url}/t/{topic_id}.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            topic = {
                'id': data.get('id'),
                'title': data.get('title', ''),
                'slug': data.get('slug', ''),
                'posts_count': data.get('posts_count', 0),
                'reply_count': data.get('reply_count', 0),
                'views': data.get('views', 0),
                'like_count': data.get('like_count', 0),
                'created_at': data.get('created_at', ''),
                'url': f"{self.base_url}/t/{data.get('slug', '')}/{topic_id}",
                'category': self._get_category_name(data.get('category_id')),
                'tags': data.get('tags', []),
                'posts': []
            }

            # Parse posts/replies
            post_stream = data.get('post_stream', {})
            posts = post_stream.get('posts', [])[:limit]

            for post in posts:
                topic['posts'].append({
                    'id': post.get('id'),
                    'username': post.get('username', ''),
                    'name': post.get('name', ''),
                    'created_at': post.get('created_at', ''),
                    'updated_at': post.get('updated_at', ''),
                    'content': post.get('cooked', ''),  # HTML content
                    'content_text': BeautifulSoup(post.get('cooked', ''), 'html.parser').get_text().strip()[:1000],
                    'reply_to_post_number': post.get('reply_to_post_number'),
                    'reply_count': post.get('reply_count', 0),
                    'like_count': post.get('like_count', 0),
                    'post_number': post.get('post_number', 0),
                    'post_type': post.get('post_type', 1),  # 1 = regular, 2 = moderator, 3 = small action
                })

            topic['scraped_at'] = datetime.now().isoformat()
            return topic

        except Exception as e:
            print(f"Error fetching topic with replies: {e}")
            return {}

    def get_categories(self) -> List[Dict]:
        """Get all forum categories"""
        url = f"{self.base_url}/categories.json"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            categories = []
            for cat in data.get('category_list', {}).get('categories', []):
                categories.append({
                    'id': cat.get('id'),
                    'name': cat.get('name'),
                    'slug': cat.get('slug'),
                    'description': cat.get('description_text', ''),
                    'topic_count': cat.get('topic_count', 0),
                    'post_count': cat.get('post_count', 0),
                    'url': f"{self.base_url}/c/{cat.get('slug')}"
                })

            return categories

        except Exception as e:
            print(f"Error fetching categories: {e}")
            return []

    def _parse_topic(self, topic_data: Dict) -> Dict:
        """Parse topic data from API response"""
        return {
            'id': topic_data.get('id'),
            'title': topic_data.get('title', ''),
            'slug': topic_data.get('slug', ''),
            'category_id': topic_data.get('category_id'),
            'posts_count': topic_data.get('posts_count', 0),
            'reply_count': topic_data.get('reply_count', 0),
            'views': topic_data.get('views', 0),
            'like_count': topic_data.get('like_count', 0),
            'created_at': topic_data.get('created_at', ''),
            'last_posted_at': topic_data.get('last_posted_at', ''),
            'bumped_at': topic_data.get('bumped_at', ''),
            'pinned': topic_data.get('pinned', False),
            'excerpt': topic_data.get('excerpt', ''),
            'visible': topic_data.get('visible', True),
            'closed': topic_data.get('closed', False),
            'archived': topic_data.get('archived', False),
            'tags': topic_data.get('tags', []),
            'url': f"{self.base_url}/t/{topic_data.get('slug', '')}/{topic_data.get('id')}",
            'scraped_at': datetime.now().isoformat()
        }

    def _get_category_name(self, category_id: Optional[int]) -> str:
        """Get category name by ID (would need caching in production)"""
        if not category_id:
            return ''

        # Common OpenAI forum categories
        category_map = {
            9: 'API',
            14: 'Prompting',
            15: 'ChatGPT',
            8: 'Developers',
            6: 'Community',
            # Add more as needed
        }

        return category_map.get(category_id, f'Category-{category_id}')


def demo_openai_community():
    """Demo OpenAI Community forum scraping"""
    print("\n" + "="*70)
    print("OPENAI COMMUNITY FORUM SCRAPING DEMO")
    print("="*70)

    scraper = OpenAICommunityScrapser()

    # Get categories
    print("\n📂 Forum Categories:")
    print("-" * 40)
    categories = scraper.get_categories()
    for cat in categories[:10]:
        print(f"- {cat['name']} ({cat['topic_count']} topics)")

    # Get latest topics
    print("\n📰 Latest Topics:")
    print("-" * 40)
    latest = scraper.get_latest_topics(limit=5)
    for topic in latest:
        print(f"\n{topic['title']}")
        print(f"  Views: {topic['views']} | Replies: {topic['reply_count']} | Likes: {topic['like_count']}")
        print(f"  Created: {topic['created_at'][:10] if topic['created_at'] else 'N/A'}")
        print(f"  URL: {topic['url']}")

    # Search for specific topics
    search_query = "GPT-4"
    print(f"\n🔍 Searching for '{search_query}':")
    print("-" * 40)
    results = scraper.search_topics(search_query, limit=5)
    for topic in results:
        print(f"\n{topic['title']}")
        print(f"  Excerpt: {topic['excerpt'][:100]}..." if len(topic['excerpt']) > 100 else f"  Excerpt: {topic['excerpt']}")

    # Get top topics this week
    print("\n🔥 Top Topics This Week:")
    print("-" * 40)
    top_topics = scraper.get_top_topics(period='weekly', limit=5)
    for topic in top_topics:
        print(f"\n{topic['title']}")
        print(f"  Views: {topic['views']} | Replies: {topic['reply_count']}")

    # Get a topic with replies
    if latest:
        topic_id = latest[0]['id']
        print(f"\n💬 Topic with Replies (ID: {topic_id}):")
        print("-" * 40)
        full_topic = scraper.get_topic_with_replies(topic_id, limit=5)

        if full_topic:
            print(f"\nTitle: {full_topic['title']}")
            print(f"Category: {full_topic['category']}")
            print(f"Tags: {', '.join(full_topic.get('tags', []))}")

            print(f"\nFirst 3 replies:")
            for i, post in enumerate(full_topic.get('posts', [])[:3], 1):
                print(f"\n  Reply {i} by {post['username']}:")
                preview = post['content_text'][:200] + "..." if len(post['content_text']) > 200 else post['content_text']
                print(f"  {preview}")
                print(f"  Likes: {post['like_count']} | Posted: {post['created_at'][:10] if post['created_at'] else 'N/A'}")

    # Save sample data
    sample_data = {
        'timestamp': datetime.now().isoformat(),
        'categories': categories[:5],
        'latest_topics': latest[:5],
        'search_results': results[:3],
        'top_weekly': top_topics[:3]
    }

    filename = f"openai_community_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(sample_data, f, indent=2, default=str)

    print(f"\n\n✅ Sample data saved to: {filename}")


if __name__ == "__main__":
    demo_openai_community()