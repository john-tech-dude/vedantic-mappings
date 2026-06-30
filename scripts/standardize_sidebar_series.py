#!/usr/bin/env python3
"""Standardize sidebar series and cross-cartography TOC blocks."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MESSIAH_ITEMS = [
    ("messiah-threshold.html", "I · The Hermeneutic Key", "✦"),
    ("messiah-parables.html", "II · Three Bridges", "◈"),
    ("messiah-silence.html", "III · The Cloud of Unknowing", "◉"),
    ("messiah-beatitudes.html", "IV · The Beatitudes as Jnana Yoga", "🌱"),
    ("messiah-mirror.html", "V · Tat Tvam Asi", "⊙"),
    ("messiah-gospel-thomas.html", "VI · The Gospel of Thomas", "📖"),
    ("messiah-avatar.html", "VII · The Incarnation as Avatar", "☸"),
]

ADVITA_ITEMS = [
    ("vedanta-living-tradition.html", "Introduction"),
    ("advaita-gaudapada.html", "I · Gaudapada"),
    ("advaita-adi-shankara.html", "II · Adi Shankara"),
    ("advaita-ramana-maharshi.html", "III · Ramana Maharshi"),
    ("advaita-nisargadatta-maharaj.html", "IV · Nisargadatta Maharaj"),
]

KABBALAH_ITEMS = [
    ("kabbalah-sefer-yetzirah.html", "I · The Book of Creation"),
    ("kabbalah-zohar.html", "II · The Zohar"),
    ("kabbalah-luria.html", "III · Isaac Luria"),
    ("kabbalah-the-ramchal.html", "IV · The Ramchal"),
    ("kabbalah-mystical-union.html", "V · Mystical Union"),
    ("kabbalah_zivug_haneshamot.html", "VI · Zivug HaNeshamot"),
    ("kabbalah_shaar_hagilgulim.html", "VII · Sha'ar HaGilgulim"),
]

GNOSTICISM_ITEMS = [
    ("gnosticism-unknown-father.html", "I · The Source"),
    ("gnosticism-the_demiurge.html", "II · The Demiurge"),
    ("gnosticism-the_divine_spark.html", "III · The Divine Spark"),
    ("gnosticism_the_bridal_chamber.html", "IV · The Bridal Chamber"),
    ("gnosticism-syzygy-nymphon.html", "V · Syzygy Theology"),
]

TAOISM_ITEMS = [
    ("taoism-threshold.html", "I · The Unnamed Way"),
    ("taoism-practices.html", "II · The Uncarved Block"),
    ("taoism-butterfly.html", "III · The Butterfly Dream"),
    ("taoism-return.html", "IV · Returning to the Root"),
]

QUANTUM_ITEMS = [
    ("quantum-unmeasured.html", "I · The Unmeasured Ground"),
    ("quantum-observer.html", "II · The Act of Looking"),
    ("quantum-entanglement.html", "III · The Hidden Connection"),
    ("quantum-implicate.html", "IV · The Implicate Order"),
]

SECTION_END = r'(?=(?:\s*<div class="nav-(?:section-title|divider)")|\s*</div>\s*</div>)'


def messiah_series_block(active_href: str, prefix: str = "") -> str:
    lines = ['            <div class="nav-section-title">Jesus of Nazareth</div>']
    for href, label, icon in MESSIAH_ITEMS:
        full_href = f"{prefix}{href}"
        active = " active" if href == active_href else ""
        lines.append(
            f'            <a href="{full_href}" class="nav-item{active}">'
            f'<span class="nav-item-icon">{icon}</span><span>{label}</span></a>'
        )
    return "\n".join(lines)


def advaita_series_block(active_href: str, use_spans: bool = True) -> str:
    lines = ['            <div class="nav-section-title">Advaita Vedanta</div>']
    for href, label in ADVITA_ITEMS:
        active = " active" if href == active_href else ""
        if use_spans:
            lines.append(
                f'            <a href="{href}" class="nav-item{active}">'
                f'<span class="nav-item-icon">🕉</span><span>{label}</span></a>'
            )
        else:
            lines.append(f'            <a href="{href}" class="nav-item{active}">{label}</a>')
    return "\n".join(lines)


def kabbalah_series_block(active_href: str) -> str:
    lines = ['            <div class="nav-section-title">Kabbalah Series</div>']
    for href, label in KABBALAH_ITEMS:
        active = " active" if href == active_href else ""
        lines.append(f'            <a href="{href}" class="nav-item{active}">{label}</a>')
    return "\n".join(lines)


def gnosticism_series_block(active_href: str) -> str:
    lines = ['            <div class="nav-section-title">Gnosticism</div>']
    icons = ["◈", "⊡", "✦", "❤", "✦"]
    for (href, label), icon in zip(GNOSTICISM_ITEMS, icons):
        active = " active" if href == active_href else ""
        lines.append(
            f'            <a href="{href}" class="nav-item{active}">'
            f'<span class="nav-item-icon">{icon}</span><span>{label}</span></a>'
        )
    return "\n".join(lines)


def taoism_series_block(active_href: str) -> str:
    lines = ['            <div class="nav-section-title">Taoism · Four Pages</div>']
    icons = ["◈", "◇", "🦋", "↩"]
    for (href, label), icon in zip(TAOISM_ITEMS, icons):
        active = " active" if href == active_href else ""
        lines.append(
            f'            <a href="{href}" class="nav-item{active}">'
            f'<span class="nav-item-icon">{icon}</span><span>{label}</span></a>'
        )
    return "\n".join(lines)


def quantum_series_block(active_href: str) -> str:
    lines = ['            <div class="nav-section-title">Quantum · Four Pages</div>']
    for href, label in QUANTUM_ITEMS:
        active = " active" if href == active_href else ""
        lines.append(
            f'            <a href="{href}" class="nav-item{active}">'
            f'<span class="nav-item-icon">⚛</span><span>{label}</span></a>'
        )
    return "\n".join(lines)


def other_cartographies_span() -> str:
    return """            <div class="nav-section-title">Other Cartographies</div>
            <a href="../index.html" class="nav-item"><span class="nav-item-icon">⌂</span><span>Home · The Cartographies</span></a>
            <a href="../advaita-vedanta/vedanta-living-tradition.html" class="nav-item"><span class="nav-item-icon">🕉</span><span>Advaita Vedanta</span></a>
            <a href="../messiah/messiah-threshold.html" class="nav-item"><span class="nav-item-icon">✝</span><span>Jesus of Nazareth</span></a>
            <a href="../kabbalah/kabbalah-sefer-yetzirah.html" class="nav-item"><span class="nav-item-icon">🔯</span><span>Kabbalah</span></a>
            <a href="../gnosticism/gnosticism-unknown-father.html" class="nav-item"><span class="nav-item-icon">◈</span><span>Gnosticism</span></a>
            <a href="../taoism/taoism-threshold.html" class="nav-item"><span class="nav-item-icon">☯</span><span>Taoism · The Unnamed Way</span></a>
            <a href="../quantum_mechanics/quantum-unmeasured.html" class="nav-item"><span class="nav-item-icon">⚛</span><span>Quantum Mechanics</span></a>"""


def vedantic_mappings_block() -> str:
    return """            <div class="nav-section-title">Vedantic Mappings</div>
            <a href="../index.html" class="nav-item">⌂ Home</a>
            <a href="../advaita-vedanta/vedanta-living-tradition.html" class="nav-item">Advaita Vedanta</a>
            <a href="../messiah/messiah-threshold.html" class="nav-item">Jesus of Nazareth</a>
            <a href="kabbalah-sefer-yetzirah.html" class="nav-item">Kabbalah</a>
            <a href="../gnosticism/gnosticism-unknown-father.html" class="nav-item">Gnosticism</a>
            <a href="../taoism/taoism-threshold.html" class="nav-item">Taoism · The Unnamed Way</a>
            <a href="../quantum_mechanics/quantum-unmeasured.html" class="nav-item">Quantum Mechanics</a>"""


def replace_section(content: str, title: str, new_block: str) -> str:
    pattern = rf'<div class="nav-section-title">{re.escape(title)}</div>.*?' + SECTION_END
    if re.search(pattern, content, flags=re.DOTALL):
        return re.sub(pattern, new_block, content, count=1, flags=re.DOTALL)
    return content


def remove_duplicate_sections(content: str, title: str) -> str:
    pattern = rf'<div class="nav-section-title">{re.escape(title)}</div>.*?' + SECTION_END
    matches = list(re.finditer(pattern, content, flags=re.DOTALL))
    if len(matches) <= 1:
        return content
    for match in reversed(matches[1:]):
        content = content[: match.start()] + content[match.end() :]
    return content


def remove_trailing_taoism_block(content: str) -> str:
    pattern = (
        r'<div class="nav-divider"></div>\s*'
        r'<div class="nav-section-title">Taoism · Four Pages</div>.*?' + SECTION_END
    )
    # Remove only if it appears after Other Cartographies
    if "Other Cartographies" in content:
        return re.sub(pattern, "", content, flags=re.DOTALL)
    return content


def process_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    content = path.read_text(encoding="utf-8")
    original = content
    name = path.name

    if rel.parts[0] == "messiah":
        content = replace_section(
            content,
            "Jesus of Nazareth",
            messiah_series_block(name),
        )
        content = replace_section(
            content,
            "Vedantic Mappings",
            messiah_series_block(name)
            + '\n            <div class="nav-divider"></div>\n'
            + other_cartographies_span(),
        )
        content = replace_section(content, "Other Cartographies", other_cartographies_span())
        content = remove_duplicate_sections(content, "Other Cartographies")
        content = remove_duplicate_sections(content, "Jesus of Nazareth")
        content = remove_trailing_taoism_block(content)

    elif rel.parts[0] == "kabbalah" and name == "messiah-beatitudes.html":
        content = replace_section(
            content,
            "Jesus of Nazareth",
            messiah_series_block("messiah-beatitudes.html", prefix="../messiah/"),
        )
        content = replace_section(content, "Other Cartographies", other_cartographies_span())
        content = remove_duplicate_sections(content, "Other Cartographies")

    elif rel.parts[0] == "kabbalah":
        content = replace_section(content, "Kabbalah Series", kabbalah_series_block(name))
        content = replace_section(content, "Vedantic Mappings", vedantic_mappings_block())
        content = remove_duplicate_sections(content, "Kabbalah Series")

    elif rel.parts[0] == "advaita-vedanta":
        use_spans = name != "advaita-gaudapada.html"
        content = replace_section(content, "Advaita Vedanta", advaita_series_block(name, use_spans=use_spans))
        content = replace_section(content, "Other Cartographies", other_cartographies_span())
        content = remove_duplicate_sections(content, "Other Cartographies")

    elif rel.parts[0] == "gnosticism":
        content = replace_section(content, "Gnosticism", gnosticism_series_block(name))
        content = replace_section(content, "Other Cartographies", other_cartographies_span())
        content = remove_duplicate_sections(content, "Other Cartographies")

    elif rel.parts[0] == "taoism":
        content = replace_section(content, "Taoism · Four Pages", taoism_series_block(name))
        content = replace_section(content, "Other Cartographies", other_cartographies_span())
        content = remove_duplicate_sections(content, "Other Cartographies")

    elif rel.parts[0] == "quantum_mechanics":
        content = replace_section(content, "Quantum · Four Pages", quantum_series_block(name))
        content = replace_section(content, "Other Cartographies", other_cartographies_span())
        content = remove_duplicate_sections(content, "Other Cartographies")

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main() -> None:
    updated = []
    for html_file in sorted(ROOT.rglob("*.html")):
        if ".git" in html_file.parts:
            continue
        if process_file(html_file):
            updated.append(html_file.relative_to(ROOT))

    print(f"Updated {len(updated)} files:")
    for f in updated:
        print(f"  - {f}")


if __name__ == "__main__":
    main()