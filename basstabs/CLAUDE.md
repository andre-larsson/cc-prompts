# Bass Tabs and Chord Progression Generator

This project creates bass tablature transcriptions and chord progressions for existing songs, from intro to end, formatted for easy playback.

## Song Structure

Transcriptions follow the actual arrangement of the original recording, which may include sections like INTRO, VERSE, PRE-CHORUS, CHORUS, BRIDGE, SOLO, BREAKDOWN, OUTRO/CODA, and INTERLUDE. Structure varies by song and artist.

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

## Generation Guidelines

### Bass Tab Guidelines
- **Always use 5-string bass tablature format (B-E-A-D-G tuning) for all songs by default**
- String names are labeled on the left (B-E-A-D-G where B is the lowest pitch and G is the highest)
- Numbers on lines represent fret positions (0 = open string)
- Include fret numbers on appropriate strings
- Focus on clear fret positions and chord labels
- Mark chord changes and song sections clearly
- Include fingering suggestions for complex passages
- Use tablature symbols for various playing techniques (see Tablature Symbols section)
- **ALWAYS present tablature in actual recorded key (remove capo transposition)**
- **NEVER include capo instructions - show real fret positions only**
- If source uses capo, add all capo frets to every fret number in tablature
- Chord notation above/below tab shows root note of chord
- Use monospace fonts to ensure proper alignment of ASCII characters
- Place chord labels clearly below tablature sections
- Use consistent spacing and dashes for visual clarity
- **Do not include beat count numbers (1 2 3 4) above or below the tablature lines**

### Chord Progression Guidelines
- Use bar lines (|) to separate measures
- Do not include beat count numbers above/below tablature lines
- Specify tempo, key, and time signature
- Show chord extensions (maj7, m7, sus4, etc.) when appropriate
- **Always include slash chords when bass note differs from chord root** (e.g., Am/G, C/E, D/F#)
- Use slash chord notation to accurately reflect the actual bass line being played
- Example: If playing Am chord but bass plays G note, write as Am/G


## Standard Workflow

### Default Process for New Tablature Requests

When asked to create bass tablature for any song, follow this standard workflow:

1. **Internet Research**
   - Search for existing bass tablature online
   - Review multiple sources (Ultimate Guitar, Songsterr, etc.)
   - Identify the most popular/highest-rated version
   - Note any playing instructions, techniques, or performance notes from these sources
   - Cross-reference different versions for accuracy
   - Research the bass player's background and discography
   - Look for information about their other recordings and collaborations

   **Converting Informal ASCII Tabs:**
   When you find high-quality tabs in informal formats (like user-submitted ASCII tabs), convert them to our structured format:
   - Extract the musical content (fret numbers, techniques, timing)
   - Determine the chord progression from the bass notes
   - Convert to 5-string bass format (B-E-A-D-G) if needed
   - Expand shortened notation (e.g., "repeat main riff" becomes full tablature)
   - Add measure bars based on time signature (every 21 characters for 4/4)
   - Include chord labels below each measure
   - Preserve special techniques (slides /, bends b, hammer-ons h, etc.)
   - Credit the original transcriber in the sources section

   Example conversion:
   ```
   Original informal tab:
   A |-------3-5--5-5--5-3-2-0-------0-2-3--3-3--3-5---

   Converted to our format:
   G|---------------------|---------------------|---------------------|---------------------|
   D|---------------------|---------------------|---------------------|---------------------|
   A|-------3-5--5-5------|--5-3-2-0------------|-------0-2-3--3-3----|--3-5----------------|
   E|---------------------|---------------------|---------------------|---------------------|
   B|---------------------|---------------------|---------------------|---------------------|
     C                     Am                    F                     G
   ```

2. **Analysis and Transposition**
   - Identify the original recorded key
   - **CRITICAL: Always check for capo usage in source material**
   - **If capo is present, transpose ALL chords and fret positions to remove capo**
   - Example: Capo 4th fret → transpose everything up 4 semitones (Am becomes C#m)
   - Show actual fret positions without capo in the tablature
   - Update key signature to reflect actual recorded pitch (not capo key)
   - Normalise tablature to the standard 5-string bass tuning (B-E-A-D-G)

3. **Generate Original Transcription**
   - **CRITICAL: Accurately transcribe the EXACT bass patterns from popular online tabs - including ALL octave jumps, chromatic runs, fills, and rhythmic variations. Simple quarter-note root patterns are ONLY acceptable if that's what the source tabs actually show.**
   - Preserve all playing techniques, fingering positions, and performance notes from source tabs
   - Start with chord progression overview, then create detailed bass tablature
   - **Use 4-bar layout**: 84 characters wide (4 measures × 21 characters each)
   - Follow original song structure and apply formatting standards
   - Save as `artist_songname.txt`

4. **Review and Quality Check**
   - Verify tablature formatting and alignment
   - Check tablature alignment and fret positions
   - Ensure measure boundaries align across all strings
   - Confirm all sections are properly labeled
   - Make any musical corrections in the .txt file

5. **Creative Interpretation (Claude Version)**
   - After completing the original transcription, create an alternate bass arrangement
   - Save as `artist_songname_claude.txt`
   - **Begin with comprehensive musical analysis before tablature:**
     - Analyze harmonic progression and key modulations
     - Identify rhythmic patterns and groove characteristics
     - Discuss melodic opportunities and counterpoint possibilities
     - Explain creative choices and arrangement decisions
     - Detail specific techniques to be employed (walking bass, ostinatos, etc.)
   - Fill in missing bass parts if none were found online, or create alternate interpretation
   - Design musical bass lines that complement the song's style and feel
   - Include different approaches: walking bass, melodic counterpoint, rhythmic variations
   - Maintain the original chord progression but explore creative bass movement


## File Naming Convention

All generated tablature files must be saved using the format:
```
artist_songname.txt          (original transcription)
artist_songname_claude.txt   (creative interpretation)
```


## Output File Formatting

To ensure proper display and formatting of generated tablature files:

### File Header Template
Every generated .txt file should start with this comprehensive header containing:
- **Metadata**: Artist, Song, Album, Year, Musicians, Bass Player, Producer, Label
- **Song Information**: Style, Tuning (Standard 5-string B-E-A-D-G), Tempo, Key, Time Signature, Length
- **Song Analysis**: Brief description of musical characteristics, bass playing style, and notable techniques
- **Bass Player Profile**: One paragraph about their musical background, other recordings, and playing style
- **Sources**: Primary sources, research notes, and original transcriber credit
- **Display Notes**: Must be viewed in monospace font (Courier New, Consolas, Monaco, etc.)
- **Legend**: | = measure boundary, 0 = open string, h = hammer on, p = pull off, / = slide up, \ = slide down, ~ = vibrato, PM = palm mute

### Tablature Structure Format

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


### Formatting Guidelines
- Use UTF-8 encoding and monospace fonts
- Include clear section separators (===== lines)
- Add blank lines between song sections
- Use consistent indentation and alignment
- Verify all fret positions align across strings
- Ensure measure boundaries align properly
- Test display in common text editors


## Rhythm and Timing

- Use | for measure boundaries
- For chord progressions: Include tempo markings and feel descriptions (swing, straight, shuffle)
- For detailed tablature: Focus on fret positions and timing through spacing, not beat numbers
- Rhythm subdivisions can be indicated in separate performance notes if needed

## Repeat Notation

To keep tablature files concise while maintaining clarity, use repeat notation for repeated sections. This applies to both Section 1 (Chord Progression Overview) and Section 2 (Detailed Bass Tablature).

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
- For creative interpretations (Claude versions), write out more sections to show variations

## Key and Scale Information

Always specify:
- Key signature
- Scale type (major, minor, modal)
- Chord function (I, vi, IV, V, etc.)
- Suggested bass note emphasis

## Tablature Format and Conventions

### Standard Bass Tablature Layout
Bass tablature uses a modified version of guitar tablature with 5 strings:
- String names are written on the left (B-E-A-D-G where B is the lowest pitch and G is the highest)
- Lines represent strings, not frets
- Numbers on lines indicate which fret to press
- Number 0 represents an open string (nut)
- This document uses pitch order convention (highest pitch string at top)

### Tablature Symbols

**Essential Playing Techniques:**
- h = hammer on, p = pull off, / = slide up, \ = slide down
- ~ or v = vibrato, b = bend string up, r = release bend
- PM = palm mute, * = natural harmonic, x = muted note
- t = tap, s = legato slide, N.C. = No chord (rest)
- Additional symbols preserved as found in source tabs