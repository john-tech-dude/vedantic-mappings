#!/usr/bin/env python3
import os
import re
from pathlib import Path
import sys

# Check for dry-run flag
DRY_RUN = '--dry-run' in sys.argv or '-d' in sys.argv

# Mapping of literal symbols/emojis to their clean vector inline SVG definitions.
# Note: Theme toggles use width="20" height="20" for premium visual balance,
# while standard icons use width="16" height="16" to fit perfectly inside the nav bar.
svg_mappings = {
    # Spiritual/Philosophical Section Symbols
    '🕉': '<svg class="icon-om" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 22s-8-4.5-8-11.5C4 6.5 8 2 12 2s8 4.5 8 8.5c0 7-8 11.5-8 11.5Z"/><path d="M12 22s-4-3-4-8.5C8 10 10 6 12 6s4 4 4 7.5c0 5.5-4 8.5-4 8.5Z"/><path d="M12 22c1.5 0 3-1 4-2.5M12 22c-1.5 0-3-1-4-2.5"/></svg>',
    '✝': '<svg class="icon-cross" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 2v20M8 8h8"/></svg>',
    '🔯': '<svg class="icon-star-david" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 2.5l5.5 9.5H6.5z"/><path d="M12 21.5L6.5 12h11z"/></svg>',
    '☯': '<svg class="icon-yinyang" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="M12 2a5 5 0 0 0 0 10 5 5 0 0 1 0 10"/><circle cx="12" cy="7" r="1.5" fill="currentColor"/><circle cx="12" cy="17" r="1.5" fill="none" stroke="currentColor" stroke-width="1"/></svg>',
    '⚛': '<svg class="icon-atom" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><ellipse cx="12" cy="12" rx="3" ry="10" transform="rotate(45 12 12)"/><ellipse cx="12" cy="12" rx="3" ry="10" transform="rotate(-45 12 12)"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
    '☸': '<svg class="icon-dharma" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/><path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M4.93 19.07L19.07 4.93"/></svg>',
    '◈': '<svg class="icon-diamond" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M2.7 10.3a2.4 2.4 0 0 0 0 3.4l7.6 7.6a2.4 2.4 0 0 0 3.4 0l7.6-7.6a2.4 2.4 0 0 0 0-3.4L13.7 2.7a2.4 2.4 0 0 0-3.4 0z"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
    '⊡': '<svg class="icon-squared-dot" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="12" cy="12" r="2" fill="currentColor"/></svg>',
    '⌂': '<svg class="icon-home" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    '⚖': '<svg class="icon-scales" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 3v17M12 20H4M12 20h8M3 7h18M6 7l-3 6h6l-3-6zM18 7l-3 6h6l-3-6z"/></svg>',
    '↩': '<svg class="icon-undo" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/></svg>',
    '◇': '<svg class="icon-diamond-outline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M2.7 10.3a2.4 2.4 0 0 0 0 3.4l7.6 7.6a2.4 2.4 0 0 0 3.4 0l7.6-7.6a2.4 2.4 0 0 0 0-3.4L13.7 2.7a2.4 2.4 0 0 0-3.4 0z"/></svg>',
    '↑': '<svg class="icon-arrow-up" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m18 15-6-6-6 6"/></svg>',

    # Page Elements / TOC Icons
    '📋': '<svg class="icon-clipboard" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/></svg>',
    '📖': '<svg class="icon-book" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    '📜': '<svg class="icon-scroll" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/></svg>',
    '📅': '<svg class="icon-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    '🦋': '<svg class="icon-butterfly" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 3v18M12 9c-1.5-3-5.5-4-8-1.5S3 14 7 14.5c2 .25 5-2 5-2M12 9c1.5-3 5.5-4 8-1.5S21 14 17 14.5c-2 .25-5-2-5-2M12 13.5c-2 0-6.5-1.5-8.5.5s0 4.5 3 4.5c3.5 0 5.5-5 5.5-5M12 13.5c2 0 6.5-1.5 8.5.5s0 4.5-3 4.5-5.5-5-5.5-5"/></svg>',
    '🧘': '<svg class="icon-meditator" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="5" r="2"/><path d="M12 7v6M7 16c0-2 2-3 5-3s5 1 5 3M5 20c1-2 3-3 7-3s6 1 7 3M8 12c-1.5.5-3 2-3 3M16 12c1.5.5 3 2 3 3"/></svg>',
    '😄': '<svg class="icon-smile" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2M9 9h.01M15 9h.01"/></svg>',
    '🧭': '<svg class="icon-compass" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    '🌱': '<svg class="icon-seedling" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M12 22V10M12 12c0-3 3-5 7-5M12 14c0-3-3-5-7-5"/></svg>',
    '🔍': '<svg class="icon-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    '❝': '<svg class="icon-quote" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.75-2-2-2H4c-1.25 0-2 .75-2 2v3c0 1.25.75 2 2 2h3c0 4-2 6-4 7zm11 0c3 0 7-1 7-8V5c0-1.25-.75-2-2-2h-4c-1.25 0-2 .75-2 2v3c0 1.25.75 2 2 2h3c0 4-2 6-4 7z"/></svg>',
    '❤': '<svg class="icon-heart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    '✨': '<svg class="icon-sparkles" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/><path d="m5 3 1 2.5L8.5 6 6 7 5 9.5 4 7 1.5 6 4 5.5z" opacity="0.6"/></svg>',
    '🌑': '<svg class="icon-moonphase" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><circle cx="12" cy="12" r="10" fill="currentColor"/></svg>',
    '✕': '<svg class="icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    '⚠': '<svg class="icon-warning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m12 5 9 14H3L12 5zM12 9v4M12 17h.01"/></svg>',
    '⚡': '<svg class="icon-energy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    '★': '<svg class="icon-star" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    '✧': '<svg class="icon-sparkle-small" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m12 5-1.5 5.5L5 12l5.5 1.5L12 19l1.5-5.5L19 12l-5.5-1.5Z"/></svg>',
    '✦': '<svg class="icon-sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275Z"/></svg>',

    # Theme Toggle Special Mappings (Bigger size, standard theme icon structure)
    '☼_theme': '<svg class="theme-toggle-icon theme-toggle-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    '☀_theme': '<svg class="theme-toggle-icon theme-toggle-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    '☾_theme': '<svg class="theme-toggle-icon theme-toggle-icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',

    '☼_ti_theme': '<svg class="theme-toggle-icon ti-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    '☀_ti_theme': '<svg class="theme-toggle-icon ti-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    '☾_ti_theme': '<svg class="theme-toggle-icon ti-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
}

# Clean inline styling helper for header icons
def get_header_svg(symbol):
    # Retrieve base SVG mapping
    base_svg = svg_mappings.get(symbol)
    if not base_svg:
        return ""
    # Inject styling to align nicely inside headings, and size to 18x18
    styled_svg = base_svg.replace('width="16" height="16"', 'width="18" height="18" style="vertical-align: -0.15em; margin-right: 0.35em; display: inline-block;"')
    return styled_svg

project_dir = Path("/Users/g/Desktop/vedantic-mappings")
html_files = sorted(list(project_dir.rglob("*.html")))

# Define patterns to search and replace inside HTML.
patterns = [
    # 1. Theme toggle icons
    (re.compile(r'<span class="theme-toggle-icon theme-toggle-icon-sun"[^>]*>\s*[☼☀]\s*</span>'), '☼_theme'),
    (re.compile(r'<span class="theme-toggle-icon theme-toggle-icon-moon"[^>]*>\s*☾\s*</span>'), '☾_theme'),
    (re.compile(r'<span class="theme-toggle-icon ti-sun"[^>]*>\s*[☼☀]\s*</span>'), '☼_ti_theme'),
    (re.compile(r'<span class="theme-toggle-icon ti-moon"[^>]*>\s*☾\s*</span>'), '☾_ti_theme'),

    # 2. Navigation items
    (re.compile(r'(<span class="nav-item-icon"[^>]*>\s*)([^\s<]+)(\s*</span>)'), None),

    # 3. Chapter separators and transition icons
    (re.compile(r'(<span class="chapter-sep"[^>]*>\s*)([^\s<]+)(\s*</span>)'), None),
    (re.compile(r'(<div class="chapter-transition-icon"[^>]*>\s*)([^\s<]+)(\s*</div>)'), None),

    # 4. Toc elements and other specific spans
    (re.compile(r'(<span class="toc-b-num"[^>]*>\s*)([^\s<]+)(\s*</span>)'), None),

    # 5. Additional span patterns that might contain emojis
    (re.compile(r'(<span class="[^"]*"[^>]*>\s*)([^\s<]+)(\s*</span>)'), None),

    # 6. Link text content with emojis
    (re.compile(r'(<a[^>]*>)([^<]*[🕉✝🔯☯⚛☸📋📖📜📅🦋🧘😄🧭🌱🔍❝❤✨🌑✕⚠⚡★☆☼☀☾◈⊡⌂⚖✧✦↩◇↑][^<]*)(</a>)'), None),

    # 7. Direct emoji replacement (catches emojis outside of specific containers)
    (re.compile(r'([🕉✝🔯☯⚛☸📋📖📜📅🦋🧘😄🧭🌱🔍❝❤✨🌑✕⚠⚡★☆☼☀☾◈⊡⌂⚖✧✦↩◇↑])'), None)
]

# Define character range by building literal unicode ranges as strings (avoiding raw string slash-U compile error)
emoji_range = '[\U0001F300-\U0001F9FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u27BF]'
heading_pattern = re.compile(r'(<h[1-6][^>]*>)\s*(' + emoji_range + r')\s*(.*?)(</h[1-6]>)')

# Pattern for CSS content rules with any emoji
css_emoji_pattern = re.compile(r"content:\s*['\"]([🕉✝🔯☯⚛☸📋📖📜📅🦋🧘😄🧭🌱🔍❝❤✨🌑✕⚠⚡★☆☼☀☾◈⊡⌂⚖✧✦✦✧★☆☀☼☾⚡⚠✕🌑✨❤🔍🌱🧭😄🧘🦋📅📜📖📋☸⚛☯🔯✝🕉])['\"];")

modified_files = 0
total_replacements = 0

print("Starting emoji to SVG migration...")
if DRY_RUN:
    print("DRY RUN MODE - No files will be modified")
    print("=" * 60)

def process_file(filepath):
    global modified_files, total_replacements
    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content
        
        file_replacements = 0
        changes = []  # Track specific changes for dry-run
        
        # 1. Apply span / container replacements
        for pattern, key_ref in patterns:
            if key_ref is not None:
                # Direct match and map replacement
                def repl_direct(match):
                    nonlocal file_replacements
                    svg = svg_mappings.get(key_ref)
                    if svg:
                        file_replacements += 1
                        if DRY_RUN:
                            changes.append(f"Theme toggle: {key_ref} -> SVG")
                        matched_str = match.group(0)
                        span_attrs_match = re.search(r'<span\s+([^>]*?)>', matched_str)
                        attrs = span_attrs_match.group(1) if span_attrs_match else ''
                        return f'<span {attrs}>{svg}</span>'
                    return match.group(0)
                content = pattern.sub(repl_direct, content)
            else:
                # Dynamic matching based on group 2 (the symbol inside the tags)
                def repl_dynamic(match):
                    nonlocal file_replacements
                    # Handle both 3-group patterns (prefix, symbol, suffix) and 1-group patterns (just symbol)
                    groups = match.groups()
                    if len(groups) == 3 and groups[1] is not None:
                        prefix = match.group(1)
                        symbol = match.group(2).strip()
                        suffix = match.group(3)
                        
                        # Check if symbol contains an emoji (for link text patterns)
                        for emoji_char in svg_mappings.keys():
                            if emoji_char in symbol:
                                file_replacements += 1
                                if DRY_RUN:
                                    changes.append(f"Symbol: {emoji_char} -> SVG")
                                symbol = symbol.replace(emoji_char, svg_mappings[emoji_char])
                        return f"{prefix}{symbol}{suffix}"
                    elif len(groups) == 1 and groups[0] is not None:
                        # Direct emoji replacement
                        symbol = match.group(1)
                        if symbol in svg_mappings:
                            file_replacements += 1
                            if DRY_RUN:
                                changes.append(f"Direct: {symbol} -> SVG")
                            return svg_mappings[symbol]
                    return match.group(0)
                content = pattern.sub(repl_dynamic, content)
        
        # 2. Apply Heading Tag Replacements
        def repl_heading(match):
            nonlocal file_replacements
            prefix = match.group(1)
            symbol = match.group(2)
            heading_text = match.group(3)
            suffix = match.group(4)
            
            if symbol in svg_mappings:
                file_replacements += 1
                if DRY_RUN:
                    changes.append(f"Heading: {symbol} -> SVG")
                header_svg = get_header_svg(symbol)
                return f"{prefix}{header_svg} {heading_text}{suffix}"
            return match.group(0)
            
        content = heading_pattern.sub(repl_heading, content)
        
        # 3. Apply CSS content: 'emoji'; replacements
        def repl_css(match):
            nonlocal file_replacements
            emoji_char = match.group(1)
            if emoji_char in svg_mappings:
                file_replacements += 1
                if DRY_RUN:
                    changes.append(f"CSS content: '{emoji_char}' -> SVG background")
                # For CSS content, we use a generic SVG placeholder - can be customized per emoji if needed
                return ('content: \'\'; background-image: url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'none\' stroke=\'white\' stroke-width=\'2\' stroke-linecap=\'round\' stroke-linejoin=\'round\'%3E%3Cpolygon points=\'13 2 3 14 12 14 11 22 21 10 12 10 13 2\'/%3E%3C/svg%3E"); '
                        'background-repeat: no-repeat; background-position: center; background-size: 16px 16px;')
            return match.group(0)
        
        content = css_emoji_pattern.sub(repl_css, content)
                
        if content != original_content:
            if DRY_RUN:
                print(f"📋 Would replace {file_replacements} symbols in: {filepath.relative_to(project_dir)}")
                for change in changes:
                    print(f"   - {change}")
                modified_files += 1
                total_replacements += file_replacements
            else:
                filepath.write_text(content, encoding='utf-8')
                print(f"✓ Replaced {file_replacements} symbols in: {filepath.relative_to(project_dir)}")
                modified_files += 1
                total_replacements += file_replacements
            
    except Exception as e:
        print(f"✗ Error processing {filepath}: {e}")

for filepath in html_files:
    if '.git' in filepath.parts or '.gemini' in filepath.parts:
        continue
    process_file(filepath)

if DRY_RUN:
    print("=" * 60)
    print(f"DRY RUN COMPLETE")
    print(f"Would update {modified_files} files with {total_replacements} emoji-to-SVG replacements")
    print("Run without --dry-run flag to apply changes")
else:
    print(f"\nMigration complete! Updated {modified_files} files, replaced {total_replacements} characters with SVGs.")
