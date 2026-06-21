#!/usr/bin/env python3
"""
Script to add unique, high-quality SVG icons for each cartography section.
Each section (Quantum, Gnosticism, Advaita, Kabbalah, Taoism, Messiah) gets unique icons.
"""

import os
from pathlib import Path
import re

# Get the project directory
project_dir = Path("/Users/g/Desktop/vedantic-mappings")

# Find all HTML files
html_files = list(project_dir.rglob("*.html"))

print(f"Found {len(html_files)} HTML files to process.")

# Unique SVG icons for each cartography section
# Quantum Mechanics
quantum_svgs = {
    'I': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2c-4.4 0-8 3.6-8 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8z"/><path d="M12 6c-2.2 0-4 1.8-4 4s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4z"/></svg>',
    'II': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="5"/><path d="M12 7l3 3-3 3-3-3 3-3z"/><circle cx="12" cy="10" r="1.5" fill="currentColor"/></svg>',
    'III': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="6" cy="12" r="4"/><circle cx="18" cy="12" r="4"/><line x1="10" y1="12" x2="14" y2="12"/><path d="M8 8l4 4"/><path d="M8 16l4-4"/></svg>',
    'IV': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="7"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="2"/></svg>',
}

# Gnosticism
gnosticism_svgs = {
    'I': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="4" r="2"/><path d="M12 6v10"/><circle cx="8" cy="16" r="2"/><circle cx="16" cy="16" r="2"/><path d="M12 10l-4 6"/><path d="M12 10l4 6"/></svg>',
    'II': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><rect x="4" y="4" width="16" height="16" rx="2"/><circle cx="8" cy="12" r="2"/><circle cx="16" cy="12" r="2"/><path d="M10 12h4"/></svg>',
    'III': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2v4"/><path d="M12 18v4"/><path d="M2 12h4"/><path d="M18 12h4"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>',
    'IV': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="8" cy="12" r="6"/><circle cx="16" cy="12" r="6" opacity="0.5"/><path d="M12 2v20"/><path d="M8 8l8 8"/><path d="M16 8l-8 8"/></svg>',
}

# Advaita Vedanta
advaita_svgs = {
    'I': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 6v4"/><path d="M12 14v4"/><circle cx="12" cy="12" r="2"/><path d="M8 8l8 8"/><path d="M16 8l-8 8"/></svg>',
    'II': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 0 20"/><path d="M12 2a10 10 0 0 0 0 20"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>',
    'III': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="3"/><path d="M12 2v4"/><path d="M12 18v4"/></svg>',
    'IV': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M6 12h12"/><path d="M12 6v12"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
}

# Kabbalah
kabbalah_svgs = {
    'I': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="4" r="2"/><circle cx="8" cy="10" r="2"/><circle cx="16" cy="10" r="2"/><circle cx="12" cy="16" r="2"/><circle cx="6" cy="20" r="2"/><circle cx="18" cy="20" r="2"/><path d="M12 6v10M8 12l4 4M16 12l-4 4"/></svg>',
    'II': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M12 2v8M8 6l4 4M16 6l-4 4M6 10l6-6M18 10l-6-6"/><circle cx="12" cy="12" r="6"/><path d="M12 18v4"/></svg>',
    'III': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><circle cx="8" cy="16" r="3"/><circle cx="16" cy="16" r="3"/><path d="M11 8h2M11 16h2M8 11v2M16 11v2"/></svg>',
    'IV': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="3"/><path d="M12 2c-5.5 0-10 4.5-10 10s4.5 10 10 10"/></svg>',
    'V': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2v20"/><path d="M12 12l6-6"/><path d="M12 12l-6 6"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
}

# Taoism
taoism_svgs = {
    'I': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 0 0 20 10 10 0 0 1 0-20z"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>',
    'II': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M12 4c-2 2-4 4-4 8s2 6 4 8"/><path d="M12 4c2 2 4 4 4 8s-2 6-4 8"/><circle cx="12" cy="12" r="3" fill="currentColor"/></svg>',
    'III': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M12 2v20"/><path d="M12 12a6 6 0 0 1 6 6"/><path d="M12 12a6 6 0 0 0-6 6"/></svg>',
    'IV': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M8 12c0-2.2 1.8-4 4-4s4 1.8 4 4"/><path d="M12 12c0 2.2-1.8 4-4 4s-4-1.8-4-4"/></svg>',
}

# Messiah
messiah_svgs = {
    'I': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M7 14c-1.1 0-2-.9-2-2 2-2 5-2 7 0 0 1.1-.9 2-2 2"/><circle cx="12" cy="10" r="4"/><path d="M12 14v6"/><path d="M10 18h4"/></svg>',
    'II': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><path d="M4 12h4l4-4 4 4h4"/><path d="M8 16l4-4"/><path d="M16 16l-4-4"/><line x1="12" y1="8" x2="12" y2="12"/></svg>',
    'III': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="12" cy="12" r="10"/><path d="M8 8c0 2.2 1.8 4 4 4s4-1.8 4-4"/><path d="M8 16c0 2.2 1.8 4 4 4s4-1.8 4-4" opacity="0.5"/><circle cx="12" cy="12" r="3"/></svg>',
    'IV': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="18" height="18"><circle cx="8" cy="12" r="4"/><circle cx="16" cy="12" r="4"/><path d="M12 8v8"/><path d="M10 10l4 4"/><path d="M14 10l-4 4"/></svg>',
}

# Section detection patterns based on nav-section-title
section_patterns = {
    'Quantum': quantum_svgs,
    'Gnosticism': gnosticism_svgs,
    'Advaita': advaita_svgs,
    'Kabbalah': kabbalah_svgs,
    'Taoism': taoism_svgs,
    'The Vedantic Messiah': messiah_svgs,
}

processed_count = 0

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Find all nav-section-title patterns and their following items
        for section_title, svg_set in section_patterns.items():
            # Look for section title
            section_pattern = rf'<div class="nav-section-title">{re.escape(section_title)}'
            
            if not re.search(section_pattern, content, re.IGNORECASE):
                continue
            
            # Find the position of this section
            section_match = re.search(section_pattern, content, re.IGNORECASE)
            if not section_match:
                continue
            
            # Get the content from this section onwards
            section_start = section_match.start()
            
            # Find the next section or end of nav-menu
            next_section = re.search(r'<div class="nav-section-title">', content[section_start + 100:])
            if next_section:
                section_end = section_start + 100 + next_section.start()
            else:
                section_end = content.find('</div>', section_start + 500)
                if section_end == -1:
                    section_end = len(content)
            
            section_content = content[section_start:section_end]
            
            # Replace SVGs for Roman numeral items in this section
            for roman_numeral, svg in svg_set.items():
                # Pattern: <span class="nav-item-icon">[old svg]</span><span>II · Title</span>
                # Match the span with the Roman numeral in the text
                numeral_pattern = rf'<span class="nav-item-icon">.*?</span><span>{re.escape(roman_numeral)} &'
                if re.search(numeral_pattern, section_content):
                    section_content = re.sub(
                        rf'(<span class="nav-item-icon">).*?(</span><span>{re.escape(roman_numeral)} &)',
                        rf'\1{svg}\2',
                        section_content,
                        count=1
                    )
            
            # Replace the section content
            content = content[:section_start] + section_content + content[section_end:]
        
        # Only write if content changed
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {html_file.relative_to(project_dir)}")
            processed_count += 1
        else:
            print(f"- Skipped (no changes): {html_file.relative_to(project_dir)}")
            
    except Exception as e:
        print(f"✗ Error processing {html_file}: {e}")
        import traceback
        traceback.print_exc()

print(f"\nDone! Processed {processed_count} files.")
print("Added unique SVG icons for each cartography section.")