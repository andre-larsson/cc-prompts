# TODO - Additional Data Sources for Research Scraper

## Developer/Tech Communities
- [x] **Lobste.rs** - High-quality tech discussions, curated community ✅
- [x] **Dev.to** - Developer articles and tutorials ✅
- [x] **Stack Overflow** - Q&A, trending questions, tagged topics ✅
- [x] ~~**Hashnode** - Developer blogs and publications~~ ❌ BLOCKED (GraphQL API issues)
- [ ] **Discord/Slack communities** - Via their public APIs where available

## AI/ML Specific
- [x] **Hugging Face** - Models, datasets, discussions, papers ✅
- [x] **Papers with Code** - Latest ML papers with implementations ✅
- [x] **ArXiv** - Preprint papers (CS, AI categories) ✅
- [ ] **Google Scholar** - Academic citations and trends
- [ ] **Replicate** - AI model marketplace and discussions

## News/Trends
- [x] **TechCrunch** - Startup and tech news ✅
- [x] **The Verge** - Tech journalism ✅
- [x] **Ars Technica** - In-depth technical articles ✅
- [x] ~~**Product Hunt** - New products and launches~~ ❌ BLOCKED (403 Forbidden)
- [x] **Indie Hackers** - Startup discussions and insights ✅
- [x] ~~**AngelList** - Startup jobs, investments, companies~~ ❌ BLOCKED (Cloudflare 403)

## Code/Projects
- [ ] **GitLab** - Open source projects
- [ ] **Codeberg** - FOSS alternative to GitHub
- [x] **npm/PyPI** - Package registries for trends ✅
- [ ] **crates.io** - Rust package registry
- [ ] **Observable** - Data visualization notebooks
- [x] **Kaggle** - Datasets, competitions, notebooks ✅

## Social/Real-time
- [ ] **Twitter/X** - Via API for tech influencers, trending topics
- [ ] **Mastodon** - Decentralized tech communities
- [ ] **LinkedIn** - Professional insights (limited API)
- [ ] **Bluesky** - Growing tech community

## Video/Multimedia
- [ ] **YouTube** - Tech channels, conference talks (via API)
- [ ] **Twitch** - Live coding streams, tech talks

## Specialized Forums
- [ ] **LessWrong** - Rationality, AI safety discussions
- [ ] **EleutherAI Discord** - Open source AI research
- [ ] **MLOps Community** - Production ML discussions
- [ ] **r/LocalLLaMA** - Local AI/LLM developments (already have Reddit, but specialized)

## Priority Implementations
✅ Completed:
1. **ArXiv** - For academic papers ✅
2. **Dev.to** - For developer articles ✅
3. **Papers with Code** - For ML implementations ✅
4. **Lobste.rs** - High-quality discussions ✅
5. ~~**Product Hunt** - New products~~ ❌ BLOCKED

✅ Completed (Round 2):
1. **Stack Overflow** - For technical Q&A ✅
2. **Hugging Face** - For AI/ML research ✅
3. ~~**Hashnode** - Developer articles~~ ❌ BLOCKED
4. **TechCrunch** - For startup news ✅
5. ~~**AngelList** - Startup data~~ ❌ BLOCKED

✅ Completed (Round 3):
1. **Kaggle** - For datasets and competitions ✅
2. **Indie Hackers** - Startup discussions ✅
3. **The Verge** - Tech journalism ✅
4. **Ars Technica** - Technical articles ✅
5. **PyPI** - Python packages ✅
6. **npm** - JavaScript packages ✅

🔄 Next priorities:
1. **Google Scholar** - Academic citations
2. **Replicate** - AI model marketplace
3. **Observable** - Data visualization notebooks
4. **LessWrong** - Rationality, AI safety discussions

## Implementation Notes
- Consider rate limiting and API keys where required
- Some sources may need authentication
- Prioritize sources with public APIs or RSS feeds
- Consider caching strategies for frequently accessed data

## Blocked Sources (Attempted but Failed)
These sources were implemented but are blocked by anti-scraping measures:
- **Product Hunt** - Cloudflare 403 Forbidden
- **Hashnode** - GraphQL API authentication issues
- **AngelList/Wellfound** - Cloudflare protection, requires browser automation

To access these sources, would need:
- Browser automation (Selenium/Playwright)
- Official API keys
- Proxy rotation services