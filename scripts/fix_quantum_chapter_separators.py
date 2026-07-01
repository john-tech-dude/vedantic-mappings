#!/usr/bin/env python3
"""
Replace flame/fire SVG with atom SVG in quantum mechanics chapter separators.
"""
import re
from pathlib import Path

# Pattern to match the flame/fire SVG in chapter separators
flame_svg_pattern = re.compile(
    r'<span class="chapter-sep"><svg width="14" height="18" viewBox="0 0 14 18" fill="none" xmlns="http://www\.w3\.org/2000/svg">\s*<path d="M7 18C3\.13401 18 0 14\.866 0 11C0 7\.13401 3\.13401 4 7 4C10\.866 4 14 7\.13401 14 11C14 14\.866 10\.866 18 7 18Z" fill="#c4a855"/>\s*<path d="M7 0C7 0 3\.5 4\.5 3\.5 8C3\.5 9\.933 5\.067 11\.5 7 11\.5C8\.933 11\.5 10\.5 9\.933 10\.5 8C10\.5 4\.5 7 0 7 0Z" fill="#e0c878"/>\s*</svg></span>',
    re.DOTALL
)

# Atom SVG replacement
atom_svg = '<span class="chapter-sep"><svg class="icon-atom" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><ellipse cx="12" cy="12" rx="3" ry="10" transform="rotate(45 12 12)"/><ellipse cx="12" cy="12" rx="3" ry="10" transform="rotate(-45 12 12)"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg></span>'

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
quantum_files = [
    "quantum_mechanics/quantum-unmeasured.html",
    "quantum_mechanics/quantum-observer.html", 
    "quantum_mechanics/quantum-implicate.html"
]

print("Replacing flame SVG with atom SVG in quantum chapter separators...")
print("=" * 60)

modified_files = 0
total_replacements = 0

for relative_path in quantum_files:
    filepath = project_dir / relative_path
    if not filepath.exists():
        print(f"⚠️  File not found: {relative_path}")
        continue
    
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        # Count matches before replacement
        matches = flame_svg_pattern.findall(content)
        if matches:
            file_replacements = len(matches)
            content = flame_svg_pattern.sub(atom_svg, content)
            
            if content != original_content:
                filepath.write_text(content, encoding='utf-8')
                print(f"✓ Replaced {file_replacements} flame SVGs with atom SVGs in: {relative_path}")
                modified_files += 1
                total_replacements += file_replacements
        else:
            print(f"ℹ️  No flame SVGs found in: {relative_path}")
            
    except Exception as e:
        print(f"✗ Error updating {relative_path}: {e}")

print("=" * 60)
print(f"Complete! Updated {modified_files} files, replaced {total_replacements} flame SVGs with atom SVGs.")