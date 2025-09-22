# CLAUDE.md

Instructions for Claude Code when conducting research on specific topics.

## Purpose

This folder is for deep-dive research on emerging technologies and trends. When asked to research a topic (e.g., agentic AI), follow these steps to gather comprehensive, up-to-date information.

## Quick Start - Using the Scraper Tools

### Setup
```bash
# Create and activate virtual environment
python3 -m venv test_env
source test_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set GitHub token (optional but recommended)
export GITHUB_TOKEN="your_token_here"
```

### Available Data Sources (16 Working Scrapers)

#### Core Sources
- **Hacker News** - Tech news, discussions, trending topics
- **Reddit** - Subreddit posts, community discussions
- **GitHub** - Trending repos, code search (API-based)

#### Developer Communities
- **Dev.to** - Developer articles and tutorials
- **Stack Overflow** - Q&A, trending questions
- **Lobste.rs** - Curated tech discussions
- **Indie Hackers** - Startup insights and discussions

#### AI/ML Research
- **ArXiv** - Academic papers and preprints
- **Papers with Code** - ML papers with implementations
- **Hugging Face** - Models, datasets, spaces
- **Kaggle** - Datasets, competitions, notebooks

#### Tech News
- **TechCrunch** - Startup and tech news
- **The Verge** - Consumer tech journalism
- **Ars Technica** - In-depth technical articles

#### Package Registries
- **PyPI** - Python package trends
- **npm** - JavaScript package ecosystem

### Usage Examples

#### 1. Basic Topic Research
```python
from enhanced_scraper import ResearchAggregator

# Initialize aggregator
aggregator = ResearchAggregator()

# Research a topic across all sources
research = aggregator.research_topic(
    "agentic AI",
    fetch_content=True,  # Get article content
    get_comments=True    # Extract top comments
)
```

#### 2. Search Specific Sources
```python
# Search academic papers
from additional_scrapers import ArXivScraper
arxiv = ArXivScraper()
papers = arxiv.search("large language models", category="cs.AI", max_results=20)

# Search Stack Overflow
from additional_scrapers_v2 import StackOverflowScraper
so = StackOverflowScraper()
questions = so.search_questions("langchain agents", sort="votes")

# Search npm packages
from additional_scrapers_v3 import NPMScraper
npm = NPMScraper()
packages = npm.search_packages("ai agent", limit=15)
```

#### 3. Get Trending Content
```python
# GitHub trending repos
from scraper import GitHubTrendingScraper
github = GitHubTrendingScraper()
repos = github.get_trending(language="python", since="weekly")

# Hacker News top stories
from scraper import HackerNewsScraper
hn = HackerNewsScraper()
stories = hn.get_top_stories(limit=30)
```

### Available Scripts

1. **Basic demo**: `python3 example_usage.py`
   - Shows basic usage of HN, Reddit, GitHub scrapers

2. **Full research**: `python3 research_demo.py`
   - Comprehensive topic research with all sources
   - Includes comment extraction and content fetching

### Output Format

All scrapers return standardized data with:
- **Title/Name** - Item title or package name
- **URL** - Link to original source
- **Score/Stars** - Popularity metrics
- **Author** - Creator username
- **Created/Updated** - ISO format timestamps
- **Scraped_at** - When data was collected

Results are saved to timestamped JSON files in the `research_results/` directory.

## Research Process

### 1. Initial Landscape Scan
- Search for "[topic] 2024 2025 state of the art"
- Look for recent survey papers, overview articles, and industry reports
- Find key conferences, workshops, and communities focused on the topic

### 2. Identify Current Trends
- Search for "[topic] trends 2025" and "[topic] latest developments"
- Look at recent GitHub trending repositories related to the topic
- Check recent discussions on Hacker News, Reddit (r/MachineLearning, topic-specific subreddits)
- Find recent blog posts from major tech companies and research labs

### 3. Tools and Frameworks
- Search for "[topic] tools frameworks libraries"
- Look for GitHub awesome lists (e.g., "awesome-agentic-ai")
- Identify the most starred/forked repositories in the space
- Check package registries (PyPI, npm) for popular libraries

### 4. Key Players and Thought Leaders
- Identify leading researchers and practitioners
- Find active Twitter/X accounts discussing the topic
- Look for popular YouTube channels and podcasts
- Identify companies and startups working in this space

### 5. Academic Research
- Search for recent papers on arXiv, Google Scholar
- Look for papers from top conferences (NeurIPS, ICML, ICLR, etc.)
- Identify seminal papers and breakthrough research

### 6. Practical Applications
- Search for "[topic] use cases" and "[topic] applications"
- Look for case studies and implementation examples
- Find production deployments and real-world results

### 7. Community Discussions
- Check recent discussions on technical forums
- Look for Discord servers and Slack communities
- Find relevant newsletters and substacks

### 8. Challenges and Limitations
- Search for "[topic] challenges limitations problems"
- Look for critical perspectives and debates
- Identify open problems and research directions

## Output Format

Organize findings into these sections:

1. **Executive Summary** - 3-5 key takeaways
2. **Current State** - Where the field stands today
3. **Major Trends** - What's emerging/changing
4. **Key Tools & Technologies** - Most important frameworks/libraries
5. **Leading Organizations** - Companies, labs, researchers
6. **Hot Topics** - What people are discussing now
7. **Resources** - Must-read papers, repos, communities
8. **Future Directions** - Where the field is heading

## Search Strategies

- Use time-bounded searches (e.g., "after:2024")
- Combine multiple search terms for comprehensive coverage
- Cross-reference findings across multiple sources
- Prioritize recent information (last 3-6 months)
- Look for both academic and industry perspectives

## Quality Indicators

Focus on sources that are:
- Recently updated (within last 6 months)
- Highly cited or referenced
- From recognized authorities
- Backed by implementation/code
- Discussed across multiple communities

## Example Queries

For researching "agentic AI":
- "agentic AI frameworks 2025"
- "autonomous agents LLM tools"
- "multi-agent systems latest research"
- "AI agents production deployment"
- "LangChain CrewAI AutoGen comparison"
- "agentic workflows best practices"

## Remember

- Cast a wide net initially, then focus on high-signal sources
- Balance academic rigor with practical applications
- Look for convergent evidence across multiple sources
- Identify both hype and legitimate breakthroughs
- Track evolution of terminology and concepts

## Troubleshooting

### Common Issues

1. **GitHub API rate limit**: Set `GITHUB_TOKEN` environment variable
2. **Blocked scrapers**: Some sites (Product Hunt, Hashnode, Wellfound) require browser automation
3. **Missing dependencies**: Run `pip install -r requirements.txt` in virtual environment
4. **Timeout errors**: Increase delay between requests or reduce batch size

### Blocked Sources

The following sources were attempted but are blocked by anti-scraping measures:
- **Product Hunt** - Cloudflare 403 Forbidden
- **Hashnode** - GraphQL API authentication issues
- **AngelList/Wellfound** - Cloudflare protection

For these sources, consider:
- Using official APIs with authentication
- Browser automation tools (Selenium/Playwright)
- Alternative data sources with similar information