# Bass Tabs and Chord Progression Generator

This project creates bass tablature transcriptions and chord progressions for existing songs, from intro to end, formatted for easy playback.

## Common Song Structure Elements

Transcribed songs may include various sections such as:
- **Intro** - Opening section to establish the key and feel
- **Verse** - Main melodic content (typically 8-16 bars)
- **Chorus** - Hook section with memorable progression
- **Bridge** - Contrasting section for variety
- **Outro** - Ending section to conclude the song

(Note: Actual song structure will match the original recording being transcribed)

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

### Song Structure Guidelines

Generated tablature is for existing and famous songs, meaning the song structure will follow the actual arrangement of the specific song being transcribed. Structure varies significantly between songs and artists.

**Key principles:**
- Accurately reflect the original song's arrangement
- Include all sections present in the recorded version
- Label each section clearly (INTRO, VERSE, CHORUS, BRIDGE, SOLO, OUTRO, etc.)
- Note any repeats, variations, or unique structural elements
- Include bar counts for each section
- Account for any instrumental breaks, solos, or extended sections

**Common section types found in popular songs:**
- **INTRO** - Opening instrumental section
- **VERSE** - Main narrative sections (often multiple verses)
- **PRE-CHORUS** - Transitional section building to chorus
- **CHORUS** - Main hook/memorable section (often repeated)
- **BRIDGE** - Contrasting section providing variety
- **SOLO** - Instrumental solo sections
- **BREAKDOWN** - Stripped-down sections
- **OUTRO/CODA** - Closing section
- **INTERLUDE** - Instrumental connecting sections

The exact structure, section lengths, and arrangement will match the original recording being transcribed.

## Standard Workflow

### Default Process for New Tablature Requests

When asked to create bass tablature for any song, follow this standard workflow:

1. **Internet Research**
   - Search for existing bass tablature online
   - Review multiple sources (Ultimate Guitar, Songsterr, etc.)
   - Cross-reference different versions for accuracy
   - Research the bass player's background and discography
   - Look for information about their other recordings and collaborations

2. **Analysis and Transposition**
   - Identify the original recorded key
   - **CRITICAL: Always check for capo usage in source material**
   - **If capo is present, transpose ALL chords and fret positions to remove capo**
   - Example: Capo 4th fret → transpose everything up 4 semitones (Am becomes C#m)
   - Show actual fret positions without capo in the tablature
   - Update key signature to reflect actual recorded pitch (not capo key)
   - Normalise tablature to the standard 5-string bass tuning (B-E-A-D-G)

3. **Generate Tablature**
   - Start with simple chord progression overview for entire song
   - Then create detailed bass tablature with specific fret positions
   - **Use 4-bar layout**: Group tablature into 4-measure lines (84 characters wide = 4 measures × 21 characters each)
   - Include chord progressions with proper timing
   - Follow song structure from original recording
   - Apply all formatting standards (monospace, alignment, etc.)
   - Ensure each measure is exactly 21 characters wide for optimal display
   - Focus solely on musical accuracy and alignment
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

### Workflow Expectations

**By default, every tablature request should:**
- Follow the 5-step workflow above
- Present music in original recorded key (no capo)
- Generate plain text .txt file (pure tablature)
- Create Claude interpretation version (.txt)
- Review the output from each step and fix any issues before continuing to ensure accuracy

## File Naming Convention

All generated tablature files must be saved using the format:
```
artist_songname.txt          (original transcription)
artist_songname_claude.txt   (creative interpretation)
```


## Output File Formatting

To ensure proper display and formatting of generated tablature files:

### File Header Template
Every generated .txt file should start with this header:
```
================================================================================
BASS TABLATURE
================================================================================
Artist: [Artist Name]
Song: [Song Title]
Album: [Album Name] (or "Not available" if unknown)
Year: [Release Year] (or "Not available" if unknown)
Musicians: [Band members/session musicians] (or "Not available" if unknown)
Bass Player: [Bass player name] (or "Not available" if unknown)
Producer: [Producer name] (or "Not available" if unknown)
Label: [Record label] (or "Not available" if unknown)

SONG INFORMATION:
Style: [Genre/Musical style]
Tuning: Standard 5-string (B-E-A-D-G)
Tempo: [BPM] (or "Not available" if unknown)
Key: [Key Signature]
Time Signature: [Time Sig]
Song Length: [Duration] (or "Not available" if unknown)

SONG ANALYSIS:
[Brief description of the song's musical characteristics, bass playing style,
notable techniques used, and any interesting musical elements. Discuss the
bass line's role in the song, whether it's melodic, rhythmic, or supportive.
Mention any distinctive features or challenges for players.]

BASS PLAYER PROFILE:
[Research the bass player and write approximately one paragraph about their
musical background. Include information about other notable records they've
played on, collaborations with other artists, whether they play other instruments,
their signature playing style, influences, and any other interesting biographical
or musical information. Mention their role in the band/session and how their
playing style contributes to this particular song. If bass player information
is not available, write "Bass player information not available."]

SOURCES AND REFERENCES:
**Primary Sources:**
- Source Name: Description of what was obtained
  URL: [URL if applicable]

**Research Notes:**
- Key findings and verification details
- Any conflicting information and resolution
- Musician credits with source verification

IMPORTANT DISPLAY NOTES:
- View this file in a monospace font (Courier New, Consolas, Monaco, etc.)
- Ensure font size allows proper character alignment
- Disable text wrapping for best results
- Tab characters may need adjustment based on your text editor

LEGEND:
| = measure boundary
0 = open string
h = hammer on
p = pull off
/ = slide up
\ = slide down
~ = vibrato
PM = palm mute

================================================================================
```

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

Example structure:
```
================================================================================
SECTION 1: CHORD PROGRESSION OVERVIEW
================================================================================
[Chord progression content here]

================================================================================
SECTION 2: DETAILED BASS TABLATURE
================================================================================
[Full bass tablature content here]
```

### Formatting Guidelines

**For .txt files:**
- Use UTF-8 encoding to ensure compatibility
- Include clear section separators (===== lines)
- Add blank lines between song sections for readability
- Use consistent indentation for chord progressions
- Include measure numbers every 4-8 bars for navigation
- Add performance notes and tempo changes where relevant

### Quality Assurance
Before saving files:
- Verify pure tablature content and alignment
- Check that all fret positions are properly aligned
- Ensure measure boundaries align across all strings
- Test display in common text editors (Notepad++, VS Code, TextEdit)
- Confirm monospace font requirement is clearly stated


## Rhythm and Timing

- Use | for measure boundaries
- For chord progressions: Include tempo markings and feel descriptions (swing, straight, shuffle)
- For detailed tablature: Focus on fret positions and timing through spacing, not beat numbers
- Rhythm subdivisions can be indicated in separate performance notes if needed

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

### ASCII Alignment Guidelines
To ensure proper tablature display:
- Use monospace fonts (Courier New, Consolas, Monaco, etc.)
- Maintain consistent character spacing throughout
- Align vertical elements (bar lines, rhythm notation) precisely
- Use hyphens (-) for empty fret positions
- Use pipe symbols (|) for string lines and measure boundaries
- Ensure rhythm notation aligns directly under corresponding tab positions
- Test display in multiple monospace environments
- Use consistent spacing between sections and measures

### Tablature Symbols

Tablature uses various symbols to denote playing techniques. Common symbols include:

### Playing Techniques
| Symbol | Technique |
|--------|-----------|
| h | hammer on |
| p | pull off |
| b | bend string up |
| r | release bend |
| / | slide up |
| \ | slide down |
| v | vibrato (sometimes written as ~) |
| t | right hand tap |
| s | legato slide |
| S | shift slide |
| * | natural harmonic |
| [n] | artificial harmonic |
| n(n) | tapped harmonic |
| tr | trill |
| T | tap |
| TP | tremolo picking |
| PM | palm muting (also written as _ and .) |
| N.C. | No chord: tacet or rest |
| \n/ | tremolo arm dip; n = amount to dip |
| \n | tremolo arm down |
| n/ | tremolo arm up |
| /n\ | tremolo arm inverted dip |
| = | hold bend; also acts as connecting device for hammers/pulls |
| <> | volume swell (louder/softer) |
| x | on rhythm slash represents muted slash |
| o | on rhythm slash represents single note slash |
| ·/. | pick slide |

### Note Length Symbols
| Symbol | Note Length |
|--------|-------------|
| W | Whole note/semibreve |
| H | Half note/minim |
| Q | Quarter note/crotchet |
| E | Eighth note/quaver |
| a | Acciaccatura |
| - | Note tied to previous |
| . | Note dotted |