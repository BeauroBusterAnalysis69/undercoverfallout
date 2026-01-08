#!/usr/bin/env python3
"""
Generate edgy episode titles from transcript content.
Usage: python generate_title.py <transcript_file> [episode_number]

Analyzes transcript and generates provocative, intriguing titles
in the Undercover Fallout style.
"""

import sys
import os
import re
from collections import Counter

# Power words that make titles pop
POWER_WORDS = {
    'danger': ['murder', 'kill', 'death', 'dead', 'assassin', 'threat', 'lethal', 'fatal'],
    'crime': ['cocaine', 'fentanyl', 'meth', 'cartel', 'dealer', 'trafficking', 'smuggling', 'extortion'],
    'government': ['cia', 'fbi', 'dea', 'federal', 'agent', 'operative', 'informant', 'undercover'],
    'tech': ['hack', 'algorithm', 'ai', 'digital', 'cyber', 'surveillance', 'encrypted', 'dark web'],
    'money': ['million', 'thousand', '$', 'laundering', 'cash', 'wire', 'fraud'],
    'chaos': ['paranoia', 'breakdown', 'spiral', 'addiction', 'relapse', 'psychosis', 'manic'],
    'places': ['trap house', 'bunker', 'safehouse', 'border', 'warehouse', 'hotel', 'alley'],
    'people': ['ms-13', 'ghost', 'shadow', 'snitch', 'handler', 'asset', 'target'],
}

# Title templates for edgy combinations
TITLE_TEMPLATES = [
    "{noun1}, {noun2}, and {noun3}",
    "{noun1}: {phrase}",
    "The {noun1} {noun2}",
    "{adjective} {noun1} and the {noun2}",
    "{number} {unit} to {event}",
    "{noun1} in the {place}",
    "Operation {codename}: {noun1}",
    "When {noun1} Meets {noun2}",
    "{verb}ing {noun1} While {adjective}",
    "The {noun1} Protocol",
]

def extract_key_terms(text):
    """Extract the most compelling terms from transcript."""
    text_lower = text.lower()

    found_terms = {category: [] for category in POWER_WORDS}

    for category, words in POWER_WORDS.items():
        for word in words:
            if word in text_lower:
                # Count occurrences
                count = text_lower.count(word)
                found_terms[category].append((word, count))

    # Sort by frequency
    for category in found_terms:
        found_terms[category].sort(key=lambda x: x[1], reverse=True)

    return found_terms

def extract_numbers(text):
    """Find compelling numbers mentioned."""
    # Look for dollar amounts
    dollars = re.findall(r'\$[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*\s*(?:dollars|thousand|million|k\b)', text.lower())

    # Look for other significant numbers
    numbers = re.findall(r'\b(\d+)\s*(days?|hours?|years?|months?|weeks?|minutes?)\b', text.lower())

    return dollars, numbers

def extract_specific_nouns(text):
    """Extract specific nouns that would make good title elements."""
    specific_patterns = [
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',  # Proper nouns
        r'\b(iPhone|Android|WhatsApp|Signal|Telegram)\b',  # Tech products
        r'\b(MS-13|Sinaloa|cartel)\b',  # Organizations
    ]

    nouns = []
    for pattern in specific_patterns:
        matches = re.findall(pattern, text)
        nouns.extend(matches)

    return list(set(nouns))[:10]

def generate_titles(transcript_text, episode_num="XXX"):
    """Generate multiple edgy title options."""

    terms = extract_key_terms(transcript_text)
    dollars, time_refs = extract_numbers(transcript_text)
    specific_nouns = extract_specific_nouns(transcript_text)

    titles = []

    # Get top terms from each category
    top_terms = {}
    for category, term_list in terms.items():
        if term_list:
            top_terms[category] = [t[0].title() for t in term_list[:3]]

    # Generate "X, Y, and Z" style titles
    all_top = []
    for category in ['danger', 'crime', 'government', 'tech']:
        if category in top_terms:
            all_top.extend(top_terms[category][:2])

    if len(all_top) >= 3:
        titles.append(f"{all_top[0]}, {all_top[1]}, and {all_top[2]}")
        titles.append(f"{all_top[2]}, {all_top[0]}, and the {all_top[1]}")

    # Generate titles with numbers
    if dollars:
        dollar_clean = dollars[0].replace(',', '')
        if 'danger' in top_terms:
            titles.append(f"{dollar_clean}: {top_terms['danger'][0]} Money")
        if 'crime' in top_terms:
            titles.append(f"The {dollar_clean} {top_terms['crime'][0]} Connection")

    if time_refs:
        num, unit = time_refs[0]
        if 'chaos' in top_terms:
            titles.append(f"{num} {unit.title()} to {top_terms['chaos'][0]}")
        if 'danger' in top_terms:
            titles.append(f"{num} {unit.title()} Till {top_terms['danger'][0]}")

    # Generate colon-style titles
    if 'tech' in top_terms and 'danger' in top_terms:
        titles.append(f"{top_terms['tech'][0]} {top_terms['danger'][0]}: Digital Carnage")
        titles.append(f"{top_terms['tech'][0]}ing While High: {top_terms['danger'][0]}")

    if 'government' in top_terms and 'crime' in top_terms:
        titles.append(f"{top_terms['government'][0]} {top_terms['crime'][0]}: The Inside Job")
        titles.append(f"The {top_terms['government'][0]} and the {top_terms['crime'][0]} Ring")

    # Place-based titles
    if 'places' in top_terms:
        place = top_terms['places'][0]
        if 'danger' in top_terms:
            titles.append(f"{top_terms['danger'][0]} in the {place}")
        if 'crime' in top_terms:
            titles.append(f"The {place} {top_terms['crime'][0]} Files")

    # Chaos titles
    if 'chaos' in top_terms:
        chaos = top_terms['chaos'][0]
        if 'tech' in top_terms:
            titles.append(f"Digital {chaos}: When AI Breaks Bad")
        if 'crime' in top_terms:
            titles.append(f"{chaos} and {top_terms['crime'][0]}: A Love Story")

    # Fallback generic edgy titles based on any found terms
    if not titles:
        any_terms = [t for cat in top_terms.values() for t in cat]
        if len(any_terms) >= 2:
            titles.append(f"The {any_terms[0]} {any_terms[1]} Conspiracy")
            titles.append(f"{any_terms[0]}: {any_terms[1]} Rising")

    # Remove duplicates and clean up
    seen = set()
    unique_titles = []
    for title in titles:
        title_clean = title.strip()
        if title_clean.lower() not in seen and len(title_clean) > 10:
            seen.add(title_clean.lower())
            unique_titles.append(title_clean)

    return unique_titles[:8], top_terms

def title_to_filename(title, episode_num):
    """Convert title to filename format."""
    # Remove special characters, replace spaces with hyphens
    clean = re.sub(r'[^\w\s-]', '', title)
    clean = re.sub(r'\s+', '-', clean.strip())
    return f"Episode-{episode_num}-{clean}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_title.py <transcript_file> [episode_number]")
        print("\nExample:")
        print("  python generate_title.py episode-001-transcript.txt 001")
        sys.exit(1)

    transcript_file = sys.argv[1]
    episode_num = sys.argv[2] if len(sys.argv) > 2 else "XXX"

    if not os.path.exists(transcript_file):
        print(f"Error: Transcript file not found: {transcript_file}")
        sys.exit(1)

    # Read transcript
    with open(transcript_file, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    # Generate titles
    titles, key_terms = generate_titles(transcript_text, episode_num)

    # Output
    print("=" * 70)
    print(f"EDGY TITLE OPTIONS FOR EPISODE {episode_num}")
    print("=" * 70)
    print()

    print("KEY THEMES DETECTED:")
    for category, terms in key_terms.items():
        if terms:
            print(f"  {category.upper()}: {', '.join(terms)}")
    print()

    print("-" * 70)
    print("TITLE OPTIONS (pick your favorite or remix):")
    print("-" * 70)
    print()

    for i, title in enumerate(titles, 1):
        filename = title_to_filename(title, episode_num)
        print(f"  {i}. {title}")
        print(f"     -> {filename}.mp4")
        print()

    print("=" * 70)

    # Save to file
    output_file = f"title-options-{episode_num}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Episode {episode_num} Title Options\n\n")
        for i, title in enumerate(titles, 1):
            filename = title_to_filename(title, episode_num)
            f.write(f"{i}. {title}\n")
            f.write(f"   Filename: {filename}.mp4\n\n")

    print(f"Options saved to: {output_file}")

if __name__ == "__main__":
    main()
