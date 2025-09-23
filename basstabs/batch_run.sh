#!/bin/bash

# Check if argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <songs_file.txt> [model]"
    echo "Example: $0 songs_list.txt"
    echo "Example: $0 songs_list.txt opus"
    echo "Default model: sonnet"
    exit 1
fi

SONGS_FILE="$1"
MODEL="${2:-sonnet}"  # Default to sonnet if no model specified

# Check if file exists
if [ ! -f "$SONGS_FILE" ]; then
    echo "Error: File '$SONGS_FILE' not found."
    exit 1
fi

# Check if file is readable
if [ ! -r "$SONGS_FILE" ]; then
    echo "Error: Cannot read file '$SONGS_FILE'."
    exit 1
fi

# Create backup of original file
cp "$SONGS_FILE" "${SONGS_FILE}.backup"

# Create logs directory if it doesn't exist
mkdir -p logs

echo "Processing songs from: $SONGS_FILE"
echo "Using model: $MODEL"
echo "Backup created: ${SONGS_FILE}.backup"
echo "========================================"

# Create temporary file for processing
TEMP_FILE=$(mktemp)

# Read file line by line
line_number=0
while IFS= read -r song || [ -n "$song" ]; do
    line_number=$((line_number + 1))

    # Skip empty lines and already commented lines
    if [ -z "$(echo "$song" | tr -d '[:space:]')" ] || [[ "$song" =~ ^[[:space:]]*# ]]; then
        echo "$song" >> "$TEMP_FILE"
        continue
    fi

    echo "[$line_number] Processing: $song"

    # Format line number with leading zero (01, 02, etc.)
    formatted_number=$(printf "%02d" "$line_number")

    # Run claude command for each song with numbered filename instruction
    claude -p "create a bass tab for $song and save it with filename starting with ${formatted_number}_ (e.g., results/${formatted_number}_artist_songname.txt)" --model "$MODEL" --allowed-tools "Bash,Read,Write,Search,WebSearch,WebFetch,Fetch,Update,Edit" > "logs/log_${line_number}.log"

    if [ $? -eq 0 ]; then
        echo "[$line_number] ✓ Completed: $song"
        # Comment out the processed song
        echo "# $song" >> "$TEMP_FILE"
    else
        echo "[$line_number] ✗ Failed: $song"
        # Keep failed song uncommented for retry
        echo "$song" >> "$TEMP_FILE"
    fi

    echo "----------------------------------------"

done < "$SONGS_FILE"

# Replace original file with updated version
mv "$TEMP_FILE" "$SONGS_FILE"

echo "========================================"
echo "Batch processing complete!"
echo "Check individual log files: logs/log_*.log"
echo "----------------------------------------"
echo "Creating song summary list..."

# Create a summary of all processed songs
claude -p "Look at all the .txt files in the results/ folder and create a summary file called 'results/00_song_summary.txt' that lists all the songs with the following format for each line: [song number from filename] - Song Name by Artist (Year) - Key: [key]. Sort by the song number. Include a header 'SONG SUMMARY LIST' and today's date at the top." --model "$MODEL" --allowed-tools "Bash,Read,Write,Glob" > "logs/summary_generation.log"

if [ $? -eq 0 ]; then
    echo "✓ Summary file created: results/00_song_summary.txt"
else
    echo "✗ Failed to create summary file. Check logs/summary_generation.log"
fi

echo "========================================"
