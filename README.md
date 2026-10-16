# KAVAL Architecture & Interiors — Cinematic Showcase

A luxury award-style single-page website for an architectural and interior design studio featuring smooth inertial scrolling, a scroll-controlled background video walkthrough in the Hero section, and real high-resolution architectural photography.

---

## Tech Stack
- **HTML5, CSS3, Vanilla JavaScript (ES modules)**
- **GSAP 3 + ScrollTrigger** (CDN)
- **Locomotive Scroll v4** (smooth scrolling integrated via `scrollerProxy`)
- **Typography**: Inter Tight (UI & Headings) + Playfair Display (editorial accents)

---

## Layout & Experience Flow
1. **Section 1: Hero Walkthrough (Background Scroll-Controlled Video)**
   - The walkthrough video (`walkthrough-scrub.mp4`) plays in the background while the user scrolls.
   - Pinned for ~450% scroll distance with butter-smooth frame-accurate scrubbing.
   - Overlaid with the studio wordmark (`KAVAL`), dynamic chapter milestones (`01 / The Arrival`, `02 / The Threshold`, `03 / The Living Space`, `04 / The Ascent`), vertical progress line, live timecode (`00:00 / 00:10`), and rotating scroll badge.
2. **Section 2: Intro + Floating Cards**
   - Directly revealed once the video walkthrough completes!
   - Warm cream `#F3EFE6` canvas with masked headline reveal (*Homes. Spaces. Stories. Details.*), interactive search pill, and 4 tilted cards featuring real luxury architectural photography.
3. **Section 3: Project List**
   - Deep charcoal background with 3D perspective tilt on entry and signature inline photo thumbnail expansion between words on hover (`0 -> 160px`).
4. **Section 4: Dusk Villa Showcase**
   - Real full-bleed twilight photography with scroll-linked camera zoom and floating glass tags with gentle sine-wave animation.
5. **Section 5: Process Carousel**
   - Pinned horizontal scroll through Consultation, Concept, Build, and Handover.
6. **Section 6: Footer & Magnetic CTA**
   - Charcoal footer with "Let's build your dream home", magnetic circular button tracking the cursor, marquee ribbon, and multi-city studio columns.

---

## Asset Locations & Placeholder Images Guide

All assets are real high-resolution photographs located in `/public/assets` (served directly at `/assets/...`):

| File Path | Description | Recommended Dimensions |
|---|---|---|
| `/assets/walkthrough-scrub.mp4` | 10-second scroll-scrubbed walkthrough video (All keyframes, `-g 1`) | `1920x1080` (H.264 MP4) |
| `/assets/hero-exterior.jpg` | Real photo of villa exterior at golden hour | `1920x1080` (JPG) |
| `/assets/dusk-house.jpg` | Real photo of villa at dusk with warm illuminated windows | `1920x1080` (JPG) |
| `/assets/rooms/living.jpg` | Real photo of double-height living room with stone wall | `1920x1080` (JPG) |
| `/assets/rooms/courtyard.jpg` | Real photo of tropical courtyard atrium | `1920x1080` (JPG) |
| `/assets/rooms/staircase.jpg` | Real photo of floating wooden architectural staircase | `1920x1080` (JPG) |
| `/assets/rooms/bedroom.jpg` | Real photo of master bedroom sanctuary | `1600x1200` (JPG) |
| `/assets/rooms/kitchen.jpg` | Real photo of modern minimalist timber kitchen | `1600x1200` (JPG) |
| `/assets/projects/p1.jpg` to `p4.jpg` | Real project showcase thumbnails | `1600x1200` (JPG) |

---

## FFmpeg Command for Smooth Scroll-Scrub Video

```bash
ffmpeg -i walkthrough.mp4 -vf scale=1920:-2 -c:v libx264 -g 1 -crf 22 -an -movflags +faststart public/assets/walkthrough-scrub.mp4
```
- `-g 1`: Guarantees every single frame is an intra-frame (keyframe), ensuring instant response when scrubbing backward and forward via scroll.
