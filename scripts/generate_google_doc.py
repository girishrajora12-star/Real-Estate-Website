#!/usr/bin/env python3
"""
Generates a downloadable, beautifully styled document (.docx and .doc)
containing the complete Google AI Studio master prompt and video walkthrough reference.
Compatible with Google Docs, Microsoft Word, and LibreOffice.
"""
import os
import zipfile
import html

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_DIR = os.path.join(PROJECT_ROOT, "public", "downloads")
DIST_DOWNLOADS_DIR = os.path.join(PROJECT_ROOT, "dist", "downloads")

os.makedirs(DOWNLOADS_DIR, exist_ok=True)
os.makedirs(DIST_DOWNLOADS_DIR, exist_ok=True)

DOCX_PATH = os.path.join(DOWNLOADS_DIR, "Google_AI_Studio_Architecture_Prompt.docx")
DOC_PATH = os.path.join(DOWNLOADS_DIR, "Google_AI_Studio_Architecture_Prompt.doc")
DIST_DOCX_PATH = os.path.join(DIST_DOWNLOADS_DIR, "Google_AI_Studio_Architecture_Prompt.docx")
DIST_DOC_PATH = os.path.join(DIST_DOWNLOADS_DIR, "Google_AI_Studio_Architecture_Prompt.doc")

PROMPT_TEXT = """Build a luxury, cinematic architectural showcase web application named "KAVAL Architecture & Interiors". The core signature feature of the website is a scroll-controlled frame-by-frame villa walkthrough on the landing page hero, accompanied by editorial typography, smooth inertial scroll interactions, and interactive project inspection.

1. TYPOGRAPHY & STYLING THEME
- Font Integration: Integrate Adobe Typekit font Degular via:
  <link rel="stylesheet" href="https://use.typekit.net/rug2hhm.css">
- Font Family: font-family: 'degular', sans-serif;
- Typographic Hierarchy:
  * Big headings (h1, h2, hero chapters, section headlines, preloader, CTA titles): font-family: 'degular', sans-serif; font-weight: 500; font-style: normal; (Medium).
  * Small headings (h3-h6, card titles, project titles, modal titles, footer titles, kickers): font-family: 'degular', sans-serif; font-weight: 400; font-style: normal; (Regular).
  * Body copy, descriptions, navigation links, buttons, form inputs: font-family: 'degular', sans-serif; font-weight: 400; font-style: normal;.
- Color Palette:
  * Deep Charcoal: #101010 (Hero, projects, and footer background)
  * Warm Architectural Cream: #F3EFE6 (Intro cards section background)
  * Raw Teak Accent: #8A4B22 / #A85A28
  * Radiant Amber: #F2A24B (Accents, highlights, active states)
  * Pure White: #FFFFFF
  * Muted Slate: #8E8A82
- Global Feel: High-end editorial, generous whitespace, zero pill-shaped AI slop, subtle 1px translucent borders (rgba(255, 255, 255, 0.08)), bespoke custom cursor with difference blend mode.

2. VIDEO WALKTHROUGH LANDING PAGE (SECTION 1)
- Asset: Uses "public/assets/House Walkthrough Website.mp4" (~20s 1080p architectural villa walkthrough).
- Extraction Pipeline:
  * Provide a Python script (scripts/extract_frames.py) using ffmpeg to extract ~300 high-resolution JPEG frames into public/assets/frames/frame_0001.jpg to frame_0300.jpg, scaling to 1080p and saving a manifest.json.
  * Connect a Vite build plugin in vite.config.ts to automatically trigger extraction on server boot if frames do not yet exist.
- Canvas Scroll Scrubbing:
  * The hero section takes 100vw and 100vh and is pinned for 400% scroll distance using GSAP ScrollTrigger.
  * An HTML5 <canvas id="heroCanvas"> scales to device pixel ratio and renders frames using aspect-ratio cover math.
  * Frame 1 is loaded and painted immediately on page load to eliminate blank states.
  * Progressive background preloading buffers every 3rd frame first, then fills in remaining frames during browser idle time.
  * A tick() animation loop applies smoothing interpolation between scroll position and target frame index.
  * No Video Selector / Upload UI: Do not display any video selector buttons, file input pickers, or dropzone overlays on the landing page. The site immediately and automatically scrubs the extracted frames.
- Dynamic Chapters:
  * As the video advances, 12 minimalist two-line editorial chapter headlines fade in and out at key timestamps:
    1. 0.0s: "Where tradition / meets modern living."
    2. 1.8s: "Step through / solid teak."
    3. 3.4s: "Warm light / greets you."
    4. 5.2s: "Space made / for family."
    5. 7.0s: "Where every meal / gathers you."
    6. 8.8s: "Light, open / and effortless."
    7. 10.6s: "Rise through / glass and wood."
    8. 12.4s: "See your home / from above."
    9. 14.2s: "A quiet corner, / upstairs."
    10. 16.0s: "Private spaces, / thoughtfully placed."
    11. 17.8s: "Wake up / to calm."
    12. 19.2s: "End every day / with this view."
- Hero Metadata & Indicator:
  * Vertical scrub progress bar on the right.
  * Circular rotating SVG badge: "SCROLL TO WALK THROUGH • FRAME BY FRAME • ".
  * Upon reaching 100% of the video walkthrough, Section 1 unpins seamlessly into Section 2 with 0px gap.

3. SUBSEQUENT INTERACTIVE SECTIONS
- Section 2: Spaces & Materiality
  * Warm cream background #F3EFE6 with charcoal text.
  * Split headline reveal: "Homes. Spaces. Stories. Details."
  * Search filter input to dynamically filter cards by room or material (e.g. Living, Teak, Courtyard).
  * 4 Parallax floating room cards (Living Sanctuary, Courtyard Atrium, Floating Mezzanine, Master Suite) with interactive heart favorite toggles and modal detail triggers.
- Section 3: Kerala Contemporary Villa 3D Elevation
  * Full-width architectural exterior render background.
  * Heading: "Stunning Double Floor 3D Elevation" in pure black (#000000) with Degular Medium (500).
  * Subheading: "Click on any architectural detail to inspect craftsmanship & material specifications." in pure black (#000000) with Degular Regular (400).
  * No top category kicker text.
  * 3 Pulsing interactive glassmorphism tags (Teak wood cladding, Smart climate architecture, Warm pendant illumination) that trigger a side inspection modal with material specs and origin data.
- Section 4: Architectural Index / Projects
  * Minimalist numbered row list (/01 Kerala Villa, /02 Uluwatu Cliff House, /03 Kyoto Timber Pavilion).
  * Hovering a row smoothly expands a floating elevation thumbnail and reveals /See more.
- Section 5: The Architectural Process
  * 4 Horizontal step cards (Site & Microclimate Analysis, Monolithic Concept Modelling, Material & Joinery Craftsmanship, Turnkey Execution).
- Section 6: Footer & Commission Inquiry
  * Infinite animated marquee of design disciplines.
  * Big headline: "Have an architectural dream?" with magnetic circular CTA button "Start Commission".
  * Accessible dialog modal with inquiry form (Full Name, Email, Site Location, Architectural Brief).

4. TECHNICAL STACK & DEPENDENCIES
- React + Vite + TypeScript (or vanilla HTML5/JS with GSAP).
- GSAP 3 + ScrollTrigger for scroll pinning and timeline orchestration.
- Tailwind CSS 4 for styling utilities.
- Clean modular codebase, zero console warnings, fast first contentful paint."""

def create_rich_doc():
    """Generates an HTML-based .doc file fully formatted for Google Docs and Word."""
    content = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head>
<meta charset='utf-8'>
<title>Google AI Studio Master Prompt &amp; Video Reference Guide</title>
<style>
  body {{
    font-family: Arial, Helvetica, sans-serif;
    color: #1a1a1a;
    line-height: 1.6;
    margin: 40px;
    background-color: #ffffff;
  }}
  h1 {{
    font-size: 26pt;
    color: #101010;
    margin-bottom: 4px;
    font-weight: 700;
    border-bottom: 2px solid #F2A24B;
    padding-bottom: 8px;
  }}
  .subtitle {{
    font-size: 13pt;
    color: #8A4B22;
    margin-top: 0;
    margin-bottom: 24px;
    font-weight: 600;
  }}
  h2 {{
    font-size: 16pt;
    color: #101010;
    margin-top: 28px;
    margin-bottom: 12px;
    padding-bottom: 4px;
    border-bottom: 1px solid #e0ded8;
  }}
  h3 {{
    font-size: 13pt;
    color: #333333;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  p, li {{
    font-size: 11pt;
    color: #2b2b2b;
  }}
  .callout {{
    background-color: #fbf9f4;
    border-left: 4px solid #F2A24B;
    padding: 14px 18px;
    margin: 18px 0;
    border-radius: 4px;
  }}
  .prompt-box {{
    background-color: #0f1115;
    color: #f4efe6;
    padding: 20px 24px;
    border-radius: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10pt;
    line-height: 1.55;
    white-space: pre-wrap;
    word-break: break-word;
    border: 1px solid #333;
    margin: 20px 0;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 10.5pt;
  }}
  th, td {{
    border: 1px solid #dcd7cc;
    padding: 10px 14px;
    text-align: left;
  }}
  th {{
    background-color: #f5f2ea;
    font-weight: 700;
    color: #111;
  }}
  tr:nth-child(even) {{
    background-color: #faf8f5;
  }}
  .badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 9pt;
    font-weight: bold;
    background-color: #F2A24B;
    color: #000;
  }}
</style>
</head>
<body>

<h1>Google AI Studio Master Prompt &amp; Video Reference</h1>
<p class='subtitle'>KAVAL Architecture &amp; Interiors &bull; Frame-by-Frame Scroll Walkthrough Blueprint</p>

<div class='callout'>
  <strong>How to open in Google Docs:</strong><br>
  1. Go to <strong>drive.google.com</strong> or <strong>docs.google.com</strong>.<br>
  2. Click <strong>+ New &gt; File upload</strong> and select this file.<br>
  3. Open the uploaded file in Google Docs &mdash; all formatting, headings, and prompt text will be perfectly preserved.
</div>

<h2>Part 1: Video Reference Specifications</h2>
<p>This section documents the exact video file and timeline breakdown used for the hero scroll-scrubbed walkthrough on the landing page.</p>

<table>
  <tr>
    <th style="width: 25%;">Property</th>
    <th>Specification</th>
  </tr>
  <tr>
    <td><strong>File Name</strong></td>
    <td><code>House Walkthrough Website.mp4</code></td>
  </tr>
  <tr>
    <td><strong>Storage Location</strong></td>
    <td><code>public/assets/House Walkthrough Website.mp4</code></td>
  </tr>
  <tr>
    <td><strong>Duration</strong></td>
    <td>20.065 seconds</td>
  </tr>
  <tr>
    <td><strong>Resolution</strong></td>
    <td>1918 x 1080 (Full HD Landscape)</td>
  </tr>
  <tr>
    <td><strong>Extracted Frames Target</strong></td>
    <td>300 frames (15 frames/sec) saved as <code>public/assets/frames/frame_0001.jpg</code> ... <code>frame_0300.jpg</code></td>
  </tr>
  <tr>
    <td><strong>Hero Pin Distance</strong></td>
    <td>400% of viewport scroll (GSAP ScrollTrigger pin)</td>
  </tr>
</table>

<h3>Timeline &amp; Scene Breakdown (12 Chapters)</h3>
<table>
  <tr>
    <th style="width: 15%;">Timestamp</th>
    <th style="width: 35%;">Room / Camera Perspective</th>
    <th>Editorial Chapter Overlay (2 Lines)</th>
  </tr>
  <tr>
    <td><strong>00:00 - 01:80</strong></td>
    <td>Exterior villa approach, golden hour facade and entry portico</td>
    <td>Where tradition<br>meets modern living.</td>
  </tr>
  <tr>
    <td><strong>01:80 - 03:40</strong></td>
    <td>Solid Indonesian teak double pivot door opening</td>
    <td>Step through<br>solid teak.</td>
  </tr>
  <tr>
    <td><strong>03:40 - 05:20</strong></td>
    <td>Entry foyer with warm ambient natural lighting</td>
    <td>Warm light<br>greets you.</td>
  </tr>
  <tr>
    <td><strong>05:20 - 07:00</strong></td>
    <td>Formal living sanctuary with monolithic stone feature wall</td>
    <td>Space made<br>for family.</td>
  </tr>
  <tr>
    <td><strong>07:00 - 08:80</strong></td>
    <td>Open dining space with handcrafted teak dining table</td>
    <td>Where every meal<br>gathers you.</td>
  </tr>
  <tr>
    <td><strong>08:80 - 10:60</strong></td>
    <td>Internal daylight courtyard with natural cross-ventilation</td>
    <td>Light, open<br>and effortless.</td>
  </tr>
  <tr>
    <td><strong>10:60 - 12:40</strong></td>
    <td>Floating architectural staircase with glass balustrade</td>
    <td>Rise through<br>glass and wood.</td>
  </tr>
  <tr>
    <td><strong>12:40 - 14:20</strong></td>
    <td>Mezzanine walkway looking down into double-height void</td>
    <td>See your home<br>from above.</td>
  </tr>
  <tr>
    <td><strong>14:20 - 16:00</strong></td>
    <td>Upper quiet retreat, study library and seating nook</td>
    <td>A quiet corner,<br>upstairs.</td>
  </tr>
  <tr>
    <td><strong>16:00 - 17:80</strong></td>
    <td>Private residential hallway with discrete flush doors</td>
    <td>Private spaces,<br>thoughtfully placed.</td>
  </tr>
  <tr>
    <td><strong>17:80 - 19:20</strong></td>
    <td>Master suite sanctuary bathed in soft morning clarity</td>
    <td>Wake up<br>to calm.</td>
  </tr>
  <tr>
    <td><strong>19:20 - 20:06</strong></td>
    <td>Sunset balcony terrace with panoramic tropical horizon</td>
    <td>End every day<br>with this view.</td>
  </tr>
</table>

<h2>Part 2: Complete Single-Turn Google AI Studio Master Prompt</h2>
<p>Copy and paste the entire block below into Google AI Studio Build to generate the complete website:</p>

<div class='prompt-box'>{html.escape(PROMPT_TEXT)}</div>

<h2>Part 3: Quick Instructions for Google AI Studio Build</h2>
<ol>
  <li><strong>Start Project</strong>: Open Google AI Studio Build (<a href="https://aistudio.google.com/">aistudio.google.com</a>) and click <em>Create Applet</em>.</li>
  <li><strong>Paste Master Prompt</strong>: Paste the prompt from Part 2 into the prompt bar.</li>
  <li><strong>Provide Video</strong>: Place <code>House Walkthrough Website.mp4</code> into <code>public/assets/</code>.</li>
  <li><strong>Run</strong>: The build engine will assemble the application, extract frames, configure the Degular font, and render the interactive architectural showcase.</li>
</ol>

<hr style="border: none; border-top: 1px solid #e0ded8; margin: 40px 0 20px;">
<p style="font-size: 9.5pt; color: #8E8A82; text-align: center;">KAVAL Architecture &amp; Interiors &bull; Generated for Google AI Studio Build &bull; 2026</p>

</body>
</html>
"""
    with open(DOC_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    with open(DIST_DOC_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated .doc file at: {DOC_PATH}")

def create_docx():
    """Builds a valid, standard OpenXML .docx file using Python zipfile."""
    # Convert prompt text into WordprocessingML paragraphs
    prompt_paragraphs = ""
    for line in PROMPT_TEXT.splitlines():
        escaped_line = html.escape(line)
        if not line.strip():
            prompt_paragraphs += '<w:p><w:pPr><w:spacing w:after="80"/></w:pPr></w:p>'
        elif line.startswith(("1.", "2.", "3.", "4.")):
            prompt_paragraphs += f'<w:p><w:pPr><w:pStyle w:val="Heading3"/><w:spacing w:before="180" w:after="80"/></w:pPr><w:r><w:rPr><w:b/><w:color w:val="F2A24B"/></w:rPr><w:t>{escaped_line}</w:t></w:r></w:p>'
        elif line.strip().startswith("-"):
            prompt_paragraphs += f'<w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:color w:val="E2DFD8"/></w:rPr><w:t>{escaped_line}</w:t></w:r></w:p>'
        elif line.strip().startswith("*"):
            prompt_paragraphs += f'<w:p><w:pPr><w:ind w:left="720"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:color w:val="D0CBC0"/></w:rPr><w:t>{escaped_line}</w:t></w:r></w:p>'
        else:
            prompt_paragraphs += f'<w:p><w:pPr><w:spacing w:after="80"/></w:pPr><w:r><w:rPr><w:color w:val="FFFFFF"/></w:rPr><w:t>{escaped_line}</w:t></w:r></w:p>'

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    <!-- Document Title -->
    <w:p>
      <w:pPr>
        <w:pStyle w:val="Title"/>
        <w:spacing w:after="120"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:sz w:val="52"/>
          <w:color w:val="101010"/>
        </w:rPr>
        <w:t>Google AI Studio Master Prompt &amp; Video Reference</w:t>
      </w:r>
    </w:p>

    <w:p>
      <w:pPr>
        <w:pStyle w:val="Subtitle"/>
        <w:spacing w:after="300"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:sz w:val="26"/>
          <w:color w:val="8A4B22"/>
        </w:rPr>
        <w:t>KAVAL Architecture &amp; Interiors • Frame-by-Frame Scroll Walkthrough Blueprint</w:t>
      </w:r>
    </w:p>

    <!-- Notice Box -->
    <w:p>
      <w:pPr>
        <w:pBdr>
          <w:left w:val="single" w:sz="24" w:space="12" w:color="F2A24B"/>
        </w:pBdr>
        <w:shd w:val="clear" w:color="auto" w:fill="FBF9F4"/>
        <w:spacing w:before="120" w:after="240"/>
        <w:ind w:left="240" w:right="240"/>
      </w:pPr>
      <w:r>
        <w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="101010"/></w:rPr>
        <w:t>How to open in Google Docs: </w:t>
      </w:r>
      <w:r>
        <w:rPr><w:sz w:val="22"/><w:color w:val="333333"/></w:rPr>
        <w:t>Upload this .docx file directly to Google Drive (drive.google.com) and click "Open with Google Docs". All typography, headings, tables, and prompt formatting will display flawlessly.</w:t>
      </w:r>
    </w:p>

    <!-- Section 1 -->
    <w:p>
      <w:pPr>
        <w:pStyle w:val="Heading1"/>
        <w:spacing w:before="360" w:after="160"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:sz w:val="36"/>
          <w:color w:val="101010"/>
        </w:rPr>
        <w:t>1. Video Reference Specifications</w:t>
      </w:r>
    </w:p>

    <w:p>
      <w:pPr><w:spacing w:after="120"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="22"/><w:color w:val="333333"/></w:rPr>
        <w:t>The landing page features a scroll-scrubbed architectural walkthrough powered by the following video assets:</w:t>
      </w:r>
    </w:p>

    <!-- Video Bullet Points -->
    <w:p>
      <w:pPr><w:ind w:left="400"/><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>• Video Asset: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="22"/><w:color w:val="8A4B22"/><w:rFonts w:ascii="Consolas"/></w:rPr><w:t>public/assets/House Walkthrough Website.mp4</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="400"/><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>• Duration &amp; Quality: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t>20.065 seconds, 1918x1080 resolution, 15fps frame rate</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="400"/><w:spacing w:after="80"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>• Extracted Frames: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t>300 sequential frames saved as frame_0001.jpg through frame_0300.jpg in public/assets/frames/</w:t></w:r>
    </w:p>
    <w:p>
      <w:pPr><w:ind w:left="400"/><w:spacing w:after="160"/></w:pPr>
      <w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>• Scroll Behavior: </w:t></w:r>
      <w:r><w:rPr><w:sz w:val="22"/></w:rPr><w:t>Pinned 100vh canvas for 400% scroll distance with 0px gap unpin into Section 2 upon reaching 100%.</w:t></w:r>
    </w:p>

    <!-- Video Timeline Breakdown -->
    <w:p>
      <w:pPr>
        <w:pStyle w:val="Heading2"/>
        <w:spacing w:before="240" w:after="120"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:sz w:val="28"/>
          <w:color w:val="101010"/>
        </w:rPr>
        <w:t>Video Timeline &amp; 12 Scene Chapter Cues</w:t>
      </w:r>
    </w:p>

    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>1. 0.0s – Exterior Villa Facade: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Where tradition / meets modern living."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>2. 1.8s – Solid Teak Entrance Door: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Step through / solid teak."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>3. 3.4s – Welcoming Light Entry Foyer: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Warm light / greets you."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>4. 5.2s – Formal Living Sanctuary: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Space made / for family."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>5. 7.0s – Open Dining Pavilion: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Where every meal / gathers you."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>6. 8.8s – Central Courtyard &amp; Atrium: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Light, open / and effortless."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>7. 10.6s – Floating Glass &amp; Timber Staircase: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Rise through / glass and wood."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>8. 12.4s – Upper Mezzanine Void Overlook: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"See your home / from above."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>9. 14.2s – Upper Floor Library Lounge: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"A quiet corner, / upstairs."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>10. 16.0s – Private Bedroom Hallway: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Private spaces, / thoughtfully placed."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="60"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>11. 17.8s – Master Bedroom Suite: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"Wake up / to calm."</w:t></w:r></w:p>
    <w:p><w:pPr><w:ind w:left="400"/><w:spacing w:after="240"/></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="22"/></w:rPr><w:t>12. 19.2s – Sunset Horizon Balcony: </w:t></w:r><w:r><w:rPr><w:sz w:val="22"/><w:color w:val="555555"/></w:rPr><w:t>"End every day / with this view."</w:t></w:r></w:p>

    <!-- Section 2: Master Prompt -->
    <w:p>
      <w:pPr>
        <w:pStyle w:val="Heading1"/>
        <w:spacing w:before="360" w:after="160"/>
      </w:pPr>
      <w:r>
        <w:rPr>
          <w:rFonts w:ascii="Arial" w:hAnsi="Arial"/>
          <w:b/>
          <w:sz w:val="36"/>
          <w:color w:val="101010"/>
        </w:rPr>
        <w:t>2. Complete Single-Turn Google AI Studio Master Prompt</w:t>
      </w:r>
    </w:p>

    <w:p>
      <w:pPr><w:spacing w:after="160"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="22"/><w:color w:val="333333"/></w:rPr>
        <w:t>Copy and paste the exact text block below directly into Google AI Studio Build:</w:t>
      </w:r>
    </w:p>

    <!-- Prompt Box Container -->
    <w:tbl>
      <w:tblPr>
        <w:tblW w:w="0" w:type="auto"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="8" w:space="0" w:color="333333"/>
          <w:left w:val="single" w:sz="8" w:space="0" w:color="333333"/>
          <w:bottom w:val="single" w:sz="8" w:space="0" w:color="333333"/>
          <w:right w:val="single" w:sz="8" w:space="0" w:color="333333"/>
        </w:tblBorders>
        <w:tblCellMar>
          <w:top w:w="240" w:type="dxa"/>
          <w:left w:w="300" w:type="dxa"/>
          <w:bottom w:w="240" w:type="dxa"/>
          <w:right w:w="300" w:type="dxa"/>
        </w:tblCellMar>
      </w:tblPr>
      <w:tr>
        <w:tc>
          <w:tcPr>
            <w:shd w:val="clear" w:color="auto" w:fill="0F1115"/>
          </w:tcPr>
          {prompt_paragraphs}
        </w:tc>
      </w:tr>
    </w:tbl>

    <w:p>
      <w:pPr><w:spacing w:before="300" w:after="120"/></w:pPr>
      <w:r>
        <w:rPr><w:sz w:val="20"/><w:color w:val="8E8A82"/></w:rPr>
        <w:t>Generated for Google AI Studio Build • KAVAL Architecture &amp; Interiors</w:t>
      </w:r>
    </w:p>
  </w:body>
</w:document>"""

    content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

    rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    for target_path in [DOCX_PATH, DIST_DOCX_PATH]:
        with zipfile.ZipFile(target_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types_xml)
            z.writestr("_rels/.rels", rels_xml)
            z.writestr("word/document.xml", document_xml)
        print(f"Generated .docx file at: {target_path}")

if __name__ == "__main__":
    create_rich_doc()
    create_docx()
    print("Document generation complete!")
