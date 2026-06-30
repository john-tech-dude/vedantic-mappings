#!/usr/bin/env python3
"""Standardize messiah series hero sections."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "messiah"

HERO_BG = """        <svg style="position:absolute;inset:0;width:100%;height:auto" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
            <g style="animation:mandalaRotate 60s linear infinite">
                <circle cx="600" cy="400" r="350" fill="none" stroke="var(--gold)" stroke-width="0.3" opacity="0.08"/>
                <circle cx="600" cy="400" r="300" fill="none" stroke="var(--violet)" stroke-width="0.5" opacity="0.10"/>
                <circle cx="600" cy="400" r="250" fill="none" stroke="var(--gold)" stroke-width="0.4" opacity="0.07"/>
                <circle cx="600" cy="400" r="200" fill="none" stroke="var(--violet)" stroke-width="0.3" opacity="0.06"/>
            </g>
        </svg>
        <div class="hero-mountain" aria-hidden="true"></div>
        <div class="mandala-ring" aria-hidden="true"></div>
        <div class="mandala-ring" aria-hidden="true"></div>
        <div class="mandala-ring" aria-hidden="true"></div>
        <div class="mandala-ring" aria-hidden="true"></div>
        <div class="hero-ripple" aria-hidden="true"></div>
        <div class="hero-ripple" aria-hidden="true"></div>
        <div class="hero-ripple" aria-hidden="true"></div>

"""

HERO_CSS = """
        .hero-content {
            position: relative;
            z-index: 3;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2rem;
            max-width: 36rem;
            width: 100%;
            padding: 0 1.5rem;
        }
        .hero-content .hero-eyemark,
        .hero-content .hero-title,
        .hero-content .hero-quote,
        .hero-content .hero-quote-attr,
        .hero-content .hero-divider {
            margin-bottom: 0;
        }
        .hero-content .hero-divider {
            margin: 0 auto;
        }
"""

PAGES = {
    "messiah-threshold.html": {
        "title": "The Hermeneutic Key",
        "quote": "&ldquo;The Kingdom of God is within you.&rdquo;",
        "attr": "&mdash; Luke 17:21",
        "scroll": "introduction",
    },
    "messiah-parables.html": {
        "title": "Three Bridges",
        "quote": "&ldquo;The kingdom of God is in the midst of you.&rdquo;",
        "attr": "&mdash; Luke 17:21",
        "scroll": "introduction",
    },
    "messiah-silence.html": {
        "title": "The Cloud of Unknowing",
        "quote": "&ldquo;In the darkness of the cloud of unknowing, one finds the place where God dwells beyond all knowing.&rdquo;",
        "attr": "&mdash; The Cloud of Unknowing",
        "scroll": "apophatic-intro",
    },
    "messiah-beatitudes.html": {
        "title": "The Beatitudes",
        "quote": "&ldquo;Blessed are the poor in spirit, for theirs is the kingdom of heaven.&rdquo;",
        "attr": "&mdash; Matthew 5:3",
        "scroll": "toc",
    },
    "messiah-mirror.html": {
        "title": "Tat Tvam Asi",
        "quote": "&ldquo;In the beginning was the Word, and the Word was with God, and the Word was God.&rdquo;",
        "attr": "&mdash; John 1:1",
        "scroll": "section9",
    },
    "messiah-gospel-thomas.html": {
        "title": "The Gospel of Thomas",
        "quote": "&ldquo;Whoever finds the meaning of these sayings will not taste death.&rdquo;",
        "attr": "&mdash; Gospel of Thomas, Logion 1",
        "scroll": "intro",
    },
    "messiah-avatar.html": {
        "title": "The Incarnation as Avatar",
        "quote": "&ldquo;The Word became flesh and dwelt among us, full of grace and truth.&rdquo;",
        "attr": "&mdash; John 1:14",
        "scroll": "descent",
    },
}


def hero_block(meta: dict) -> str:
    scroll = meta["scroll"]
    return f"""{HERO_BG}        <div class="hero-content">
            <p class="hero-eyemark">Jesus of Nazareth</p>
            <h1 class="hero-title">{meta['title']}</h1>
            <div class="hero-divider" aria-hidden="true">
                <div class="hero-divider-line"></div>
                <div class="hero-divider-diamond"></div>
                <div class="hero-divider-line"></div>
            </div>
            <p class="hero-quote">{meta['quote']}</p>
            <p class="hero-quote-attr">{meta['attr']}</p>
        </div>
        <div class="hero-scroll-cue" onclick="document.getElementById('{scroll}').scrollIntoView({{behavior:'smooth'}})" tabindex="0" role="button">
            <span>Enter</span>
            <div class="scroll-line" aria-hidden="true"></div>
        </div>"""


def inject_css(content: str) -> str:
    if ".hero-content" in content:
        return content
    marker = "        .hero-eyemark {"
    if marker not in content:
        marker = "        .hero {"
        insert_at = content.find(marker)
        if insert_at == -1:
            return content
        end = content.find("}", insert_at) + 1
        return content[:end] + HERO_CSS + content[end:]
    return content.replace(marker, HERO_CSS + "\n" + marker, 1)


def replace_hero(content: str, filename: str) -> str:
    meta = PAGES[filename]

    if filename == "messiah-avatar.html":
        # Fix broken nav/hero structure
        content = re.sub(
            r"<script type='text/javascript' src='https://prod-chat-kimi[^>]*></script><base target=\"_blank\">",
            "",
            content,
        )
        nav_end = content.find("</div>\n  </div>\n  <h1 class=\"hero-title\">")
        if nav_end != -1:
            before = content[: nav_end + len("</div>\n  </div>")]
            after_start = content.find("</header>", nav_end)
            after = content[after_start + len("</header>") :]
            hero = (
                "\n</nav>\n\n<header class=\"hero\" id=\"hero\">\n"
                + hero_block(meta)
                + "\n</header>"
            )
            content = before + hero + after

    pattern = r'<header class="hero" id="hero">.*?</header>'
    replacement = f'<header class="hero" id="hero">\n{hero_block(meta)}\n    </header>'
    content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)
    return content


def main() -> None:
    for name, _ in PAGES.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        text = inject_css(text)
        text = replace_hero(text, name)
        path.write_text(text, encoding="utf-8")
        print(f"Updated {name}")

    # Mirror kabbalah duplicate beatitudes hero
    kabbalah = ROOT.parent / "kabbalah" / "messiah-beatitudes.html"
    if kabbalah.exists():
        meta = PAGES["messiah-beatitudes.html"]
        text = kabbalah.read_text(encoding="utf-8")
        if ".hero-content" not in text or "Jesus of Nazareth" not in text.split("hero-content")[1][:400]:
            text = inject_css(text)
            text = re.sub(
                r'<header class="hero" id="hero">.*?</header>',
                f'<header class="hero" id="hero">\n{hero_block(meta)}\n    </header>',
                text,
                count=1,
                flags=re.DOTALL,
            )
            kabbalah.write_text(text, encoding="utf-8")
            print("Updated kabbalah/messiah-beatitudes.html")


if __name__ == "__main__":
    main()