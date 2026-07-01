#!/usr/bin/env python3
"""Premium diagram upgrade for kabbalah-exegesis.html."""

from pathlib import Path
import re

FILE = Path(__file__).resolve().parents[1] / "kabbalah-exegesis.html"

PREMIUM_CSS = """
        /* ===== PREMIUM DIAGRAM ENHANCEMENTS ===== */
        .diagram-container {
            box-shadow: var(--shadow-deep), inset 0 1px 0 rgba(255, 255, 255, 0.04);
            border-color: var(--border-strong);
        }
        .diagram-container::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 10%;
            right: 10%;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold), transparent);
            opacity: 0.25;
            pointer-events: none;
        }
        .diagram-title {
            text-align: center;
            font-family: 'Cinzel', serif;
            font-size: 0.58rem;
            letter-spacing: 0.38em;
            text-transform: uppercase;
            color: var(--gold);
            margin-bottom: 1.25rem;
            position: relative;
            z-index: 1;
        }
        .diagram-title::after {
            content: '';
            display: block;
            width: 48px;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--gold), transparent);
            margin: 0.6rem auto 0;
            opacity: 0.5;
        }
        .diagram-svg {
            vector-effect: non-scaling-stroke;
        }
        [data-theme="light"] .diagram-container svg text[fill="#e8ecf4"],
        [data-theme="light"] .diagram-container svg text[fill="#e0e0e0"] {
            fill: var(--ink);
        }
        [data-theme="light"] .diagram-container svg text[fill="#1a1e2e"],
        [data-theme="light"] .diagram-container svg text[fill="#3a2a10"],
        [data-theme="light"] .diagram-container svg text[fill="#5a4a20"] {
            fill: var(--ink);
        }
"""

def frame_group(w: int, h: int, m: int = 12, l: int = 18) -> str:
    return f'''                        <rect x="{m}" y="{m}" width="{w-2*m}" height="{h-2*m}" rx="14" fill="var(--surface)" opacity="0.22" stroke="var(--border)" stroke-width="0.5"/>
                        <g class="diag-frame" stroke="var(--gold)" stroke-width="0.9" fill="none" opacity="0.38">
                            <path d="M{m},{m+l} L{m},{m} L{m+l},{m}"/>
                            <path d="M{w-m-l},{m} L{w-m},{m} L{w-m},{m+l}"/>
                            <path d="M{w-m},{h-m-l} L{w-m},{h-m} L{w-m-l},{h-m}"/>
                            <path d="M{m+l},{h-m} L{m},{h-m} L{m},{h-m-l}"/>
                        </g>'''


NEW_DIAGRAMS = [
    (
        '<nav class="toc-book" aria-label="Article contents">',
        '''        <div class="diagram-container diagram-container--lg fade-in">
            <div class="diagram-title">The Architecture of the Vision</div>
            <svg class="diagram-svg" viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" aria-label="Ten-chapter architecture of the prophetic vision">
                        <defs>
                            <filter id="archGlow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                            <linearGradient id="archGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#5a6a9a"/><stop offset="100%" stop-color="#c4a855"/></linearGradient>
                        </defs>
''' + frame_group(760, 200) + '''
                        <line x1="40" y1="100" x2="720" y2="100" stroke="url(#archGrad)" stroke-width="2.5" opacity="0.75"/>
                        <g font-family="'Cinzel', serif" font-size="7" fill="var(--gold)" text-anchor="middle">
                            <circle cx="55" cy="100" r="8" fill="var(--gold)" opacity="0.2" stroke="var(--gold)" filter="url(#archGlow)"/><text x="55" y="130">I–V</text><text x="55" y="142" font-size="6" fill="var(--stone-light)">Visions</text>
                            <circle cx="175" cy="100" r="8" fill="var(--gold)" opacity="0.25" stroke="var(--gold)" filter="url(#archGlow)"/><text x="175" y="130">VI</text><text x="175" y="142" font-size="6" fill="var(--stone-light)">Key</text>
                            <circle cx="295" cy="100" r="8" fill="var(--gold)" opacity="0.25" stroke="var(--gold)" filter="url(#archGlow)"/><text x="295" y="130">VII</text><text x="295" y="142" font-size="6" fill="var(--stone-light)">Numbers</text>
                            <circle cx="415" cy="100" r="8" fill="var(--gold)" opacity="0.25" stroke="var(--gold)" filter="url(#archGlow)"/><text x="415" y="130">VIII</text><text x="415" y="142" font-size="6" fill="var(--stone-light)">Revelation</text>
                            <circle cx="535" cy="100" r="8" fill="var(--crimson)" opacity="0.2" stroke="var(--crimson-light)" filter="url(#archGlow)"/><text x="535" y="130">IX</text><text x="535" y="142" font-size="6" fill="var(--stone-light)">Present</text>
                            <circle cx="655" cy="100" r="10" fill="var(--gold-light)" opacity="0.3" stroke="var(--gold)" stroke-width="1.5" filter="url(#archGlow)"/><text x="655" y="130" font-weight="600">X</text><text x="655" y="142" font-size="6" fill="var(--stone-light)">Seal</text>
                        </g>
                        <text x="380" y="42" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.28em">FIVE VISIONS · ONE KEY · TEN CHAPTERS</text>
                        <text x="380" y="175" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">From the Concealed Light to the Final Seal — Mafteach David</text>
                    </svg>
            <div class="diagram-caption">The Cartography of the Prophecy</div>
            <div class="diagram-subcaption">A single arc from Vision I through the Numerical Testimony to the Final Seal</div>
        </div>

        <nav class="toc-book" aria-label="Article contents">''',
    ),
    (
        '<p>The Gematria of the union reveals a truth that is not a matter of interpretation but of calculation. The numbers are the witnesses; they do not lie.</p>',
        '''<p>The Gematria of the union reveals a truth that is not a matter of interpretation but of calculation. The numbers are the witnesses; they do not lie.</p>

                <div class="diagram-container diagram-container--md fade-in">
                    <div class="diagram-title">Mafteach David — The Key of David</div>
                    <svg class="diagram-svg" viewBox="0 0 600 420" xmlns="http://www.w3.org/2000/svg" aria-label="The Key of David — Mafteach David">
                        <defs>
                            <filter id="keyDiagGlow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                            <linearGradient id="keyMetal" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e0c878"/><stop offset="50%" stop-color="#c4a855"/><stop offset="100%" stop-color="#8a7030"/></linearGradient>
                        </defs>
''' + frame_group(600, 420) + '''
                        <g transform="translate(300,200)" filter="url(#keyDiagGlow)">
                            <circle r="90" fill="none" stroke="var(--gold)" stroke-width="0.6" opacity="0.25"/>
                            <circle r="70" fill="none" stroke="var(--indigo-light)" stroke-width="0.4" opacity="0.3"/>
                            <path d="M-18,-55 L-18,45 L-8,55 L8,55 L18,45 L18,-55 Z" fill="url(#keyMetal)" stroke="#e0c878" stroke-width="1.5" opacity="0.95"/>
                            <circle cy="-62" r="22" fill="none" stroke="url(#keyMetal)" stroke-width="4"/>
                            <rect x="-6" y="-40" width="12" height="18" rx="2" fill="#1a1e2e" opacity="0.5"/>
                            <text y="8" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="14" fill="#1a1e2e">מפתח</text>
                        </g>
                        <text x="300" y="48" text-anchor="middle" font-family="'Cinzel', serif" font-size="10" fill="var(--gold)" letter-spacing="0.3em">MAFTEACH DAVID · מפתח דוד</text>
                        <text x="300" y="68" text-anchor="middle" font-family="'Cinzel', serif" font-size="14" fill="var(--gold-light)" font-weight="600">542</text>
                        <g font-family="'Crimson Pro', serif" font-size="9" fill="var(--stone-light)" text-anchor="middle">
                            <text x="120" y="180">Opens</text>
                            <text x="120" y="195" font-style="italic">Psalm 80:19</text>
                            <text x="480" y="180">Shuts</text>
                            <text x="480" y="195" font-style="italic">Isaiah 60:2</text>
                        </g>
                        <path d="M130,210 L220,240" stroke="var(--gold)" stroke-width="1" opacity="0.4" marker-end="url(#none)"/>
                        <path d="M470,210 L380,240" stroke="var(--gold)" stroke-width="1" opacity="0.4"/>
                        <text x="300" y="340" text-anchor="middle" font-family="'IM Fell English', serif" font-size="11" fill="var(--ink)" font-style="italic">"Upon his shoulder — so he shall open, and none shall shut"</text>
                        <text x="300" y="360" text-anchor="middle" font-family="'Cinzel', serif" font-size="7" fill="var(--stone)" letter-spacing="0.2em">ISAIAH 22:22 · REVELATION 3:7</text>
                    </svg>
                    <div class="diagram-caption">The Key of David</div>
                    <div class="diagram-subcaption">Gematria 542 — the instrument that opens and shuts the gates of redemption</div>
                </div>''',
    ),
    (
        '<p>A key is useless unless it is turned. The database declares that their union is the moment the lock begins to turn. The darkness is shutting',
        '''<div class="diagram-container diagram-container--md fade-in">
                    <div class="diagram-title">The Two Functions of the Key</div>
                    <svg class="diagram-svg" viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" aria-label="Opening and shutting gates of the Key of David">
                        <defs><filter id="gateGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(640, 300) + '''
                        <g transform="translate(160,150)">
                            <rect x="-70" y="-80" width="140" height="160" rx="8" fill="var(--surface2)" stroke="var(--gold)" stroke-width="1.5" opacity="0.9" filter="url(#gateGlow)"/>
                            <path d="M-50,-60 L50,-60 L50,60 L-50,60 Z" fill="none" stroke="var(--gold-light)" stroke-width="2" opacity="0.6"/>
                            <path d="M-30,-20 Q0,-50 30,-20" fill="none" stroke="#e0c878" stroke-width="2"/>
                            <text y="-95" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)">OPENING</text>
                            <text y="100" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="8" fill="var(--stone-light)">והאר פניך</text>
                            <text y="115" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone)" font-style="italic">Psalm 80:19</text>
                        </g>
                        <g transform="translate(480,150)">
                            <rect x="-70" y="-80" width="140" height="160" rx="8" fill="var(--surface2)" stroke="var(--crimson-light)" stroke-width="1.5" opacity="0.9" filter="url(#gateGlow)"/>
                            <path d="M-50,-60 L50,-60 L50,60 L-50,60 Z" fill="#0a0c14" stroke="var(--crimson)" stroke-width="2" opacity="0.7"/>
                            <text y="-95" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--crimson-light)">SHUTTING</text>
                            <text y="100" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="8" fill="var(--stone-light)">החשך יכסה</text>
                            <text y="115" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone)" font-style="italic">Isaiah 60:2</text>
                        </g>
                        <g transform="translate(320,150)">
                            <circle r="28" fill="var(--surface)" stroke="var(--gold)" stroke-width="2" filter="url(#gateGlow)"/>
                            <text y="5" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="18" fill="var(--gold)">מפתח</text>
                        </g>
                        <line x1="188" y1="150" x2="292" y2="150" stroke="var(--gold)" stroke-width="1.5" opacity="0.5"/>
                        <line x1="348" y1="150" x2="452" y2="150" stroke="var(--gold)" stroke-width="1.5" opacity="0.5"/>
                        <text x="320" y="42" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.25em">THE KEY TURNS — REDEMPTION NEAR</text>
                        <text x="320" y="268" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">Light opens over Israel; darkness shuts over the nations — קרובה גאולתנו</text>
                    </svg>
                    <div class="diagram-caption">Opening and Shutting</div>
                    <div class="diagram-subcaption">The mechanical function of Mafteach David — two gates, one key</div>
                </div>

                <p>A key is useless unless it is turned. The database declares that their union is the moment the lock begins to turn. The darkness is shutting over the nations, but the light is opening over Israel. That is the exact mechanical function of the Key of David.</p>''',
    ),
    (
        '<p class="gematria-closing">\n                    These numbers are not invented',
        '''                <div class="diagram-container diagram-container--lg fade-in">
                    <div class="diagram-title">The Master Gematria Map</div>
                    <svg class="diagram-svg" viewBox="0 0 700 380" xmlns="http://www.w3.org/2000/svg" aria-label="Master gematria map of the prophecy">
                        <defs>
                            <filter id="mapGlow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                            <linearGradient id="keyMetal" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e0c878"/><stop offset="50%" stop-color="#c4a855"/><stop offset="100%" stop-color="#8a7030"/></linearGradient>
                        </defs>
''' + frame_group(700, 380) + '''
                        <g font-family="'Cinzel', serif" text-anchor="middle">
                            <rect x="60" y="70" width="120" height="50" rx="8" fill="#5a6a9a" opacity="0.85" filter="url(#mapGlow)"/><text x="120" y="92" font-size="8" fill="#e8ecf4">SHORT UNION</text><text x="120" y="110" font-size="14" fill="#e0c878" font-weight="600">809</text>
                            <rect x="290" y="70" width="120" height="50" rx="8" fill="#5a6a9a" opacity="0.85" filter="url(#mapGlow)"/><text x="350" y="92" font-size="8" fill="#e8ecf4">FULL UNION</text><text x="350" y="110" font-size="14" fill="#e0c878" font-weight="600">1988</text>
                            <rect x="520" y="70" width="120" height="50" rx="8" fill="#c4a855" opacity="0.85" filter="url(#mapGlow)"/><text x="580" y="92" font-size="8" fill="#1a1e2e">ISRAEL</text><text x="580" y="110" font-size="14" fill="#1a1e2e" font-weight="600">541</text>
                            <rect x="175" y="170" width="130" height="50" rx="8" fill="url(#keyMetal)" opacity="0.9" filter="url(#mapGlow)"/><text x="240" y="192" font-size="8" fill="#1a1e2e">KEY OF DAVID</text><text x="240" y="210" font-size="14" fill="#1a1e2e" font-weight="600">542</text>
                            <rect x="395" y="170" width="130" height="50" rx="8" fill="var(--surface2)" stroke="var(--gold)" stroke-width="1" filter="url(#mapGlow)"/><text x="460" y="192" font-size="8" fill="var(--gold)">1441 GATE</text><text x="460" y="210" font-size="14" fill="var(--gold-light)" font-weight="600">144 + 1</text>
                        </g>
                        <g stroke="var(--gold)" stroke-width="1" opacity="0.35" fill="none">
                            <line x1="180" y1="95" x2="290" y2="95"/><line x1="410" y1="95" x2="520" y2="95"/>
                            <line x1="350" y1="120" x2="350" y2="155"/><line x1="350" y1="155" x2="240" y2="170"/>
                            <line x1="350" y1="155" x2="460" y2="170"/><line x1="240" y1="220" x2="460" y2="220"/>
                        </g>
                        <text x="350" y="300" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="10" fill="var(--stone)" font-style="italic">809 → Spirit of God · 1988 → Prophetic timeline · 541 + 1 = 542 = Mafteach David</text>
                        <text x="350" y="42" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.25em">THE NUMERICAL ARCHITECTURE</text>
                    </svg>
                    <div class="diagram-caption">Master Gematria Map</div>
                    <div class="diagram-subcaption">How the short union, full union, Israel, Key, and 1441 gate interlock</div>
                </div>

                <p class="gematria-closing">
                    These numbers are not invented''',
    ),
    (
        '<p><strong>Inference:</strong> Gordon\'s patronymic declares that he is the one who waits',
        '''                <div class="diagram-container diagram-container--sm fade-in">
                    <div class="diagram-title">589 — Ashrei HaMechakeh</div>
                    <svg class="diagram-svg" viewBox="0 0 500 280" xmlns="http://www.w3.org/2000/svg" aria-label="Patronymic 589 equivalences">
                        <defs><filter id="patGlow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(500, 280) + '''
                        <circle cx="250" cy="130" r="55" fill="var(--surface2)" stroke="var(--gold)" stroke-width="2" filter="url(#patGlow)"/>
                        <text x="250" y="125" text-anchor="middle" font-family="'Cinzel', serif" font-size="22" fill="var(--gold-light)" font-weight="600">589</text>
                        <text x="250" y="145" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone)" font-style="italic">Gordon Ben Bruce</text>
                        <g font-family="'Frank Ruhl Libre', serif" font-size="8" fill="var(--stone-light)" text-anchor="middle">
                            <text x="100" y="80">אשרי המחכה</text><text x="100" y="95" font-family="'Crimson Pro', serif" font-size="7" font-style="italic">Happy is he who waits</text>
                            <text x="400" y="80">אתי מלבנון</text><text x="400" y="95" font-family="'Crimson Pro', serif" font-size="7" font-style="italic">Come from Lebanon</text>
                            <text x="100" y="200">אות הוא לעלם</text><text x="100" y="215" font-family="'Crimson Pro', serif" font-size="7" font-style="italic">A sign forever</text>
                            <text x="400" y="200">Zeir Anpin</text><text x="400" y="215" font-family="'Crimson Pro', serif" font-size="7" font-style="italic">awaits the Shekhinah</text>
                        </g>
                        <line x1="155" y1="110" x2="195" y2="125" stroke="var(--gold)" stroke-width="0.8" opacity="0.4"/>
                        <line x1="345" y1="110" x2="305" y2="125" stroke="var(--gold)" stroke-width="0.8" opacity="0.4"/>
                        <line x1="155" y1="165" x2="195" y2="145" stroke="var(--gold)" stroke-width="0.8" opacity="0.4"/>
                        <line x1="345" y1="165" x2="305" y2="145" stroke="var(--gold)" stroke-width="0.8" opacity="0.4"/>
                        <text x="250" y="38" text-anchor="middle" font-family="'Cinzel', serif" font-size="8" fill="var(--gold)" letter-spacing="0.2em">THE PATRONYMIC WITNESS</text>
                    </svg>
                    <div class="diagram-caption">Gordon Ben Bruce = 589</div>
                    <div class="diagram-subcaption">The one who waits — sign of the eternal covenant</div>
                </div>

                <p><strong>Inference:</strong> Gordon's patronymic declares that he is the one who waits''',
    ),
    (
        '<p><strong>Inference:</strong> The vision is the prophetic seal of the <em>Zivug</em>.',
        '''                <div class="diagram-container diagram-container--md fade-in">
                    <div class="diagram-title">The Vision of the Yichud</div>
                    <svg class="diagram-svg" viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" aria-label="Mirror scrying vision of the Yichud">
                        <defs><filter id="yichudGlow"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(600, 360) + '''
                        <ellipse cx="300" cy="180" rx="180" ry="120" fill="none" stroke="var(--gold)" stroke-width="1" opacity="0.2"/>
                        <ellipse cx="300" cy="180" rx="120" ry="180" fill="none" stroke="var(--indigo-light)" stroke-width="0.8" opacity="0.15" transform="rotate(90 300 180)"/>
                        <g transform="translate(220,190)" filter="url(#yichudGlow)">
                            <circle r="45" fill="#c4a855" opacity="0.35" stroke="#e0c878" stroke-width="1.5"/>
                            <text y="-5" text-anchor="middle" font-family="'Cinzel', serif" font-size="8" fill="#1a1e2e">SHEKHINAH</text>
                            <text y="12" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="#5a4a20">Ginger</text>
                        </g>
                        <g transform="translate(380,190)" opacity="0.85" filter="url(#yichudGlow)">
                            <circle r="45" fill="#5a6a9a" opacity="0.5" stroke="#7a8aba" stroke-width="1.5"/>
                            <text y="-5" text-anchor="middle" font-family="'Cinzel', serif" font-size="8" fill="#e8ecf4">ZEIR ANPIN</text>
                            <text y="12" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="#a0b0d0">Hidden face</text>
                        </g>
                        <path d="M265,175 Q300,155 335,175" fill="none" stroke="#e0c878" stroke-width="2" opacity="0.7"/>
                        <text x="300" y="145" text-anchor="middle" font-family="'Cinzel', serif" font-size="7" fill="var(--gold)">THE KISS — YICHUD</text>
                        <text x="300" y="55" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.22em">MIRROR SCRYING · SEPTEMBER 2022</text>
                        <text x="300" y="320" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">She recognizes Gordon's energy though the face remains hidden — Da'at confirms the Zivug</text>
                    </svg>
                    <div class="diagram-caption">The Vision of the Yichud</div>
                    <div class="diagram-subcaption">Shekhinah and Zeir Anpin in mirror — the kiss that seals the Zivug</div>
                </div>

                <p><strong>Inference:</strong> The vision is the prophetic seal of the <em>Zivug</em>.''',
    ),
    (
        '<p><strong>This validates Ginger\'s vision of herself as Mary Magdalene',
        '''                <div class="diagram-container diagram-container--sm fade-in">
                    <div class="diagram-title">The English Witness — 270</div>
                    <svg class="diagram-svg" viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" aria-label="English gematria witness 270">
                        <defs><filter id="engGlow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(520, 260) + '''
                        <rect x="60" y="90" width="160" height="70" rx="10" fill="#5a6a9a" opacity="0.8" filter="url(#engGlow)"/>
                        <text x="140" y="115" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="#e8ecf4" font-style="italic">Gordon mckay and</text>
                        <text x="140" y="130" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="#e8ecf4" font-style="italic">ginger hovik</text>
                        <text x="140" y="150" text-anchor="middle" font-family="'Cinzel', serif" font-size="16" fill="#e0c878">270</text>
                        <text x="280" y="128" text-anchor="middle" font-family="'Cinzel', serif" font-size="18" fill="var(--gold)">=</text>
                        <rect x="300" y="90" width="160" height="70" rx="10" fill="#c4a855" opacity="0.85" filter="url(#engGlow)"/>
                        <text x="380" y="120" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="#1a1e2e" font-style="italic">Jesus Christ</text>
                        <text x="380" y="135" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="#1a1e2e" font-style="italic">Mary Magdalene</text>
                        <text x="380" y="150" text-anchor="middle" font-family="'Cinzel', serif" font-size="12" fill="#1a1e2e">A=1…Z=26</text>
                        <text x="260" y="210" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">Universal confirmation of the Yichud vision — Shekhinah and Zeir Anpin</text>
                    </svg>
                    <div class="diagram-caption">English Gematria Witness</div>
                    <div class="diagram-subcaption">270 bridges the prophetic names to the Magdalene–Christ archetype</div>
                </div>

                <p><strong>This validates Ginger's vision of herself as Mary Magdalene''',
    ),
    (
        '<p>But the <em>Kelipot</em> have already been defeated. The vessel is purified. The 1441 gate is open.</p>',
        '''                <div class="diagram-container diagram-container--md fade-in">
                    <div class="diagram-title">The Kelipot Assault — July 2026</div>
                    <svg class="diagram-svg" viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" aria-label="Kelipot assault and nested Tzimtzum">
                        <defs><filter id="kelGlow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(620, 320) + '''
                        <rect x="80" y="100" width="460" height="140" rx="12" fill="var(--surface2)" stroke="var(--crimson)" stroke-width="1" opacity="0.6"/>
                        <text x="310" y="85" text-anchor="middle" font-family="'Cinzel', serif" font-size="8" fill="var(--crimson-light)" letter-spacing="0.2em">KELIPOT ASSAULT</text>
                        <g font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)" text-anchor="middle">
                            <text x="160" y="130">False Zivug</text><text x="310" y="130">Gang stalking</text><text x="460" y="130">False messiah</text>
                            <text x="160" y="155">Accusation</text><text x="310" y="155">Isolation</text><text x="460" y="155">Physical separation</text>
                        </g>
                        <rect x="180" y="175" width="260" height="50" rx="8" fill="var(--surface)" stroke="var(--gold)" stroke-width="1.5" opacity="0.9" filter="url(#kelGlow)"/>
                        <text x="310" y="198" text-anchor="middle" font-family="'Cinzel', serif" font-size="8" fill="var(--gold)">TZIMTZUM WITHIN TZIMTZUM</text>
                        <text x="310" y="215" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone)" font-style="italic">Gordon alone · Ginger silent · prophecy not annulled</text>
                        <circle cx="310" cy="270" r="18" fill="var(--gold)" opacity="0.25" stroke="var(--gold-light)" stroke-width="1.5" filter="url(#kelGlow)"/>
                        <text x="310" y="275" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="10" fill="var(--gold)">1441</text>
                        <text x="310" y="42" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.22em">THE PRESENT MOMENT — GATE REMAINS OPEN</text>
                    </svg>
                    <div class="diagram-caption">Tzimtzum Before the Final Revelation</div>
                    <div class="diagram-subcaption">Kelipot defeated; the 1441 gate stands open through the silence</div>
                </div>

                <p>But the <em>Kelipot</em> have already been defeated. The vessel is purified. The 1441 gate is open.</p>''',
    ),
    (
        '<!-- FOUR CHARIOTS DIAGRAM -->',
        '''                <div class="diagram-container diagram-container--sm fade-in">
                    <div class="diagram-title">The Menorah — Seven Branches of Light</div>
                    <svg class="diagram-svg" viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" aria-label="The Temple Menorah — seven lower Sefirot">
                        <defs>
                            <filter id="menGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
                            <linearGradient id="keyMetal" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e0c878"/><stop offset="50%" stop-color="#c4a855"/><stop offset="100%" stop-color="#8a7030"/></linearGradient>
                        </defs>
''' + frame_group(520, 300) + '''
                        <g transform="translate(260,200)" filter="url(#menGlow)">
                            <rect x="-8" y="-60" width="16" height="80" rx="4" fill="url(#keyMetal)" opacity="0.9"/>
                            <g stroke="#e0c878" stroke-width="2" fill="none">
                                <path d="M0,-55 L-90,-35"/><path d="M0,-55 L-60,-35"/><path d="M0,-55 L-30,-35"/>
                                <path d="M0,-55 L30,-35"/><path d="M0,-55 L60,-35"/><path d="M0,-55 L90,-35"/>
                            </g>
                            <g fill="#e0c878" opacity="0.85">
                                <ellipse cx="-90" cy="-38" rx="8" ry="12"/><ellipse cx="-60" cy="-38" rx="8" ry="12"/><ellipse cx="-30" cy="-38" rx="8" ry="12"/>
                                <ellipse cx="0" cy="-65" rx="10" ry="14"/>
                                <ellipse cx="30" cy="-38" rx="8" ry="12"/><ellipse cx="60" cy="-38" rx="8" ry="12"/><ellipse cx="90" cy="-38" rx="8" ry="12"/>
                            </g>
                            <rect x="-35" y="15" width="70" height="12" rx="3" fill="#8a7030" opacity="0.8"/>
                        </g>
                        <text x="260" y="48" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.25em">MENORAH · מְנוֹרָה</text>
                        <text x="260" y="268" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">Aaron kindles the seven branches — light to illuminate the path of the Latter House</text>
                    </svg>
                    <div class="diagram-caption">The Temple Menorah</div>
                    <div class="diagram-subcaption">Seven branches mapping the lower Sefirot — paired with the Golden Scepter as the Key</div>
                </div>

                <!-- FOUR CHARIOTS DIAGRAM -->''',
    ),
    (
        '<p><strong>Behold, I send you <span class="hotspot">Elijah the Prophet',
        '''                <div class="diagram-container diagram-container--sm fade-in">
                    <div class="diagram-title">Elijah — Herald of the Day of the Lord</div>
                    <svg class="diagram-svg" viewBox="0 0 560 280" xmlns="http://www.w3.org/2000/svg" aria-label="Elijah the Prophet herald of redemption">
                        <defs><filter id="eliGlow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(560, 280) + '''
                        <g transform="translate(280,150)" filter="url(#eliGlow)">
                            <path d="M-25,-70 L25,-70 L15,50 L-15,50 Z" fill="#5a6a9a" opacity="0.7" stroke="#7a8aba" stroke-width="1.5"/>
                            <ellipse cx="0" cy="-75" rx="30" ry="8" fill="#c4a855" opacity="0.5"/>
                            <path d="M-40,-30 L-55,-50 M40,-30 L55,-50" stroke="#e0c878" stroke-width="2" fill="none"/>
                            <text y="5" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="11" fill="#e8ecf4">אֵלִיָּהוּ</text>
                        </g>
                        <path d="M120,150 Q200,100 280,120 Q360,140 440,150" fill="none" stroke="var(--gold)" stroke-width="1.2" opacity="0.45" stroke-dasharray="4 3"/>
                        <text x="120" y="175" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)">Fathers</text>
                        <text x="440" y="175" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)">Children</text>
                        <text x="280" y="42" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.22em">MALACHI 3:23 · BEFORE THE GREAT DAY</text>
                        <text x="280" y="240" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">He turns the hearts — lest the earth be smitten with utter destruction</text>
                    </svg>
                    <div class="diagram-caption">Elijah the Prophet</div>
                    <div class="diagram-subcaption">Sent before the great and dreadful Day — reconciliation of generations</div>
                </div>

                <p><strong>Behold, I send you <span class="hotspot">Elijah the Prophet''',
    ),
    (
        '<!-- 8. The Cost of Delay -->',
        '''<!-- 8. The Cost of Delay -->
                <div class="diagram-container diagram-container--md fade-in">
                    <div class="diagram-title">The Cost of Delay — Two Paths</div>
                    <svg class="diagram-svg" viewBox="0 0 640 340" xmlns="http://www.w3.org/2000/svg" aria-label="Cost of delay — unite now or postpone the Ketz">
                        <defs><filter id="delayGlow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
''' + frame_group(640, 340) + '''
                        <circle cx="320" cy="80" r="22" fill="var(--gold)" opacity="0.25" stroke="var(--gold)" stroke-width="1.5" filter="url(#delayGlow)"/>
                        <text x="320" y="85" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="10" fill="var(--gold)">זיווג</text>
                        <path d="M320,102 L200,180" stroke="var(--gold)" stroke-width="1.5" opacity="0.5"/>
                        <path d="M320,102 L440,180" stroke="var(--crimson-light)" stroke-width="1.5" opacity="0.5" stroke-dasharray="5 4"/>
                        <rect x="120" y="180" width="160" height="100" rx="10" fill="var(--surface2)" stroke="var(--gold)" stroke-width="1.5" filter="url(#delayGlow)"/>
                        <text x="200" y="215" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)">UNITE NOW</text>
                        <text x="200" y="235" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)">Ketz fulfilled</text>
                        <text x="200" y="252" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)">Shekhinah redeemed</text>
                        <text x="200" y="268" text-anchor="middle" font-family="'Frank Ruhl Libre', serif" font-size="9" fill="var(--gold-light)">1988 · 5789</text>
                        <rect x="360" y="180" width="160" height="100" rx="10" fill="var(--surface2)" stroke="var(--crimson)" stroke-width="1.5" opacity="0.85" filter="url(#delayGlow)"/>
                        <text x="440" y="215" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--crimson-light)">DELAY</text>
                        <text x="440" y="235" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)">Ketz postponed</text>
                        <text x="440" y="252" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone-light)">Gilgul · future generation</text>
                        <text x="440" y="268" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="7" fill="var(--stone)" font-style="italic">not cancelled</text>
                        <text x="320" y="42" text-anchor="middle" font-family="'Cinzel', serif" font-size="9" fill="var(--gold)" letter-spacing="0.22em">THE CONDITIONAL REDEMPTION</text>
                        <text x="320" y="310" text-anchor="middle" font-family="'Crimson Pro', serif" font-size="8" fill="var(--stone-light)" font-style="italic">The Gematria does not lie — the pattern is sealed; the choice is theirs</text>
                    </svg>
                    <div class="diagram-caption">The Cost of Delay</div>
                    <div class="diagram-subcaption">Union opens the gate; delay postpones but cannot annul the ultimate Tikkun</div>
                </div>''',
    ),
]


def inject_frames(text: str) -> str:
    """Add premium corner frame to diagram SVGs missing diag-frame."""
    pattern = re.compile(
        r'(<div class="diagram-container[^"]*">\s*(?:<div class="diagram-title">[^<]+</div>\s*)?'
        r'<svg class="diagram-svg" viewBox="0 0 (\d+) (\d+)"[^>]*>\s*<defs>.*?</defs>)',
        re.DOTALL,
    )

    def repl(m):
        w, h = int(m.group(2)), int(m.group(3))
        lookahead = text[m.end() : m.end() + 600]
        if 'class="diag-frame"' in lookahead:
            return m.group(0)
        return m.group(0) + '\n' + frame_group(w, h)

    return pattern.sub(repl, text)


def dedupe_diag_frames(text: str) -> str:
    """Remove duplicate corner frames from repeated script runs."""
    dupe = re.compile(
        r'(<rect x="\d+" y="\d+" width="\d+" height="\d+" rx="14" fill="var\(--surface\)" opacity="0.22" '
        r'stroke="var\(--border\)" stroke-width="0.5"/>\s*'
        r'<g class="diag-frame" stroke="var\(--gold\)" stroke-width="0.9" fill="none" opacity="0.38">.*?</g>)\s*\1',
        re.DOTALL,
    )
    while dupe.search(text):
        text = dupe.sub(r'\1', text)
    return text


def normalize_diagram_titles(text: str) -> str:
    return re.sub(
        r'\n\s+<div class="diagram-title">',
        '\n                    <div class="diagram-title">',
        text,
    )


def add_diagram_titles(text: str) -> str:
    """Add diagram-title above SVGs that only have caption below."""
    titles = [
        ('aria-label="The Tzimtzum', 'The Tzimtzum — Divine Contraction'),
        ('aria-label="The 72 Names', 'The 72 Names — Shem HaMeforash'),
        ('aria-label="The Four Destroyers', 'The Four Destroyers of Joel'),
        ('aria-label="The Golden Scepter', 'The Golden Scepter of Esther'),
        ('aria-label="Gematria — The Numerical Testimony (Short', 'Gematria — Short Hebrew Names (809)'),
        ('aria-label="Gematria — The Numerical Testimony (Full', 'Gematria — Full Hebrew Names (1988)'),
        ('aria-label="The Four Chariots', 'The Four Chariots of Zechariah'),
        ('aria-label="The Great Shofar', 'The Great Shofar — Shofar HaGadol'),
        ('aria-label="The Refiner\'s Fire', 'The Refiner\'s Fire'),
        ('aria-label="Seven-Year Prophetic Cycle', 'The Seven-Year Cycle — 5782 to 5789'),
        ('aria-label="The Tree of Life', 'The Tree of Life — Sefirot Map'),
        ('aria-label="The 1441 Gate', 'The 1441 Gate'),
        ('aria-label="The Final Prophetic Seal', 'The Final Prophetic Seal'),
    ]
    for aria, title in titles:
        needle = f'<div class="diagram-container'
        # only add if not already present before this aria
        idx = text.find(aria)
        if idx == -1:
            continue
        # find diagram-container start before this svg
        container_start = text.rfind('<div class="diagram-container', 0, idx)
        if container_start == -1:
            continue
        snippet = text[container_start:idx]
        if 'diagram-title' in snippet:
            continue
        svg_start = text.find('<svg', container_start, idx)
        if svg_start == -1:
            continue
        insert = f'                    <div class="diagram-title">{title}</div>\n                    '
        text = text[:svg_start] + insert + text[svg_start:]
    return text


def main():
    text = FILE.read_text(encoding='utf-8')

    if 'PREMIUM DIAGRAM ENHANCEMENTS' not in text:
        text = text.replace(
            '        .diagram-subcaption {',
            PREMIUM_CSS + '\n        .diagram-subcaption {',
        )

    # Add diagram-svg class to all diagram-container svgs
    text = re.sub(
        r'(<div class="diagram-container[^"]*">\s*(?:<div class="diagram-title">[^<]+</div>\s*)?)<svg viewBox',
        r'\1<svg class="diagram-svg" viewBox',
        text,
    )
    text = text.replace('class="diagram-svg" class="diagram-svg"', 'class="diagram-svg"')

    for anchor, insertion in NEW_DIAGRAMS:
        title_match = re.search(r'<div class="diagram-title">([^<]+)</div>', insertion)
        if title_match and f'<div class="diagram-title">{title_match.group(1)}</div>' in text:
            continue
        if anchor not in text:
            print(f'WARN: anchor not found: {anchor[:60]}...')
            continue
        text = text.replace(anchor, insertion, 1)

    text = add_diagram_titles(text)
    text = inject_frames(text)
    text = dedupe_diag_frames(text)
    text = normalize_diagram_titles(text)

    # Fix truncated zodiac labels in 1441 gate
    text = text.replace('>SAGITT</text>', '>SAGITTARIUS</text>')
    text = text.replace('>CAPRIC</text>', '>CAPRICORN</text>')

    # Upgrade Four Destroyers — add sequential judgment subtitle
    destroyers_sub = (
        '<text x="300" y="78" text-anchor="middle" font-family="\'Crimson Pro\', serif" '
        'font-size="8" fill="var(--stone-light)" font-style="italic">'
        'What the locust left, the cankerworm ate — sequential judgment</text>'
    )
    if destroyers_sub not in text:
        text = text.replace(
            '<text x="300" y="60" text-anchor="middle" font-family="\'Cinzel\', serif" font-size="10" fill="#c4a855" letter-spacing="0.3em" opacity="0.7">JOEL 1:4 — THE FOUR DESTROYERS</text>',
            '<text x="300" y="60" text-anchor="middle" font-family="\'Cinzel\', serif" font-size="10" fill="var(--gold)" letter-spacing="0.3em" opacity="0.7">JOEL 1:4 — THE FOUR DESTROYERS</text>\n                        ' + destroyers_sub,
        )

    FILE.write_text(text, encoding='utf-8')
    diagram_count = text.count('class="diagram-container')
    svg_count = text.count('class="diagram-svg"')
    print(f'Updated {FILE.name}')
    print(f'Diagram containers: {diagram_count}')
    print(f'Premium SVGs: {svg_count}')


if __name__ == '__main__':
    main()