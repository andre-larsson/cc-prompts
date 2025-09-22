# Formatting Reference

## Output Formats

### Bass Tabs Format
```
G|---------------------|
D|---------------------|
A|--3---5---7---5------|
E|---------------------|
B|---------------------|
```

### Chord Progression Overview Format
```
INTRO (4 bars):
| Am    | F     | C     | G     |

VERSE (8 bars):
| Am    | Am    | F     | F     |
| C     | G     | Am    | Am    |

CHORUS (8 bars):
| F     | C     | G     | Am    |
| F     | C     | G     | G     |

Tempo: 120 BPM
Key: C Major
Time Signature: 4/4
```

### Detailed Bass Tablature Format
```
INTRO:
G|---------------------|---------------------|
D|---------------------|---------------------|
A|--3---5---7---5------|--0---2---3---2------|
E|---------------------|---------------------|
B|---------------------|---------------------|
  Am                    F

G|---------------------|---------------------|
D|---------------------|---------------------|
A|---------------------|--0---2---3---2------|
E|--3---5---7---5------|---------------------|
B|---------------------|---------------------|
  C                     G
```

## File Header Template
Every generated .txt file should start with:
- **Metadata**: Artist, Song, Album, Year, Musicians, Bass Player, Producer, Label
- **Song Information**: Style, Tuning (Standard 5-string B-E-A-D-G), Tempo, Key, Time Signature, Length
- **Generation Notes**: Specify mode used (Complete Transcription Mode / Research-Based Mode) and rationale
- **Song Analysis**: Brief description of musical characteristics, bass playing style, and notable techniques
- **Bass Player Profile**: One paragraph about their musical background, other recordings, and playing style
- **Sources**: Primary sources, research notes, and original transcriber credit
- **Display Notes**: Must be viewed in monospace font (Courier New, Consolas, Monaco, etc.)
- **Legend**: | = measure boundary, 0 = open string, h = hammer on, p = pull off, / = slide up, \ = slide down, ~ = vibrato, PM = palm mute

## Tablature Structure Format

Each .txt file should contain these two main sections:

**SECTION 1: CHORD PROGRESSION OVERVIEW**
- Complete song structure with chord changes only
- Shows timing and measure counts for each section
- Provides roadmap for entire song
- Easy reference for quick practice or jamming

**SECTION 2: DETAILED BASS TABLATURE**
- Full bass line with specific fret positions
- Note-by-note transcription for entire song
- Includes all techniques (slides, hammer-ons, etc.)
- Follows complete song structure from beginning to end

## Formatting Guidelines
- Use UTF-8 encoding and monospace fonts
- Include clear section separators (===== lines)
- Add blank lines between song sections
- Use consistent indentation and alignment
- Verify all fret positions align across strings
- Ensure measure boundaries align properly
- **Use 4-bar layout**: 84 characters wide (4 measures × 21 characters each)
- Test display in common text editors

## Rhythm and Timing
- Use | for measure boundaries
- For chord progressions: Include tempo markings and feel descriptions (swing, straight, shuffle)
- For detailed tablature: Focus on fret positions and timing through spacing, not beat numbers
- Rhythm subdivisions can be indicated in separate performance notes if needed

## Repeat Notation
To keep tablature files concise while maintaining clarity:

### Notation Guidelines
- **Identical repeats**: Use `[Repeat Section_Name pattern]` when a section is played exactly the same
- **Repeats with count**: Use `[Play 2x]` or `[Play 4x]` above a section that should be repeated
- **Variations**: Use `[Same as Section_Name with variations on measures X-Y]` when mostly similar
- **First/second endings**: Number endings as `|1.` and `|2.` for different endings on repeats

### When to Use Repeat Notation
- Apply to both Section 1 (chord progressions) and Section 2 (detailed tablature)
- Use for verses, choruses, or other sections that repeat identically
- Use for instrumental sections that mirror vocal sections
- Always write out the first occurrence in full
- Write out any section with significant variations
- For creative interpretations, write out more sections to show variations