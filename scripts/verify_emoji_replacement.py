#!/usr/bin/env python3
"""
Verification script to check for remaining emoji characters in HTML files
after the emoji-to-SVG migration. This ensures no Unicode symbols were missed.
"""
import re
from pathlib import Path

# List of emojis that should have been replaced
target_emojis = [
    '🕉', '✝', '🔯', '☯', '⚛', '☸', '📋', '📖', '📜', '📅', 
    '🦋', '🧘', '😄', '🧭', '🌱', '🔍', '❝', '❤', '✨', '🌑', 
    '✕', '⚠', '⚡', '★', '☆', '☼', '☀', '☾', '◈', '⊡', '⌂', '⚖',
    '✧', '✦'
]

# Build regex pattern to find any of these emojis
emoji_pattern = re.compile('|'.join(re.escape(emoji) for emoji in target_emojis))

# Also check for CSS content rules with emojis (general pattern)
css_content_pattern = re.compile(r"content:\s*['\"][^'\"]*['\"]")

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
html_files = sorted(list(project_dir.rglob("*.html")))

print("Scanning for remaining emoji characters...")
print("=" * 60)

issues_found = False
total_issues = 0

for filepath in html_files:
    if '.git' in filepath.parts or '.gemini' in filepath.parts:
        continue
    
    try:
        content = filepath.read_text(encoding='utf-8')
        file_issues = []
        
        # Check for emoji characters
        emoji_matches = emoji_pattern.findall(content)
        if emoji_matches:
            file_issues.extend(emoji_matches)
        
        # Check for CSS content rules that might contain emojis
        css_matches = css_content_pattern.findall(content)
        for css_match in css_matches:
            # Check if the CSS content contains any of our target emojis
            for emoji in target_emojis:
                if emoji in css_match:
                    file_issues.append(css_match)
                    break
        
        if file_issues:
            issues_found = True
            total_issues += len(file_issues)
            print(f"⚠️  Found {len(file_issues)} issues in: {filepath.relative_to(project_dir)}")
            for issue in set(file_issues):  # Show unique issues
                print(f"   - {repr(issue)}")
                
    except Exception as e:
        print(f"✗ Error scanning {filepath}: {e}")

print("=" * 60)
if not issues_found:
    print("✅ VERIFICATION PASSED - No remaining emoji characters found!")
    print("All emoji characters have been successfully replaced with SVGs.")
else:
    print(f"❌ VERIFICATION FAILED - Found {total_issues} remaining emoji instances")
    print("Please review the files above and manually replace any remaining emojis.")