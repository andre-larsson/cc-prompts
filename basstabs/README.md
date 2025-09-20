# Bass Tab Generator (Personal Use)

This folder has prompts that help Claude create bass tabs for songs. When you run Claude Code here, it'll look up songs online and write out the bass lines in tab format for 5-string bass. You'll get two versions - one that matches the original and another with Claude's own take on it. Just for personal practice and learning.

## Example Usage

```bash
claude -p "create bass tab for [Song Name] by [Artist]"
```

You'll get two files:
- `artist_songname.txt` - The original bass line as played
- `artist_songname_claude.txt` - Claude's version with some creative ideas