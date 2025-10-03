# Bass Tab Generator

Generates bass tablature for songs by looking them up online and transcribing them for 5-string bass (B-E-A-D-G tuning). Creates two versions: original transcription and a creative interpretation.

## Usage

```bash
claude -p "create bass tab for [Song Name] by [Artist]"
codex -p "create bass tab for [Song Name] by [Artist]"
```

For Codex runs, pass a non-coding GPT model with `-m` (for example `codex -m gpt-4.1-mini -p "create bass tab for [Song Name] by [Artist]"`). Internal testing shows these non-coding GPT variants edge out Claude on chord-only transcriptions.

## Output

Two text files:
- `artist_songname.txt` - Original bass line transcription
- `artist_songname_claude.txt` - Creative interpretation

## Key Features

- **Original key transcription**: All tabs show actual fret positions in the song's original recorded key
- **No capo notation**: If source material uses capo, tabs are automatically transposed to show real fret positions
- **5-string bass format**: Standard B-E-A-D-G tuning
- **Complete song structure**: From intro to outro with all sections labeled

## Model Performance Note

**Important**: Model performance varies by task:
- **Chord progressions**: Work reasonably well with Opus
- **Bass tablature**: Both Sonnet and Opus struggle - results tend to be either overly simplistic (plain root notes throughout) or inaccurate
- **Codex**: Works well for chord-only progressions; run it with non-coding GPT models for the best accuracy; internal tests show these models edge out Claude on this task, though bass tabs may still need manual verification

## File Structure

Each file includes:

1. **Header**: Artist info, song details, bass player profile
2. **Chord Progression Overview**: Quick reference with chord changes
3. **Detailed Bass Tablature**: Full note-by-note transcription with techniques (slides, hammer-ons, etc.)