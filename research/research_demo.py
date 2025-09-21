#!/usr/bin/env python3

from enhanced_scraper import ResearchAggregator, EnhancedHackerNewsScraper, EnhancedRedditScraper, ContentFetcher
import json
from datetime import datetime


def demo_topic_research():
    """Demo: Research specific topics with comments and content"""
    print("\n" + "="*70)
    print("ENHANCED RESEARCH DEMO - TOPIC SEARCH WITH COMMENTS & CONTENT")
    print("="*70)

    aggregator = ResearchAggregator()

    # Research a specific topic (e.g., "agentic AI")
    topic = "agentic AI"
    print(f"\nResearching: {topic}")

    research = aggregator.research_topic(
        topic,
        fetch_content=True,  # Fetch actual article content
        get_comments=True    # Get top comments from discussions
    )

    # Display results
    print("\n" + "-"*50)
    print("RESEARCH SUMMARY")
    print("-"*50)

    # Hacker News results
    if research['sources']['hackernews']['stories']:
        print(f"\n📰 HACKER NEWS - Top 3 stories about '{topic}':")
        for i, story in enumerate(research['sources']['hackernews']['stories'][:3], 1):
            print(f"\n{i}. {story['title']}")
            print(f"   Points: {story['points']} | Comments: {story['comments']}")
            print(f"   URL: {story['url'][:70]}...")

        # Show top comments from best story
        top_story = research['sources']['hackernews'].get('top_story_with_comments')
        if top_story and top_story.get('comments'):
            print(f"\n   💬 Top comments on '{top_story['title'][:60]}...':")
            for j, comment in enumerate(top_story['comments'][:3], 1):
                comment_preview = comment['text'][:200] + "..." if len(comment['text']) > 200 else comment['text']
                print(f"\n   Comment {j} by {comment['author']}:")
                print(f"   {comment_preview}")
                if comment.get('replies', 0) > 0:
                    print(f"   ({comment['replies']} replies)")

    # Reddit results
    if research['sources']['reddit']['posts']:
        print(f"\n\n📱 REDDIT - Top posts about '{topic}':")
        for post in research['sources']['reddit']['posts'][:3]:
            print(f"\n- {post['title']}")
            print(f"  r/{post['subreddit']} | Score: {post['score']} | Comments: {post['comments']}")

        # Show top comments
        top_post = research['sources']['reddit'].get('top_post_with_comments')
        if top_post and top_post.get('top_comments'):
            print(f"\n   💬 Top comments on Reddit post:")
            for comment in top_post['top_comments'][:2]:
                comment_preview = comment['text'][:150] + "..." if len(comment['text']) > 150 else comment['text']
                print(f"\n   {comment['author']} ({comment['score']} points):")
                print(f"   {comment_preview}")

    # Fetched article content
    if research.get('fetched_content'):
        print(f"\n\n📖 ARTICLE CONTENT (from top links):")
        for content in research['fetched_content'][:2]:
            if 'error' not in content:
                print(f"\n   Title: {content['title'][:80]}...")
                print(f"   Word count: {content['word_count']}")
                if content.get('description'):
                    print(f"   Description: {content['description'][:150]}...")
                if content.get('content_preview'):
                    preview = content['content_preview'][:300] + "..." if len(content['content_preview']) > 300 else content['content_preview']
                    print(f"\n   Preview:\n   {preview}")

    # Save to JSON
    filename = f"research_{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(research, f, indent=2, default=str)
    print(f"\n\n✅ Full research saved to: {filename}")


def demo_multi_topic_search():
    """Demo: Search multiple topics across platforms"""
    print("\n" + "="*70)
    print("MULTI-TOPIC SEARCH DEMO")
    print("="*70)

    # Search for multiple AI-related topics
    topics = ["LLM agents", "RAG systems", "prompt engineering"]

    # Hacker News multi-topic search
    hn = EnhancedHackerNewsScraper()
    print("\n📰 Searching Hacker News for multiple topics...")
    hn_results = hn.search_topics(topics, dateRange='week', limit=5)

    for topic, stories in hn_results.items():
        print(f"\n{topic}: {len(stories)} stories found")
        if stories:
            top_story = stories[0]
            print(f"  Top story: {top_story['title'][:60]}... ({top_story['points']} points)")

    # Reddit multi-topic search across subreddits
    reddit = EnhancedRedditScraper()
    subreddits = ['MachineLearning', 'LocalLLaMA', 'artificial']

    print("\n📱 Searching Reddit across multiple subreddits...")
    reddit_results = reddit.search_multiple_topics(topics[:2], subreddits=subreddits, time='week', limit=3)

    for topic, subreddit_results in reddit_results.items():
        print(f"\n{topic}:")
        for subreddit, posts in subreddit_results.items():
            if posts:
                print(f"  r/{subreddit}: {len(posts)} posts")
                print(f"    Top: {posts[0]['title'][:50]}... ({posts[0]['score']} points)")


def demo_content_fetching():
    """Demo: Fetch and analyze article content"""
    print("\n" + "="*70)
    print("CONTENT FETCHING DEMO")
    print("="*70)

    fetcher = ContentFetcher()

    # Example URLs to fetch
    urls = [
        "https://openai.com/blog",  # Will fetch whatever is on OpenAI's blog
        "https://arxiv.org/abs/2301.04467"  # Example arXiv paper
    ]

    print("\n📖 Fetching content from URLs...")
    for url in urls:
        print(f"\nFetching: {url}")
        content = fetcher.fetch_article_content(url)

        if 'error' not in content:
            print(f"Title: {content.get('title', 'N/A')[:80]}")
            print(f"Word count: {content.get('word_count', 0)}")
            if content.get('author'):
                print(f"Author: {content['author']}")
            if content.get('description'):
                print(f"Description: {content['description'][:150]}...")
        else:
            print(f"Error: {content['error']}")


def main():
    print("\n" + "="*70)
    print("ENHANCED WEB SCRAPER - DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows:")
    print("1. Topic research with comments and content fetching")
    print("2. Multi-topic search across platforms")
    print("3. Article content extraction")

    # Run demos
    demo_topic_research()
    # demo_multi_topic_search()  # Uncomment to run
    # demo_content_fetching()     # Uncomment to run

    print("\n" + "="*70)
    print("DEMO COMPLETE!")
    print("="*70)


if __name__ == "__main__":
    main()