#!/bin/bash

# Help function
show_help() {
    echo "Usage: $0 -o OUTPUT_DIR [OPTIONS]"
    echo "Options:"
    echo "  -o, --output    Specify the download directory"
    echo "  -h, --help      Show this help message"
}

# Default output directory
OUTDIR="$HOME/Downloads/"

# Parse parameters
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -o|--output) OUTDIR="$2"; shift ;;
        -h|--help) show_help; exit 0 ;;
        *) items+=("$1") ;;  # Collect other parameters
    esac
    shift
done

# Validate output directory
if [[ -z "$OUTDIR" || ! -d "$OUTDIR" ]]; then
    echo "Error: The directory '$OUTDIR' does not exist."
    exit 1
fi

# Loop through other parameters and execute command
for item in "${items[@]}"; do
   which yt-dlp > /dev/null && yt-dlp --ignore-errors -f "bestvideo[height<=1080]+bestaudio/best[height<=480]" --remux-video mp4 \
        --output '%(title)s.%(ext)s' --paths "$OUTDIR" "$item" || python3 pip-universal-wrapper.py --exec yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=480]" --remux-video mp4 \
        --output '%(title)s.%(ext)s' --paths "$OUTDIR" "$item"
done
