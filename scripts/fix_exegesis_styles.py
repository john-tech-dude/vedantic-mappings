#!/usr/bin/env python3
"""Resolve internal style inconsistencies in kabbalah-exegesis.html."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "kabbalah-exegesis.html"

CSS_BLOCK = """
        /* ===== OPENING PULLQUOTE ===== */
        .pq-section {
            position: relative;
            padding: 5rem 2rem;
            text-align: center;
            background: radial-gradient(ellipse 90% 80% at 50% 35%, #1a1e3a 0%, #0f1220 40%, #0a0c14 70%);
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            overflow: hidden;
        }
        [data-theme="light"] .pq-section {
            background: radial-gradient(ellipse 90% 80% at 50% 35%, #e4e7f0 0%, #d8dce8 40%, #f0f2f8 70%);
        }
        .pq-section-glow {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -55%);
            width: 500px;
            height: 350px;
            background: radial-gradient(ellipse, var(--indigo-glow) 0%, transparent 55%);
            pointer-events: none;
            animation: breathe 10s ease-in-out infinite;
        }
        .pq-mark {
            font-family: 'Cormorant Garamond', serif;
            font-size: 8rem;
            color: var(--gold);
            opacity: 0.06;
            display: block;
        }
        .pq-text {
            font-family: 'IM Fell English', serif;
            font-style: italic;
            font-size: clamp(1.05rem, 2.5vw, 1.5rem);
            color: var(--ink);
            line-height: 1.68;
            max-width: 640px;
            margin: 0 auto 1.25rem;
            position: relative;
            z-index: 1;
        }
        .pq-attr {
            font-family: 'Cinzel', serif;
            font-size: 0.55rem;
            letter-spacing: 0.4em;
            color: var(--stone-light);
            text-transform: uppercase;
            position: relative;
            z-index: 1;
        }

        /* ===== HIGHLIGHTED STAGE ===== */
        .stage-section--highlight {
            background: var(--surface2);
            border-top: 2px solid var(--gold);
            border-bottom: 2px solid var(--gold);
        }

        /* ===== DIAGRAM SIZE VARIANTS ===== */
        .diagram-container--sm {
            max-width: 500px;
        }
        .diagram-container--md {
            max-width: 600px;
        }
        .diagram-container--lg {
            max-width: 700px;
        }

        /* ===== GEMATRIA CARDS ===== */
        .gematria-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        .gematria-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            box-shadow: var(--shadow);
        }
        .gematria-card-title {
            font-family: 'Cinzel', serif;
            font-size: 0.6rem;
            letter-spacing: 0.3em;
            color: var(--gold);
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        .gematria-row {
            display: flex;
            justify-content: space-between;
            font-family: 'Crimson Pro', serif;
            font-size: 1rem;
            color: var(--stone);
        }
        .gematria-value {
            color: var(--gold);
            font-weight: 600;
        }
        .gematria-divider {
            border: none;
            border-top: 1px solid var(--border);
            margin: 0.5rem 0;
        }
        .gematria-note {
            font-size: 0.85rem;
            color: var(--ink2);
            margin: 0.25rem 0 0.5rem 0;
            text-align: right;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 0.25rem;
        }
        .gematria-note:last-child,
        .gematria-note--final {
            border-bottom: none;
            margin-bottom: 0;
        }
        .gematria-closing {
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 0.65rem;
            letter-spacing: 0.25em;
            color: var(--stone);
            text-transform: uppercase;
            margin-top: 1rem;
        }

        /* ===== REVELATION & DECREE BOXES ===== */
        .revelation-box,
        .decree-box {
            background: var(--surface);
            border-left: 4px solid var(--gold);
            border-radius: var(--radius-sm);
            padding: 1.5rem 2rem;
            margin: 2rem 0;
            box-shadow: var(--shadow-gold);
        }
        .decree-box {
            margin: 2.5rem 0;
            padding: 2rem;
        }
        .revelation-text {
            font-family: 'IM Fell English', serif;
            font-size: 1.2rem;
            font-style: italic;
            color: var(--ink);
            margin: 0;
        }
        .revelation-mark {
            font-size: 2rem;
            color: var(--gold);
        }
        .revelation-line {
            display: block;
            margin-top: 0.25rem;
            color: var(--gold);
        }
        .revelation-line--spaced {
            margin-top: 0.5rem;
        }
        .revelation-caption {
            display: block;
            margin-top: 0.5rem;
            font-family: 'Cinzel', serif;
            font-size: 0.7rem;
            letter-spacing: 0.2em;
            color: var(--stone-light);
        }
        .decree-body {
            font-family: 'Crimson Pro', serif;
            font-size: 1rem;
            color: var(--stone);
            line-height: 1.8;
            margin-top: 0.5rem;
        }
        .decree-closing {
            font-family: 'IM Fell English', serif;
            font-size: 1.4rem;
            font-style: italic;
            color: var(--gold);
            text-align: center;
            margin-top: 1rem;
        }

        /* ===== UNION FORMULA ===== */
        .union-display {
            display: flex;
            justify-content: center;
            margin: 1.5rem 0;
        }
        .union-formula {
            background: var(--surface);
            border: 1px solid var(--gold);
            border-radius: var(--radius-md);
            padding: 1.5rem 2rem;
            text-align: center;
            max-width: 600px;
        }
        .union-formula-part {
            font-size: 1.2rem;
        }
        .union-formula-op {
            color: var(--gold);
            font-size: 1.5rem;
        }
        .union-formula-vav {
            color: var(--gold);
            font-size: 1.5rem;
        }
        .union-formula-sum {
            color: var(--gold);
            font-size: 2rem;
            font-weight: 600;
        }
        .union-formula-label {
            font-size: 0.9rem;
            color: var(--stone-light);
            margin-top: 0.5rem;
        }

        /* ===== PROPHETIC LIST ===== */
        .prophetic-list {
            list-style: none;
            padding: 0;
            margin: 1rem 0;
        }
        .prophetic-list li {
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border-subtle);
        }
        .prophetic-list li:last-child {
            border-bottom: none;
        }

        /* ===== STAGE CALLOUTS ===== */
        .stage-callout {
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 0.8rem;
            letter-spacing: 0.3em;
            color: var(--gold);
            margin: 2rem 0;
        }
        .stage-callout--seal {
            font-size: 0.7rem;
            letter-spacing: 0.4em;
            margin-top: 3rem;
        }
        .seal-quote-box {
            background: var(--surface);
            border: 1px solid var(--gold);
            border-radius: var(--radius-md);
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
        }
        .seal-quote-text {
            font-family: 'IM Fell English', serif;
            font-style: italic;
            font-size: 1.2rem;
            color: var(--ink);
        }
        .seal-quote-attr {
            font-family: 'Cinzel', serif;
            font-size: 0.55rem;
            letter-spacing: 0.3em;
            color: var(--stone-light);
            text-transform: uppercase;
            margin-top: 0.5rem;
        }
"""

REPLACEMENTS = [
    ('a:focus-visible,\n        button:focus-visible', None),  # skip - add manually
    ('class="diagram-container" style="max-width:500px;"', 'class="diagram-container diagram-container--sm"'),
    ('class="diagram-container" style="max-width:600px;"', 'class="diagram-container diagram-container--md"'),
    ('class="diagram-container" style="max-width:700px;"', 'class="diagram-container diagram-container--lg"'),
    (
        '<section class="stage-section" id="numerical" style="background:var(--surface2); border-top:2px solid var(--gold); border-bottom:2px solid var(--gold);">',
        '<section class="stage-section stage-section--highlight" id="numerical">',
    ),
    (
        '<section class="stage-section" id="present" style="background:var(--surface2); border-top:2px solid var(--gold); border-bottom:2px solid var(--gold);">',
        '<section class="stage-section stage-section--highlight" id="present">',
    ),
    ('<ul style="list-style: none; padding:0; margin:1rem 0;">', '<ul class="prophetic-list">'),
    (
        '<li style="padding:0.5rem 0; border-bottom:1px solid var(--border-subtle);">',
        '<li>',
    ),
    (
        '<p style="text-align:center; font-family:\'Cinzel\',serif; font-size:0.8rem; letter-spacing:0.3em; color:var(--gold); margin:2rem 0;">',
        '<p class="stage-callout">',
    ),
    (
        '<p style="text-align:center; font-family:\'Cinzel\',serif; font-size:0.7rem; letter-spacing:0.4em; color:var(--gold); margin-top:3rem;">',
        '<p class="stage-callout stage-callout--seal">',
    ),
    (
        '<p style="text-align:center; font-family:\'Cinzel\',serif; font-size:0.65rem; letter-spacing:0.25em; color:var(--stone); text-transform:uppercase; margin-top:1rem;">',
        '<p class="gematria-closing">',
    ),
]


def main():
    text = FILE.read_text(encoding="utf-8")

    # focus-visible
    if "a:focus-visible" not in text:
        text = text.replace(
            "        ::selection {\n"
            "            background: rgba(196, 168, 85, 0.15);\n"
            "            color: var(--ink);\n"
            "        }\n",
            "        ::selection {\n"
            "            background: rgba(90, 106, 154, 0.20);\n"
            "            color: var(--ink);\n"
            "        }\n"
            "        a:focus-visible,\n"
            "        button:focus-visible {\n"
            "            outline: 2px solid var(--gold);\n"
            "            outline-offset: 2px;\n"
            "            border-radius: 4px;\n"
            "        }\n",
        )

    # hotspot light theme tokens
    text = text.replace(
        "        [data-theme=\"light\"] .hotspot {\n"
        "            border-bottom-color: #8a7030;\n"
        "            color: #8a7030;\n"
        "        }\n"
        "        [data-theme=\"light\"] .hotspot:hover {\n"
        "            border-bottom-color: #6a5820;\n"
        "        }\n",
        "        [data-theme=\"light\"] .hotspot {\n"
        "            border-bottom-color: var(--gold);\n"
        "            color: var(--gold);\n"
        "        }\n"
        "        [data-theme=\"light\"] .hotspot:hover {\n"
        "            border-bottom-color: var(--gold-deep);\n"
        "        }\n",
    )

    # footer light theme
    if '[data-theme="light"] .footer-emblem-outer' not in text:
        text = text.replace(
            "        [data-theme=\"dark\"] .footer-emblem-inner {\n"
            "            border-color: var(--gold-light);\n"
            "        }\n"
            "        .footer-name {",
            "        [data-theme=\"dark\"] .footer-emblem-inner {\n"
            "            border-color: var(--gold-light);\n"
            "        }\n"
            "        [data-theme=\"light\"] .footer-emblem-outer {\n"
            "            border-color: var(--gold);\n"
            "        }\n"
            "        [data-theme=\"light\"] .footer-emblem-inner {\n"
            "            border-color: var(--gold-light);\n"
            "        }\n"
            "        .footer-name {",
        )

    # insert CSS block
    if ".pq-section {" not in text:
        text = text.replace(
            "        /* ===== RESPONSIVE ===== */",
            CSS_BLOCK + "\n        /* ===== RESPONSIVE ===== */",
        )

    for old, new in REPLACEMENTS:
        if old and new:
            text = text.replace(old, new)

    # opening pullquote
    old_pq = '''    <div class="pq-section" id="intro" style="padding:5rem 2rem; text-align:center; background:radial-gradient(ellipse 90% 80% at 50% 35%, #1a1e3a 0%, #0f1220 40%, #0a0c14 70%); border-top:1px solid var(--border); border-bottom:1px solid var(--border);">
        <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-55%); width:500px; height:350px; background:radial-gradient(ellipse, var(--indigo-glow) 0%, transparent 55%); pointer-events:none; animation:breathe 10s ease-in-out infinite;"></div>
        <span style="font-family:'Cormorant Garamond',serif; font-size:8rem; color:var(--gold); opacity:0.06; display:block;">"</span>
        <p style="font-family:'IM Fell English',serif; font-style:italic; font-size:clamp(1.05rem,2.5vw,1.5rem); color:var(--ink); line-height:1.68; max-width:640px; margin:0 auto 1.25rem; position:relative; z-index:1;">
            "Thus says the Breath of the Living God, the One who sits upon the Throne of the Merkavah, He who spoke and the world was, He who hides the Light of the First Day for the righteous: I AM THAT I AM."
        </p>
        <p style="font-family:'Cinzel',serif; font-size:0.55rem; letter-spacing:0.4em; color:var(--stone-light); text-transform:uppercase; position:relative; z-index:1;">— The Prophetic Vision</p>
    </div>'''

    new_pq = '''    <div class="pq-section" id="intro">
        <div class="pq-section-glow" aria-hidden="true"></div>
        <span class="pq-mark" aria-hidden="true">"</span>
        <p class="pq-text">
            "Thus says the Breath of the Living God, the One who sits upon the Throne of the Merkavah, He who spoke and the world was, He who hides the Light of the First Day for the righteous: I AM THAT I AM."
        </p>
        <p class="pq-attr">— The Prophetic Vision</p>
    </div>'''
    text = text.replace(old_pq, new_pq)

    # gematria grid opening
    text = text.replace(
        '<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px,1fr)); gap:1.5rem; margin:2rem 0;">',
        '<div class="gematria-grid">',
    )
    text = text.replace(
        '<div style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-md); padding:1.5rem; box-shadow:var(--shadow);">',
        '<div class="gematria-card">',
    )
    text = text.replace(
        '<h4 style="font-family:\'Cinzel\',serif; font-size:0.6rem; letter-spacing:0.3em; color:var(--gold); text-transform:uppercase; margin-bottom:0.5rem;">',
        '<h4 class="gematria-card-title">',
    )
    text = text.replace(
        '<div style="display:flex; justify-content:space-between; font-family:\'Crimson Pro\',serif; font-size:1rem; color:var(--stone);">',
        '<div class="gematria-row">',
    )
    text = text.replace(
        '<span style="color:var(--gold); font-weight:600;">',
        '<span class="gematria-value">',
    )
    text = text.replace(
        '<hr style="border:none; border-top:1px solid var(--border); margin:0.5rem 0;">',
        '<hr class="gematria-divider">',
    )
    text = text.replace(
        '<div style="font-size:0.85rem; color:var(--ink2); margin:0.25rem 0 0.5rem 0; text-align:right; border-bottom:1px solid var(--border-subtle); padding-bottom:0.25rem;">',
        '<div class="gematria-note">',
    )
    text = text.replace(
        '<div style="font-size:0.85rem; color:var(--ink2); margin:0.25rem 0 0 0; text-align:right;">',
        '<div class="gematria-note gematria-note--final">',
    )

    # revelation box (numerical)
    old_rev = '''                <div style="background:var(--surface); border-left:4px solid var(--gold); border-radius:var(--radius-sm); padding:1.5rem 2rem; margin:2rem 0; box-shadow:var(--shadow-gold);">
                    <p style="font-family:'IM Fell English', serif; font-size:1.2rem; font-style:italic; color:var(--ink); margin:0;">
                        <span style="font-size:2rem; color:var(--gold);">✦</span>
                        <strong>The Revelation of the Key:</strong><br>
                        <span style="display:block; margin-top:0.25rem;">
                            <span style="color:var(--gold);">Gordon (269) + the Vav (6) + Ginger (266) = 541 = <strong>ישראל</strong></span>
                        </span>
                        <span style="display:block; margin-top:0.25rem;">
                            <span style="color:var(--gold);">The Key of David (מפתח דוד) = 542</span>
                        </span>
                        <span style="display:block; margin-top:0.25rem;">
                            <span style="color:var(--gold);">542 − 541 = <strong>1</strong> — the <em>Echad</em>, the One God who completes the union.</span>
                        </span>
                        <span style="display:block; margin-top:0.5rem; font-family:'Cinzel',serif; font-size:0.7rem; letter-spacing:0.2em; color:var(--stone-light);">
                            Israel + the One = the Key of David. Their union, sanctified by the Holy One, becomes the Key that opens and shuts the gates of redemption.
                        </span>
                        <span style="display:block; margin-top:0.5rem; font-family:'Cinzel',serif; font-size:0.7rem; letter-spacing:0.2em; color:var(--stone-light);">
                            — Discovered and verified by Gordon McKay, who calculated it himself.
                        </span>
                    </p>
                </div>'''

    new_rev = '''                <div class="revelation-box">
                    <p class="revelation-text">
                        <span class="revelation-mark">✦</span>
                        <strong>The Revelation of the Key:</strong><br>
                        <span class="revelation-line">
                            Gordon (269) + the Vav (6) + Ginger (266) = 541 = <strong>ישראל</strong>
                        </span>
                        <span class="revelation-line">
                            The Key of David (מפתח דוד) = 542
                        </span>
                        <span class="revelation-line">
                            542 − 541 = <strong>1</strong> — the <em>Echad</em>, the One God who completes the union.
                        </span>
                        <span class="revelation-caption">
                            Israel + the One = the Key of David. Their union, sanctified by the Holy One, becomes the Key that opens and shuts the gates of redemption.
                        </span>
                        <span class="revelation-caption">
                            — Discovered and verified by Gordon McKay, who calculated it himself.
                        </span>
                    </p>
                </div>'''
    text = text.replace(old_rev, new_rev)

    # union display
    old_union = '''                <div style="display:flex; justify-content:center; margin:1.5rem 0;">
                    <div style="background:var(--surface); border:1px solid var(--gold); border-radius:var(--radius-md); padding:1.5rem 2rem; text-align:center; max-width:600px;">
                        <span style="font-size:1.2rem;">1041</span> <span style="color:var(--gold); font-size:1.5rem;"> + </span> <span style="color:var(--gold); font-size:1.5rem;">ו</span> <span style="font-size:1.2rem;"> (6) </span> <span style="color:var(--gold); font-size:1.5rem;"> + </span> <span style="font-size:1.2rem;">941</span>
                        <br><span style="color:var(--gold); font-size:2rem; font-weight:600;">= 1988</span>
                        <div style="font-size:0.9rem; color:var(--stone-light); margin-top:0.5rem;">Ginger Marybeth Hovik + Vav + Gordon Bruce Embry McKay</div>
                    </div>
                </div>'''

    new_union = '''                <div class="union-display">
                    <div class="union-formula">
                        <span class="union-formula-part">1041</span> <span class="union-formula-op"> + </span> <span class="union-formula-vav">ו</span> <span class="union-formula-part"> (6) </span> <span class="union-formula-op"> + </span> <span class="union-formula-part">941</span>
                        <br><span class="union-formula-sum">= 1988</span>
                        <div class="union-formula-label">Ginger Marybeth Hovik + Vav + Gordon Bruce Embry McKay</div>
                    </div>
                </div>'''
    text = text.replace(old_union, new_union)

    # seal quote box
    old_seal = '''                <div style="background:var(--surface); border:1px solid var(--gold); border-radius:var(--radius-md); padding:2rem; margin:2rem 0; text-align:center;">
                    <p style="font-family:'IM Fell English', serif; font-style:italic; font-size:1.2rem; color:var(--ink);">
                        "What has been opened, no one shall shut."
                    </p>
                    <p style="font-family:'Cinzel',serif; font-size:0.55rem; letter-spacing:0.3em; color:var(--stone-light); text-transform:uppercase; margin-top:0.5rem;">
                        — The Key of David
                    </p>
                </div>'''

    new_seal = '''                <div class="seal-quote-box">
                    <p class="seal-quote-text">
                        "What has been opened, no one shall shut."
                    </p>
                    <p class="seal-quote-attr">
                        — The Key of David
                    </p>
                </div>'''
    text = text.replace(old_seal, new_seal)

    # decree box
    old_decree = '''                <div style="background:var(--surface); border-left:4px solid var(--gold); border-radius:var(--radius-sm); padding:2rem; margin:2.5rem 0; box-shadow:var(--shadow-gold);">
                    <p style="font-family:'IM Fell English', serif; font-size:1.2rem; font-style:italic; color:var(--ink); line-height:1.8; margin:0;">
                        <span style="font-size:2rem; color:var(--gold);">✦</span>
                        <strong>The Decree of the Most High</strong>
                    </p>
                    <p style="font-family:'Crimson Pro', serif; font-size:1rem; color:var(--stone); line-height:1.8; margin-top:0.5rem;">
                        <strong>Gordon and Ginger are the vessel of Israel.</strong> The One is the Key of David. Their union, corrected and sealed, is the prophetic timeline that spans from the revelation of the Messiah to the final gathering. The war of Gog and Magog is the external war that mirrors the internal war against their <em>Zivug</em>. The vision of the <em>Yichud</em> is the prophetic seal of their union. The silence of the Shekhinah is the <em>Tzimtzum</em> before the final revelation. They were attacked because they are the key to the <em>Tikkun</em>. The <em>Kelipot</em> have been defeated. The vessel is purified. The 1441 gate is open.
                    </p>
                    <p style="font-family:'IM Fell English', serif; font-size:1.4rem; font-style:italic; color:var(--gold); text-align:center; margin-top:1rem;">
                        "What has been opened, no one shall shut."
                    </p>
                </div>'''

    new_decree = '''                <div class="decree-box">
                    <p class="revelation-text">
                        <span class="revelation-mark">✦</span>
                        <strong>The Decree of the Most High</strong>
                    </p>
                    <p class="decree-body">
                        <strong>Gordon and Ginger are the vessel of Israel.</strong> The One is the Key of David. Their union, corrected and sealed, is the prophetic timeline that spans from the revelation of the Messiah to the final gathering. The war of Gog and Magog is the external war that mirrors the internal war against their <em>Zivug</em>. The vision of the <em>Yichud</em> is the prophetic seal of their union. The silence of the Shekhinah is the <em>Tzimtzum</em> before the final revelation. They were attacked because they are the key to the <em>Tikkun</em>. The <em>Kelipot</em> have been defeated. The vessel is purified. The 1441 gate is open.
                    </p>
                    <p class="decree-closing">
                        "What has been opened, no one shall shut."
                    </p>
                </div>'''
    text = text.replace(old_decree, new_decree)

    # responsive gematria grid
    if ".gematria-grid" not in text.split("/* ===== RESPONSIVE ===== */")[1][:500]:
        text = text.replace(
            "            .image-gallery {\n"
            "                grid-template-columns: 1fr;\n"
            "            }\n"
            "        }\n"
            "        @media (max-width: 480px) {",
            "            .image-gallery {\n"
            "                grid-template-columns: 1fr;\n"
            "            }\n"
            "            .gematria-grid {\n"
            "                grid-template-columns: 1fr;\n"
            "            }\n"
            "            .pq-section {\n"
            "                padding: 3.5rem 1.5rem;\n"
            "            }\n"
            "        }\n"
            "        @media (max-width: 480px) {",
        )

    remaining = text.count('style=')
    FILE.write_text(text, encoding="utf-8")
    print(f"Updated {FILE.name}")
    print(f"Remaining inline style= attributes: {remaining}")


if __name__ == "__main__":
    main()