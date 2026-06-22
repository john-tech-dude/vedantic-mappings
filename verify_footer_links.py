#!/usr/bin/env python3
"""
Script to verify and fix footer links in Gnosticism HTML files.
Ensures all links work and open in the same tab.
"""

import os
import re
from pathlib import Path

# Project root
PROJECT_ROOT = Path("/Users/g/Desktop/vedantic-mappings")

# Files to update
GNOSTICISM_FILES = [
    "gnosticism/gnosticism-unknown-father.html",
    "gnosticism/gnosticism-the_demiurge.html",
    "gnosticism/gnosticism-the_divine_spark.html",
    "gnosticism/gnosticism_the_bridal_chamber.html"
]

# Expected footer links (relative to gnosticism directory)
EXPECTED_LINKS = {
    "⌂ Vedantic Mappings": "../index.html",
    "Advaita Vedanta": "../advaita-vedanta/advaita-gaudapada.html",
    "The Vedantic Messiah": "../messiah/messiah-threshold.html",
    "Kabbalah": "../kabbalah/kabbalah-sefer-yetzirah.html",
    "Gnosticism": "gnosticism-unknown-father.html",
    "Taoism · The Unnamed Way": "../taoism/taoism-practices.html",
    "Quantum Mechanics": "../quantum_mechanics/quantum-observer.html"  # Fixed to use existing file
}

def resolve_link(link, base_file):
    """Resolve a relative link to an absolute path."""
    base_dir = base_file.parent
    absolute_link = (base_dir / link).resolve()
    return absolute_link

def link_exists(link, base_file):
    """Check if a link target file exists."""
    try:
        absolute_path = resolve_link(link, base_file)
        return absolute_path.exists()
    except:
        return False

def update_footer_links(file_path):
    """Update footer links in a file to match expected links."""
    print(f"\nProcessing: {file_path.name}")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove malicious script tags and base target="_blank" tags
    content = re.sub(r'<script type=[\'"].*?javascript[\'"].*?</script><base target="_blank">', '', content, flags=re.DOTALL)
    content = re.sub(r'<base target="_blank">', '', content)
    print("  ✅ Removed malicious base target tags")
    
    # Find the footer-links section
    footer_pattern = r'<div class="footer-links">(.*?)</div>'
    match = re.search(footer_pattern, content, re.DOTALL)
    
    if not match:
        print("  ❌ No footer-links section found")
        return False
    
    # Build new footer links
    new_links_html = '    <div class="footer-links">\n'
    for label, href in EXPECTED_LINKS.items():
        # Verify link exists
        if link_exists(href, file_path):
            status = "✅"
        else:
            status = "❌"
        print(f"  {status} {label}: {href}")
        new_links_html += f'      <a href="{href}">{label}</a>\n'
    new_links_html += '    </div>'
    
    # Replace the footer links section
    new_content = re.sub(footer_pattern, new_links_html, content, flags=re.DOTALL)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("  ✅ Footer links updated")
    return True

def main():
    print("=" * 60)
    print("Footer Link Verification and Update Script")
    print("=" * 60)
    
    for relative_path in GNOSTICISM_FILES:
        file_path = PROJECT_ROOT / relative_path
        if not file_path.exists():
            print(f"\n❌ File not found: {file_path}")
            continue
        
        update_footer_links(file_path)
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()