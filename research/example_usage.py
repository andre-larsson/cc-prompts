#!/usr/bin/env python3

from scraper import HackerNewsScraper, RedditScraper, GitHubTrendingScraper, export_results
import json


def main():
    print("=" * 60)
    print("Web Scraper Examples")
    print("=" * 60)

    print("\n1. HACKER NEWS SCRAPING")
    print("-" * 40)
    hn = HackerNewsScraper()

    print("\nFetching top stories...")
    top_stories = hn.get_top_stories(limit=10)

    print(f"\nTop {len(top_stories)} stories on Hacker News:")
    for i, story in enumerate(top_stories[:5], 1):
        print(f"\n{i}. {story['title']}")
        print(f"   Points: {story['points']} | Comments: {story['comments']}")
        print(f"   URL: {story['url'][:70]}..." if len(story['url']) > 70 else f"   URL: {story['url']}")

    print("\nSearching for 'AI agents' in the past week...")
    ai_stories = hn.search_stories("AI agents", dateRange="week")
    print(f"Found {len(ai_stories)} stories about AI agents")

    if ai_stories:
        print("\nTop 3 results:")
        for story in ai_stories[:3]:
            print(f"- {story['title']} ({story['points']} points)")

    export_results(top_stories, "hn_top_stories.json")
    print("\nExported top stories to hn_top_stories.json")

    print("\n" + "=" * 60)
    print("2. REDDIT SCRAPING")
    print("-" * 40)
    reddit = RedditScraper()

    print("\nFetching r/MachineLearning hot posts...")
    ml_posts = reddit.get_subreddit_posts("MachineLearning", sort="hot", limit=10)

    print(f"\nTop posts from r/MachineLearning:")
    for post in ml_posts[:5]:
        print(f"\n- {post['title']}")
        print(f"  Score: {post['score']} | Comments: {post['comments']}")

    print("\nSearching Reddit for 'LangChain' in the past month...")
    langchain_posts = reddit.search_posts("LangChain", time="month")
    print(f"Found {len(langchain_posts)} posts about LangChain")

    export_results(ml_posts, "reddit_ml_posts.json")
    print("\nExported Reddit posts to reddit_ml_posts.json")

    print("\n" + "=" * 60)
    print("3. GITHUB TRENDING")
    print("-" * 40)
    github = GitHubTrendingScraper()

    print("\nFetching trending Python repos (this week)...")
    python_repos = github.get_trending(language="python", since="weekly")

    print(f"\nTop trending Python repositories:")
    for repo in python_repos[:5]:
        print(f"\n- {repo['full_name']}")
        print(f"  ⭐ {repo['stars']:,} stars | {repo['stars_today']} stars today")
        if repo['description']:
            desc = repo['description'][:100] + "..." if len(repo['description']) > 100 else repo['description']
            print(f"  {desc}")

    print("\nFetching all trending repos (today)...")
    all_repos = github.get_trending(since="daily")

    languages = {}
    for repo in all_repos:
        lang = repo['language'] or 'Unknown'
        languages[lang] = languages.get(lang, 0) + 1

    print(f"\nLanguage distribution in today's trending:")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {lang}: {count} repos")

    export_results(python_repos, "github_trending_python.json")
    print("\nExported GitHub trending to github_trending_python.json")

    print("\n" + "=" * 60)
    print("Research data exported to JSON files!")
    print("You can now analyze the data for trends and insights.")


if __name__ == "__main__":
    main()