# UNDERCOVER FALLOUT - Episode Production Workflow

## Overview
This document outlines the complete workflow for producing and publishing episodes to undercoverfallout.com. The process is designed to minimize manual work - you handle the creative discussions and final decisions, Claude handles the technical production.

---

## Your Role (Human)
1. Have discussions with Claude on topics you want to explore
2. Upload conversations to NotebookLM and generate audio
3. Download the .m4a audio file when ready
4. Tell Claude "episode ready" with episode number
5. Pick your favorite title from generated options
6. Paste the Gemini prompt and download the cover image
7. Approve final episode before GitHub push

## Claude's Role (AI Assistant)
1. Transcribe the audio file
2. Generate edgy title options based on transcript
3. Generate Gemini 3 image prompt for cover art
4. Rename audio file with chosen title
5. Compress and convert audio to MP4 (under 100MB for GitHub)
6. Create episode summary
7. Organize files into episode subfolder
8. Update index.html with new episode
9. Push to GitHub

---

## Folder Structure

```
undercover-fallout/
├── index.html                 # Main website
├── CNAME                      # Domain config
├── WORKFLOW-PROCESS.md        # This document
├── episodes/
│   ├── 001-Episode-Title/
│   │   ├── Episode-001-Title.mp4        # Video file (for embeds/backup)
│   │   ├── Episode-001-Title.m4a        # Audio file (USED BY WEBSITE PLAYER)
│   │   ├── episode-001-cover.png        # Cover art
│   │   ├── episode-001-transcript.txt   # Full transcript
│   │   └── episode-001-summary.txt      # Episode summary
│   ├── 002-Episode-Title/
│   │   └── ...
│   └── ...
├── archive/                   # Old site files (reference)
└── tools/                     # Production scripts
    ├── transcribe_audio.py
    ├── generate_title.py
    ├── generate_cover_prompt.py
    └── convert_to_mp4.py
```

---

## Step-by-Step Process

### Phase 1: Content Creation (You)
1. Discuss topics with Claude (or other AI)
2. Upload conversation to NotebookLM
3. Generate audio podcast
4. Download .m4a file to Downloads folder

### Phase 2: Production (Tell Claude "Episode X is ready")

**Claude will automatically:**

1. **Transcribe Audio**
   - Uses Google Speech Recognition API
   - Splits into 30-second chunks for accuracy
   - Output: `episode-XXX-transcript.txt`

2. **Generate Title Options**
   - Analyzes transcript for key themes
   - Creates 10+ edgy title options
   - You pick your favorite

3. **Generate Cover Art Prompt**
   - Creates Gemini 3 prompt based on transcript
   - You paste into Gemini and download image

4. **Convert to MP4**
   - Combines audio + cover image
   - Compresses to under 100MB (GitHub limit)
   - Uses ffmpeg with optimized settings

5. **Organize Files**
   - Creates episode subfolder
   - Moves all assets into organized structure
   - Renames files with episode title

6. **Create Summary**
   - Writes episode description
   - Generates tags
   - Lists key topics

### Phase 3: Publishing (Claude)

7. **Update Website**
   - Adds episode to index.html episodes array
   - IMPORTANT: Use .m4a file path (not .mp4) - the audio player doesn't support mp4 video
   - Links to cover art, transcript

8. **Push to GitHub**
   - Commits all changes
   - Pushes to origin/master
   - Site auto-deploys to undercoverfallout.com

---

## Quick Commands

When starting a new episode, just tell Claude:
- "Episode X is ready in Downloads"
- Claude will find the latest .m4a file and start the process

When reviewing options:
- "I like title #3" - Claude will use that title
- "Generate more titles focused on [theme]" - Claude will create more options

When cover is ready:
- "Cover image is downloaded" - Claude will find it and continue

---

## Technical Notes

### Audio Compression
- Original .m4a files are ~65-70MB for 35-min episodes
- MP4 output compressed to ~50-80MB (under GitHub 100MB limit)
- Settings: CRF 28, AAC 128k, fast preset

### Transcription
- Uses free Google Speech Recognition API
- 30-second chunks for API limits
- ~5 minutes to transcribe 35-min episode

### GitHub Limits
- Max file size: 100MB
- If episode exceeds limit, ffmpeg compression is increased

---

## Resuming Work

If conversation is interrupted, tell Claude:
- "Let's continue with the undercover fallout workflow"
- Provide context: "We were on Episode X, [last step completed]"
- Claude will read this document and pick up where you left off

---

## Tools Location

All Python scripts are in the project root:
- `transcribe_audio.py` - Audio to text
- `generate_title.py` - Title generator
- `generate_cover_prompt.py` - Gemini prompt generator
- `convert_to_mp4.py` - Audio + image to video

Python path: `C:\Users\rober\AppData\Local\Programs\Python\Python312\python.exe`
FFmpeg path: `C:\Users\rober\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\`

---

*Last updated: January 15, 2026*

---

## Quick Start Paths (For Claude)

When starting a new session, use these paths directly:
- **Project folder:** `C:/Users/rober/OneDrive/Desktop/undercover-fallout/`
- **Downloads:** `C:/Users/rober/Downloads/`
- **Python:** `C:\Users\rober\AppData\Local\Programs\Python\Python312\python.exe`
- **FFmpeg:** `C:\Users\rober\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\`

Run transcription from the project folder (not System32) to avoid permission errors with temp files.

---

## Quick Reference Commands

### Transcription
```bash
cd episodes/001-Episode-Folder
python "C:\Users\rober\AppData\Local\Programs\Python\Python312\python.exe" \
  "tools/transcribe_audio.py" \
  "Episode-001-Title.m4a" \
  "episode-001-transcript.txt"
```

### Convert to MP4 (with compression for GitHub)
```bash
# If file > 100MB, use higher CRF (32) and lower audio bitrate (128k)
ffmpeg -y -loop 1 \
  -i "episode-001-cover.png" \
  -i "Episode-001-Title.m4a" \
  -c:v libx264 -tune stillimage -crf 32 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p -shortest \
  "Episode-001-Title.mp4"
```

### Typical File Sizes
- Original m4a: ~69MB (35 min episode)
- MP4 with CRF 32: ~70MB (under GitHub 100MB limit)

*Process notes added: January 8, 2026*
