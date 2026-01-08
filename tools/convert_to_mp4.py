#!/usr/bin/env python3
"""
Convert audio file to MP4 video with static image.
Usage: python convert_to_mp4.py <audio_file> <image_file> [output_file]

If no output file is specified, it will use the audio filename with .mp4 extension.
"""

import subprocess
import sys
import os

# FFmpeg path (installed via winget)
FFMPEG_PATH = r"C:\Users\rober\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"

def convert_audio_to_mp4(audio_file, image_file, output_file=None):
    """
    Convert an audio file to MP4 video using a static image.

    Args:
        audio_file: Path to audio file (.m4a, .mp3, etc.)
        image_file: Path to image file (.jpg, .png, etc.)
        output_file: Optional output path. Defaults to audio filename with .mp4 extension.
    """

    if not os.path.exists(audio_file):
        print(f"Error: Audio file not found: {audio_file}")
        return False

    if not os.path.exists(image_file):
        print(f"Error: Image file not found: {image_file}")
        return False

    if not os.path.exists(FFMPEG_PATH):
        print(f"Error: FFmpeg not found at: {FFMPEG_PATH}")
        return False

    # Generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(audio_file)[0]
        output_file = base_name + ".mp4"

    print(f"Converting...")
    print(f"  Audio: {audio_file}")
    print(f"  Image: {image_file}")
    print(f"  Output: {output_file}")

    # FFmpeg command to combine static image with audio
    # -loop 1: loop the image
    # -i: input files
    # -c:v libx264: video codec
    # -tune stillimage: optimize for static image
    # -c:a aac: audio codec
    # -b:a 192k: audio bitrate
    # -pix_fmt yuv420p: pixel format for compatibility
    # -shortest: finish when shortest input ends (the audio)

    cmd = [
        FFMPEG_PATH,
        '-loop', '1',
        '-i', image_file,
        '-i', audio_file,
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        '-y',  # Overwrite output file if exists
        output_file
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / (1024 * 1024)
            print(f"\nSuccess! Created: {output_file}")
            print(f"File size: {file_size:.2f} MB")
            return True
        else:
            print(f"\nError during conversion:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"\nException during conversion: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_to_mp4.py <audio_file> <image_file> [output_file]")
        print("\nExample:")
        print("  python convert_to_mp4.py episode.m4a cover.jpg")
        print("  python convert_to_mp4.py episode.m4a cover.jpg Episode-001.mp4")
        sys.exit(1)

    audio = sys.argv[1]
    image = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    success = convert_audio_to_mp4(audio, image, output)
    sys.exit(0 if success else 1)
