#!/usr/bin/env python3
"""
Transcribe audio file to text using Google Speech Recognition.
Usage: python transcribe_audio.py <audio_file> [output_file]

Supports: .mp3, .m4a, .mp4, .wav
If no output file is specified, uses audio filename with -transcript.txt suffix.
"""

import speech_recognition as sr
from pydub import AudioSegment
import math
import os
import sys

# Configure ffmpeg path for pydub
FFMPEG_PATH = r"C:\Users\rober\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
os.environ["PATH"] = FFMPEG_PATH + os.pathsep + os.environ.get("PATH", "")
AudioSegment.converter = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(FFMPEG_PATH, "ffprobe.exe")

def transcribe_audio(audio_file, output_file=None):
    """
    Transcribe an audio file to text.

    Args:
        audio_file: Path to audio file (.mp3, .m4a, .mp4, .wav)
        output_file: Optional output path. Defaults to audio filename with -transcript.txt
    """

    if not os.path.exists(audio_file):
        print(f"Error: Audio file not found: {audio_file}")
        return False

    # Generate output filename if not provided
    if output_file is None:
        base_name = os.path.splitext(audio_file)[0]
        output_file = base_name + "-transcript.txt"

    # Determine file format
    ext = os.path.splitext(audio_file)[1].lower()

    print(f"Loading audio file: {audio_file}")
    print(f"Format: {ext}")

    try:
        if ext == '.mp3':
            audio = AudioSegment.from_mp3(audio_file)
        elif ext == '.m4a':
            audio = AudioSegment.from_file(audio_file, format='m4a')
        elif ext == '.mp4':
            audio = AudioSegment.from_file(audio_file, format='mp4')
        elif ext == '.wav':
            audio = AudioSegment.from_wav(audio_file)
        else:
            # Try generic loading
            audio = AudioSegment.from_file(audio_file)
    except Exception as e:
        print(f"Error loading audio: {e}")
        return False

    # Get duration
    duration_seconds = len(audio) / 1000
    print(f"Duration: {duration_seconds:.2f} seconds ({duration_seconds/60:.2f} minutes)")

    # Split into 30-second chunks for API limits
    chunk_length_ms = 30000  # 30 seconds
    chunks_count = math.ceil(len(audio) / chunk_length_ms)
    print(f"Processing {chunks_count} chunks...")
    print()

    recognizer = sr.Recognizer()
    full_transcript = []

    for i in range(chunks_count):
        start_ms = i * chunk_length_ms
        end_ms = min((i + 1) * chunk_length_ms, len(audio))

        chunk = audio[start_ms:end_ms]
        chunk_file = f"_temp_chunk_{i}.wav"

        print(f"[{i+1}/{chunks_count}] {start_ms/1000:.1f}s - {end_ms/1000:.1f}s ... ", end="", flush=True)

        # Export chunk as WAV
        chunk.export(chunk_file, format="wav")

        # Transcribe
        try:
            with sr.AudioFile(chunk_file) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
                full_transcript.append(text)
                print(f"OK")
        except sr.UnknownValueError:
            print("(silence/unclear)")
        except sr.RequestError as e:
            print(f"API error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")

        # Clean up chunk file
        try:
            os.remove(chunk_file)
        except:
            pass

    # Join all transcripts
    final_transcript = " ".join(full_transcript)

    # Save to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_transcript)

    print()
    print("=" * 60)
    print(f"Transcription complete!")
    print(f"Output: {output_file}")
    print(f"Length: {len(final_transcript)} characters")
    print("=" * 60)

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_audio.py <audio_file> [output_file]")
        print()
        print("Supported formats: .mp3, .m4a, .mp4, .wav")
        print()
        print("Example:")
        print("  python transcribe_audio.py episode.m4a")
        print("  python transcribe_audio.py episode.mp3 my-transcript.txt")
        sys.exit(1)

    audio = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    success = transcribe_audio(audio, output)
    sys.exit(0 if success else 1)
