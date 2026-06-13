# DONE: Refactor ramana-maharshi.html + nisargadatta-maharaj.html to unified nav-compass

**Completed as high-priority item (June 2026).**

- Both flagship Advaita cartographies now use the floating nav-compass (matching Taoism + Messiah series).
- Sidebar, progress bars, reading time, old toggles removed.
- Internal section navigation + full cross-series links in dropdowns.
- Footers standardized with complete links (Taoism added to Ramana).
- Chapter nav added for Ramana for flow.
- Clean JS for nav/theme/back-to-top + retained page-specific interactions.

See git history or the files for details. The original plan below is kept for reference.

## Current State Analysis

### Ramana sidebar structure:
- Permanent sidebar on left (260px wide, always visible on desktop)
- Collapsible via hamburger toggle
- Reading progress bar in sidebar
- Top progress bar at page top
- Reading time indicator
- Sections: Primary (Home, Origin, Transmission, Roots), Teaching (Stages, Practice, Works)
- Main content has margin-left: 260px to accommodate sidebar
- Close button in sidebar header
- Mobile: sidebar slides in/out with backdrop

### Taoism nav-compass structure:
- Floating nav-compass (top-left hamburger menu, 44px)
- Dropdown menu that toggles open/close
- No permanent space taken (full-width content)
- No reading progress bars
- No reading time indicators
- Sections: The Cartographies (Home), Advaita Vedanta, Comparative, Taoism (cross-site links)
- Simple JavaScript toggle logic
- Back-to-top and theme-toggle buttons

## Implementation Steps

### 1. CSS Changes
- **DELETE**: All sidebar-related CSS (`.sidebar`, `.sidebar-*`, `.sidebar-backdrop`, `.sidebar-toggle`, `.sidebar-close-btn`, `.sidebar-header`, `.sidebar-logo`, `.sidebar-title`, `.sidebar-nav`, `.sidebar-nav-*`, `.sidebar-progress`)
- **DELETE**: `.main-content` margin-left: 260px and transition
- **DELETE**: Top progress bar CSS (`#topProgress`, progress bars)
- **DELETE**: Reading info bar CSS (`.reading-info`)
- **DELETE**: Reading progress tracking CSS
- **ADD**: nav-compass CSS from taoism-threshold.html (`.nav-compass`, `.nav-toggle`, `.nav-menu`, `.nav-item`, `.nav-item-icon`, `.nav-section-title`, `.nav-divider`, `.nav-menu.open`)
- **DELETE**: Skip link CSS (if present)
- **ADD**: Taoism-style theme-toggle CSS (simple sun/moon icons)
- **DELETE**: Complex theme-toggle with toggle-tooltip
- **ADD**: Taoism-style back-to-top CSS

### 2. HTML Structure Changes
- **DELETE**: Skip link
- **DELETE**: Top progress bar `<div id="topProgress">`
- **DELETE**: Entire sidebar structure (`<div class="sidebar-backdrop">` through closing `</nav>`)
- **DELETE**: Sidebar toggle button inside main-content
- **DELETE**: Reading info bar
- **DELETE**: Reading time-left indicator
- **DELETE**: Theme toggle tooltip
- **ADD**: nav-compass structure at top of body:
  - `<div class="nav-compass">` with hamburger toggle
  - `<div class="nav-menu">` with dropdown content
- **RETAIN**: Main content wrapper (remove margin-left dependency)
- **ADD**: Navigation structure adapted for Ramana's page sections (internal page links instead of cross-site links)
- **RETAIN**: Hero section and all content sections
- **UPDATE**: Theme toggle button to Taoism simple style (text emojis ☀/☾)
- **UPDATE**: Back-to-top button to Taoism style

### 3. JavaScript Changes
- **DELETE**: All sidebar-related JavaScript (sidebar, sidebarToggle, sidebarCloseBtn, sidebarBackdrop, isMobile, openSidebar, closeSidebar, toggleSidebar, initSidebar)
- **DELETE**: Progress bar tracking (topProgress, progressFill, progressPercent, readingInfo, readingTimeLeft, TOTAL_WORDS, ticking logic)
- **DELETE**: Scroll progress observer if present
- **ADD**: nav-compass JavaScript from Taoism:
  - Simple toggle: `navMenu.classList.toggle('open')`
  - Click outside to close menu
- **UPDATE**: Theme toggle JavaScript to simple text-based toggling
- **UPDATE**: Back-to-top logic to Taoism style (simple scrollY check)
- **DELETE**: Resize-based responsive logic (no longer needed)

### 4. Navigation Content
- **REPLACE**: Cross-site navigation links with Ramana-specific navigation:
  - Instead of "The Cartographies" section with cross-links to other series, use internal page sections
  - Sections to include: Primary (Home, Origin, Transmission, Roots), Teaching (Stages, Practice, Works), Sources (if applicable)
- **RETAIN**: Internal page section icons and structure from current sidebar
- **ADD**: Section dividers like Taoism uses
- **KEEP**: Same icons and text labels from current sidebar

### 5. Content Adjustments
- **REMOVE**: Hero reading badge (~35 min read) if present
- **REMOVE**: Any reading time or progress indicators
- **RETAIN**: All content sections (hero, origin, transmission, roots, stages, practice, works, sources)
- **RETAIN**: All interactive elements (tooltips, glossary, etc.)

### 6. Responsive Changes
- **DELETE**: Sidebar-specific responsive breakpoints (max-width: 1100px mobile sidebar logic)
- **DELETE**: Main-content margin-left changes
- **DELETE**: Backdrop display logic
- **DELETE**: Resize-based sidebar logic
- **ADD**: Taoism responsive CSS if any (mobile menu styling)

## Summary of Changes
- **CSS**: ~100 lines to delete, ~30 lines to add
- **HTML**: ~50 lines to delete, ~20 lines to add
- **JavaScript**: ~80 lines to delete, ~15 lines to add
- **Navigation**: Convert from permanent sidebar to floating dropdown
- **Layout**: Full-width content (no sidebar space allocation)
- **Features**: Remove reading progress, keep all content and interactions

## Risks
- **Major structural change**: Could temporarily break navigation if not done carefully
- **JavaScript logic**: Need to ensure new toggle works correctly
- **Mobile experience:** Ensure dropdown works well on touch devices
- **Section active states:** Need to maintain active state for current section
- **Smooth scroll:** Verify smooth scrolling to sections still works

## Reference Files
- Target: `/Users/g/Desktop/vedantic-mappings/taoism/taoism-threshold.html` (nav-compass style)
- Source: `/Users/g/Desktop/vedantic-mappings/advaita-vedanta/ramana-maharshi.html` (current sidebar style)
