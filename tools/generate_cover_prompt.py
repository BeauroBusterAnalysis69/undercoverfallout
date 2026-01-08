#!/usr/bin/env python3
"""
Generate a Gemini 3 image prompt based on episode transcript.
Usage: python generate_cover_prompt.py <transcript_file> [episode_number]

Analyzes the transcript and creates a compelling image generation prompt
for creating episode cover art.
"""

import sys
import os
import re

def extract_key_themes(text):
    """Extract key themes and imagery from transcript text."""

    # Common powerful visual themes to look for
    theme_keywords = {
        'surveillance': ['spy', 'surveillance', 'watching', 'camera', 'monitor', 'tracking', 'hack', 'digital'],
        'danger': ['murder', 'kill', 'death', 'threat', 'danger', 'weapon', 'gun', 'knife'],
        'drugs': ['fentanyl', 'cocaine', 'meth', 'drugs', 'overdose', 'cartel', 'dealer'],
        'technology': ['ai', 'algorithm', 'computer', 'phone', 'digital', 'cyber', 'hack', 'code'],
        'conspiracy': ['federal', 'government', 'cia', 'fbi', 'dea', 'agent', 'undercover', 'secret'],
        'urban': ['street', 'city', 'neighborhood', 'trap house', 'hotel', 'alley'],
        'darkness': ['shadow', 'dark', 'night', 'hidden', 'underground', 'bunker'],
        'chaos': ['chaos', 'paranoia', 'addiction', 'relapse', 'breakdown', 'spiral'],
        'justice': ['justice', 'investigation', 'evidence', 'witness', 'informant', 'truth']
    }

    text_lower = text.lower()
    found_themes = []

    for theme, keywords in theme_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_themes.append(theme)
                break

    return list(set(found_themes))

def extract_specific_imagery(text):
    """Extract specific nouns and imagery from the text."""

    # Look for specific visual elements mentioned
    visual_elements = []

    patterns = [
        r'\b(phone|iphone|computer|laptop|screen)\b',
        r'\b(gun|weapon|knife)\b',
        r'\b(car|vehicle|van)\b',
        r'\b(house|apartment|hotel|building)\b',
        r'\b(street|alley|corner)\b',
        r'\b(camera|satellite|drone)\b',
        r'\b(money|cash|dollars)\b',
        r'\b(pills|powder|needle)\b',
        r'\b(badge|agent|officer)\b',
        r'\b(shadow|silhouette|figure)\b',
    ]

    text_lower = text.lower()
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        visual_elements.extend(matches)

    return list(set(visual_elements))

def generate_prompt(transcript_text, episode_number=None):
    """Generate a Gemini image prompt from transcript analysis."""

    themes = extract_key_themes(transcript_text)
    visuals = extract_specific_imagery(transcript_text)

    # Base style for the podcast
    style_elements = [
        "cinematic",
        "noir aesthetic",
        "deep shadows",
        "neon accents in purple and teal",
        "gritty urban atmosphere",
        "digital glitch effects",
        "mysterious and tense mood"
    ]

    # Build the prompt
    prompt_parts = []

    # Opening
    prompt_parts.append("Create a dark, cinematic podcast cover image.")

    # Theme-based imagery
    if 'surveillance' in themes:
        prompt_parts.append("Include surveillance imagery like camera lenses, digital screens, or watching eyes.")
    if 'danger' in themes:
        prompt_parts.append("Convey danger and threat through stark lighting and ominous elements.")
    if 'technology' in themes:
        prompt_parts.append("Incorporate digital/cyber elements like code, glitching effects, or circuit patterns.")
    if 'conspiracy' in themes:
        prompt_parts.append("Suggest government secrecy with redacted documents, badges, or shadowy figures.")
    if 'urban' in themes:
        prompt_parts.append("Set in a gritty urban environment with street lights and concrete.")
    if 'drugs' in themes:
        prompt_parts.append("Hint at the drug underworld through atmospheric tension, not explicit imagery.")
    if 'darkness' in themes:
        prompt_parts.append("Heavy use of shadows and darkness with selective lighting.")
    if 'chaos' in themes:
        prompt_parts.append("Visual chaos through layered, fragmented composition.")
    if 'justice' in themes:
        prompt_parts.append("Elements suggesting investigation - files, evidence, or searching light.")

    # Specific visual elements
    if visuals:
        prompt_parts.append(f"Consider incorporating: {', '.join(visuals[:5])}.")

    # Style guidance
    prompt_parts.append(f"Style: {', '.join(style_elements[:4])}.")

    # Color palette
    prompt_parts.append("Color palette: deep blacks, cosmic purples (#8B5CF6), electric teal (#14B8A6), with hints of warning red.")

    # Format
    prompt_parts.append("Square format for podcast cover. No text in the image.")

    # Combine
    full_prompt = " ".join(prompt_parts)

    return full_prompt, themes, visuals

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_cover_prompt.py <transcript_file> [episode_number]")
        print("\nExample:")
        print("  python generate_cover_prompt.py episode-001-transcript.txt 001")
        sys.exit(1)

    transcript_file = sys.argv[1]
    episode_num = sys.argv[2] if len(sys.argv) > 2 else "XXX"

    if not os.path.exists(transcript_file):
        print(f"Error: Transcript file not found: {transcript_file}")
        sys.exit(1)

    # Read transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    # Generate prompt
    prompt, themes, visuals = generate_prompt(transcript_text, episode_num)

    # Output
    print("=" * 70)
    print(f"GEMINI IMAGE PROMPT FOR EPISODE {episode_num}")
    print("=" * 70)
    print()
    print("DETECTED THEMES:", ", ".join(themes) if themes else "general")
    print("VISUAL ELEMENTS:", ", ".join(visuals) if visuals else "none specific")
    print()
    print("-" * 70)
    print("COPY THIS PROMPT FOR GEMINI 3:")
    print("-" * 70)
    print()
    print(prompt)
    print()
    print("=" * 70)

    # Also save to file
    output_file = f"cover-prompt-{episode_num}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Episode {episode_num} Cover Art Prompt\n")
        f.write(f"Detected Themes: {', '.join(themes)}\n")
        f.write(f"Visual Elements: {', '.join(visuals)}\n\n")
        f.write("PROMPT:\n")
        f.write(prompt)

    print(f"Prompt also saved to: {output_file}")

if __name__ == "__main__":
    main()
