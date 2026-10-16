# Plan: Google Docs Downloadable Prompt & Video Reference Guide

Generate a formatted, downloadable document (`.docx` / Google Docs compatible) containing the complete Google AI Studio master prompt and video walkthrough reference instructions, without raw markdown syntax.

---

### User Review & Critical Decisions

> [!IMPORTANT]
> - **Delivery Format**: Downloadable Google Docs compatible document (`.docx` / styled rich document) placed in the public downloads directory with a direct browser download link and button, ready to open or import directly into Google Docs.
> - **Scope & Content**: Prompt and video reference instructions only (excluding extraction script code, as requested).
> - **Document Styling**: Styled for Google Docs with clean typography (Degular / Arial hierarchy), title, section headings, visual bullet points, callout boxes, and copy-paste ready prompt text.

- **Confirmed Decision 1**: Downloadable document ready to open in Google Docs.
- **Confirmed Decision 2**: Prompt and video reference instructions only.

---

## 1. Overview & Document Structure

The generated document will be structured for immediate use in Google Docs or Google AI Studio:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Google Docs Document Layout                          │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Document Title & Project Overview                                   │
│    "KAVAL Architecture & Interiors — Google AI Studio Master Prompt"   │
│                                                                        │
│ 2. Video Reference & Asset Specification                               │
│    • Video file name, resolution, duration, and walkthrough timeline   │
│    • Scene breakdown (Exterior -> Teak Entrance -> Courtyard ->       │
│      Living Space -> Floating Mezzanine -> Dusk Terrace)               │
│                                                                        │
│ 3. Complete Single-Turn Google AI Studio Master Prompt                 │
│    • Role and design philosophy                                        │
│    • Adobe Typekit Degular typography setup & hierarchy rules          │
│    • Hero frame-by-frame canvas scroll scrubbing specification         │
│    • 12 Kinetic typography chapter subtitles                           │
│    • Spaces & Materiality filterable cards section                     │
│    • 3D Elevation showcase (pure black typography, no kicker)          │
│    • Architectural project row index & process steps                   │
│    • Footer marquee & inquiry dialog modal                             │
│                                                                        │
│ 4. Step-by-Step Instructions to Run in Google AI Studio                │
│    • How to create a new project, paste prompt, and provide video      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technical Execution Steps

1. **Document Generator Script**:
   - Create a generator script that builds the `.docx` document with styled headings, clean margins, bullet points, callout boxes, and table layouts formatted natively for Google Docs.
   - Output the file to `public/downloads/Google_AI_Studio_Architecture_Prompt.docx` so it can be downloaded directly from the browser preview.

2. **Download UI & Link Access**:
   - Provide a direct download button / link on the live website and direct URL access (`/downloads/Google_AI_Studio_Architecture_Prompt.docx`).
   - Also generate a styled HTML document (`Google_AI_Studio_Architecture_Prompt.html`) formatted for one-click upload or copy-paste into Google Docs.

3. **Content Verification**:
   - Verify that all prompt instructions, Adobe Typekit Degular styling (500 for big headings, 400 for small headings), Section 3 black text specifications, and video timeline cues are captured accurately.

---

## 3. Verification Checklist

- [ ] Generate `.docx` document and place in `public/downloads/`.
- [ ] Verify file opens cleanly in Google Docs with preserved headings, formatting, and prompt blocks.
- [ ] Verify prompt includes exact video reference specifications (`House Walkthrough Website.mp4`, 20.065s, 300 frames).
- [ ] Verify download link accessible via dev server.
