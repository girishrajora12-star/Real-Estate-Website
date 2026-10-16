#!/usr/bin/env python3
import os
import subprocess
import math

PUBLIC_DIR = "/public/assets"
os.makedirs(f"{PUBLIC_DIR}/rooms", exist_ok=True)
os.makedirs(f"{PUBLIC_DIR}/projects", exist_ok=True)
os.makedirs("/tmp/svg_build", exist_ok=True)

# 1. Generate SVGs for all architectural scenes
def get_hero_svg(include_sky=True, transparent=False):
    sky = ""
    if include_sky and not transparent:
        sky = """
        <defs>
            <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#1B2838"/>
                <stop offset="35%" stop-color="#38495E"/>
                <stop offset="65%" stop-color="#8C583E"/>
                <stop offset="85%" stop-color="#D97A48"/>
                <stop offset="100%" stop-color="#F4AF6A"/>
            </linearGradient>
            <radialGradient id="sunGlow" cx="65%" cy="70%" r="50%">
                <stop offset="0%" stop-color="#FFD494" stop-opacity="0.85"/>
                <stop offset="40%" stop-color="#F28B44" stop-opacity="0.4"/>
                <stop offset="100%" stop-color="#F28B44" stop-opacity="0"/>
            </radialGradient>
        </defs>
        <rect width="1920" height="1080" fill="url(#skyGrad)"/>
        <circle cx="1250" cy="720" r="450" fill="url(#sunGlow)"/>
        """
    else:
        sky = """
        <defs>
            <linearGradient id="warmLight" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#FFE0A3" stop-opacity="0.9"/>
                <stop offset="100%" stop-color="#FF9E42" stop-opacity="0.7"/>
            </linearGradient>
        </defs>
        """

    # Villa Architecture details
    building = """
    <!-- Background Mountains / Distant Tropical Trees -->
    <path d="M 0 740 Q 240 700 500 730 T 1100 710 T 1600 725 T 1920 710 L 1920 1080 L 0 1080 Z" fill="#243329" opacity="0.6"/>
    <g fill="#1B281F" opacity="0.8">
        <path d="M -50 780 C 20 680, 80 640, 120 790 Z"/>
        <path d="M 1650 780 C 1720 650, 1800 620, 1880 790 Z"/>
        <path d="M 1780 790 C 1840 680, 1920 670, 1980 790 Z"/>
    </g>

    <!-- Main Villa Building Structure -->
    <!-- Terracotta Roof Left Wing -->
    <polygon points="120,440 460,330 680,440 640,465 140,465" fill="#8F341F"/>
    <polygon points="140,440 460,340 660,440" fill="#B3462B"/>
    <!-- Roof tiles ridge lines -->
    <line x1="460" y1="330" x2="460" y2="440" stroke="#682110" stroke-width="4"/>
    <line x1="280" y1="390" x2="300" y2="450" stroke="#7A2814" stroke-width="3"/>
    <line x1="560" y1="390" x2="540" y2="450" stroke="#7A2814" stroke-width="3"/>

    <!-- Terracotta Roof Center & Upper Story -->
    <polygon points="940,240 1480,240 1680,360 1620,385 860,385 910,360" fill="#782917"/>
    <polygon points="960,250 1460,250 1640,360 900,360" fill="#A83E24"/>
    <polygon points="620,370 1020,370 1060,430 580,430" fill="#8F341F"/>

    <!-- Left Wing Facade (Teak vertical louvers) -->
    <rect x="180" y="465" width="460" height="340" fill="#221C19"/>
    <!-- Glass with warm interior reflection -->
    <rect x="200" y="485" width="420" height="290" fill="#4A3423"/>
    <rect x="220" y="500" width="380" height="260" fill="#E6984A" opacity="0.35"/>
    <!-- Teak Louvers slats -->
    """
    louvers = "".join([f'<rect x="{x}" y="480" width="12" height="310" fill="#753C18" rx="2"/><rect x="{x+2}" y="480" width="4" height="310" fill="#9C5424"/>' for x in range(210, 610, 24)])

    structure_center = """
    <!-- Center Entrance Portal & Grand Teak Pivot Door -->
    <rect x="680" y="430" width="360" height="400" fill="#2A2420"/>
    <!-- Stone Cladding Wall -->
    <rect x="650" y="430" width="80" height="400" fill="#3A3734"/>
    <rect x="990" y="430" width="90" height="400" fill="#3F3C38"/>
    <!-- Stone texture seams -->
    <line x1="650" y1="490" x2="730" y2="490" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="650" y1="560" x2="730" y2="560" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="650" y1="640" x2="730" y2="640" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="650" y1="720" x2="730" y2="720" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="990" y1="480" x2="1080" y2="480" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="990" y1="550" x2="1080" y2="550" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="990" y1="630" x2="1080" y2="630" stroke="#1F1E1D" stroke-width="2"/>
    <line x1="990" y1="710" x2="1080" y2="710" stroke="#1F1E1D" stroke-width="2"/>

    <!-- Deep Portico Shadow & Double Teak Doors -->
    <rect x="730" y="460" width="260" height="360" fill="#151210"/>
    <!-- Teak Door Left Leaf -->
    <rect x="745" y="480" width="110" height="340" fill="#7A421D" rx="3"/>
    <rect x="750" y="490" width="100" height="45" fill="#8F5025" rx="2"/>
    <rect x="750" y="550" width="100" height="45" fill="#8F5025" rx="2"/>
    <rect x="750" y="610" width="100" height="45" fill="#8F5025" rx="2"/>
    <rect x="750" y="670" width="100" height="45" fill="#8F5025" rx="2"/>
    <rect x="750" y="730" width="100" height="45" fill="#8F5025" rx="2"/>
    <circle cx="845" cy="650" r="5" fill="#DDB05E"/>

    <!-- Teak Door Right Leaf -->
    <rect x="865" y="480" width="110" height="340" fill="#884A22" rx="3"/>
    <rect x="870" y="490" width="100" height="45" fill="#9C572A" rx="2"/>
    <rect x="870" y="550" width="100" height="45" fill="#9C572A" rx="2"/>
    <rect x="870" y="610" width="100" height="45" fill="#9C572A" rx="2"/>
    <rect x="870" y="670" width="100" height="45" fill="#9C572A" rx="2"/>
    <rect x="870" y="730" width="100" height="45" fill="#9C572A" rx="2"/>
    <circle cx="875" cy="650" r="5" fill="#DDB05E"/>

    <!-- Overhead Portico Teak Soffit with warm recessed lights -->
    <polygon points="690,430 1030,430 1010,460 710,460" fill="#5E3113"/>
    <circle cx="780" cy="455" r="8" fill="#FFE2A0"/>
    <circle cx="940" cy="455" r="8" fill="#FFE2A0"/>

    <!-- Steps leading to entrance -->
    <polygon points="640,820 1080,820 1110,845 610,845" fill="#736E67"/>
    <polygon points="610,845 1110,845 1140,870 580,870" fill="#87827A"/>
    <polygon points="580,870 1140,870 1170,895 550,895" fill="#99938B"/>
    <line x1="550" y1="895" x2="1170" y2="895" stroke="#4F4A44" stroke-width="3"/>

    <!-- Right Wing: 2 Stories with Balcony & Carport -->
    <!-- Upper Story Glass with Teak Frames -->
    <rect x="1080" y="380" width="460" height="230" fill="#1C1B19"/>
    <rect x="1100" y="400" width="200" height="190" fill="#523924"/>
    <rect x="1110" y="410" width="180" height="170" fill="#F0A656" opacity="0.45"/>
    <rect x="1330" y="400" width="190" height="190" fill="#473425"/>
    <!-- Glass Balcony Railing -->
    <rect x="1080" y="580" width="460" height="50" fill="#A8BAC7" opacity="0.3" stroke="#687985" stroke-width="2"/>

    <!-- Lower Right: Garage / Portico & Car -->
    <rect x="1080" y="610" width="480" height="230" fill="#1E1C1A"/>
    <!-- Teak ceiling for carport -->
    <rect x="1080" y="610" width="480" height="25" fill="#6B3917"/>
    <!-- White Luxury Car in Portico -->
    <path d="M 1320 780 C 1340 735, 1420 730, 1530 735 C 1600 740, 1660 760, 1690 790 L 1690 830 L 1310 830 Z" fill="#E8ECEF"/>
    <path d="M 1370 740 L 1440 740 L 1480 760 L 1350 760 Z" fill="#252A30"/>
    <circle cx="1370" cy="830" r="28" fill="#1A1A1A"/>
    <circle cx="1370" cy="830" r="14" fill="#C7CCD1"/>
    <circle cx="1630" cy="830" r="28" fill="#1A1A1A"/>
    <circle cx="1630" cy="830" r="14" fill="#C7CCD1"/>
    <polygon points="1660,785 1690,785 1685,800 1655,798" fill="#FFC95C"/>

    <!-- Ground, Driveway & Landscaping -->
    <polygon points="0,870 1920,870 1920,1080 0,1080" fill="#3D3B37"/>
    <!-- Stone pavers grid -->
    """

    pavers = ""
    for y in range(880, 1080, 40):
        pavers += f'<line x1="0" y1="{y}" x2="1920" y2="{y}" stroke="#2B2926" stroke-width="2"/>'
    for x in range(0, 1920, 80):
        pavers += f'<line x1="{x}" y1="880" x2="{x-60}" y2="1080" stroke="#2B2926" stroke-width="2"/>'

    plants = """
    <!-- Tropical Plants & Landscaping (Foreground / Midground) -->
    <!-- Left Plant Cluster (Monstera & Palms) -->
    <g fill="#182A1B">
        <path d="M 40 920 C 10 840, 80 800, 120 860 C 160 810, 220 850, 180 930 Z"/>
        <path d="M 140 950 C 90 870, 180 830, 240 890 C 290 850, 320 900, 270 960 Z"/>
        <path d="M 280 970 C 240 900, 330 870, 380 930 Z"/>
    </g>
    <g fill="#2B462E">
        <path d="M 60 930 C 30 860, 90 820, 130 870 Z"/>
        <path d="M 160 960 C 110 890, 190 850, 240 900 Z"/>
    </g>

    <!-- Planter by Entrance -->
    <rect x="520" y="810" width="110" height="60" fill="#36332F" rx="4"/>
    <g fill="#213B26">
        <path d="M 540 810 C 510 750, 560 720, 575 790 Z"/>
        <path d="M 570 810 C 550 740, 600 710, 615 780 Z"/>
        <path d="M 590 810 C 580 730, 630 730, 625 800 Z"/>
    </g>

    <!-- Right Plant Cluster by Carport -->
    <g fill="#182A1B">
        <path d="M 1020 890 C 990 820, 1050 780, 1080 840 C 1110 790, 1170 830, 1140 900 Z"/>
        <path d="M 1720 920 C 1680 820, 1780 780, 1820 860 C 1870 810, 1920 860, 1880 930 Z"/>
    </g>
    """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    {sky}
    {building}
    {louvers}
    {structure_center}
    {pavers}
    {plants}
    </svg>"""
    return svg

def get_dusk_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <defs>
        <linearGradient id="duskSky" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#080E18"/>
            <stop offset="45%" stop-color="#121C2B"/>
            <stop offset="80%" stop-color="#222738"/>
            <stop offset="100%" stop-color="#3D2924"/>
        </linearGradient>
        <radialGradient id="windowGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFE082" stop-opacity="1"/>
            <stop offset="60%" stop-color="#FF9800" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="#E65100" stop-opacity="0.2"/>
        </radialGradient>
    </defs>
    <rect width="1920" height="1080" fill="url(#duskSky)"/>
    <!-- Silhouette Mountains -->
    <path d="M 0 680 Q 400 620 900 650 T 1920 640 L 1920 1080 L 0 1080 Z" fill="#0A0F14"/>

    <!-- Villa Structure at Dusk -->
    <!-- Left Wing Roof & Windows -->
    <polygon points="140,430 460,330 660,430" fill="#3D1812"/>
    <rect x="200" y="470" width="420" height="300" fill="#120D0A"/>
    <!-- Glowing Windows -->
    <rect x="220" y="490" width="380" height="260" fill="url(#windowGlow)"/>
    <!-- Teak Louver Silhouettes -->
    """ + "".join([f'<rect x="{x}" y="480" width="10" height="280" fill="#1C120C" opacity="0.9"/>' for x in range(230, 590, 28)]) + """

    <!-- Upper Story Glowing Glass -->
    <polygon points="940,240 1480,240 1680,360 900,360" fill="#30130E"/>
    <rect x="1080" y="380" width="460" height="220" fill="#120D0A"/>
    <rect x="1100" y="400" width="420" height="180" fill="url(#windowGlow)"/>
    """ + "".join([f'<rect x="{x}" y="390" width="8" height="200" fill="#140E0A"/>' for x in range(1120, 1500, 36)]) + """

    <!-- Center Pivot Door with Warm Light spill -->
    <rect x="680" y="420" width="360" height="400" fill="#1A1410"/>
    <rect x="740" y="470" width="240" height="350" fill="#0F0C0A"/>
    <polygon points="760,490 850,480 870,820 740,820" fill="#FFB74D" opacity="0.85"/>
    <polygon points="870,480 960,490 980,820 850,820" fill="#FFA726" opacity="0.75"/>

    <!-- Terrace & Reflection Pool -->
    <polygon points="0,850 1920,850 1920,1080 0,1080" fill="#0D1117"/>
    <!-- Pool with water reflection of amber windows -->
    <rect x="350" y="890" width="1220" height="170" fill="#0F1722" rx="12"/>
    <ellipse cx="450" cy="970" rx="160" ry="40" fill="#FF9800" opacity="0.35"/>
    <ellipse cx="860" cy="970" rx="100" ry="30" fill="#FFB74D" opacity="0.45"/>
    <ellipse cx="1320" cy="970" rx="180" ry="40" fill="#FF9800" opacity="0.35"/>

    <!-- Floating Landscape Uplights -->
    <circle cx="560" cy="860" r="12" fill="#FFE082"/>
    <circle cx="1060" cy="860" r="12" fill="#FFE082"/>
    <circle cx="1580" cy="860" r="12" fill="#FFE082"/>

    <!-- Foreground Palm Silhouettes -->
    <g fill="#06090D">
        <path d="M 0 1080 C 40 920, 140 880, 200 950 C 260 890, 320 940, 280 1080 Z"/>
        <path d="M 1680 1080 C 1720 900, 1820 880, 1880 960 C 1920 920, 1960 980, 1920 1080 Z"/>
    </g>
    </svg>"""

def get_living_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <defs>
        <linearGradient id="warmInterior" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#2C231C"/>
            <stop offset="50%" stop-color="#1F1914"/>
            <stop offset="100%" stop-color="#14100D"/>
        </linearGradient>
    </defs>
    <rect width="1920" height="1080" fill="url(#warmInterior)"/>
    <!-- Ceiling with Teak Beams & Concealed LED Cove -->
    <polygon points="0,0 1920,0 1920,240 0,240" fill="#18130F"/>
    <rect x="0" y="235" width="1920" height="15" fill="#FFA726" opacity="0.7"/>
    """ + "".join([f'<rect x="{x}" y="0" width="30" height="240" fill="#6B3917"/>' for x in range(120, 1920, 160)]) + """

    <!-- Stacked Natural Stone Feature Wall -->
    <rect x="320" y="250" width="880" height="480" fill="#2E2B27"/>
    """ + "".join([f'<line x1="320" y1="{y}" x2="1200" y2="{y}" stroke="#1E1C19" stroke-width="3"/>' for y in range(270, 730, 28)]) + """
    <!-- Contemporary Illuminated Artwork -->
    <rect x="520" y="340" width="480" height="260" fill="#D5C5A8" stroke="#FFA726" stroke-width="4"/>
    <path d="M 560 520 Q 680 380 760 480 T 960 420" stroke="#7A3919" stroke-width="12" fill="none"/>
    <path d="M 580 440 Q 720 540 880 390" stroke="#2B241E" stroke-width="8" fill="none"/>

    <!-- Floor-to-Ceiling Glass Sliding Doors to Tropical Garden -->
    <rect x="1240" y="250" width="680" height="580" fill="#0C1410"/>
    <!-- Moonlit Palms outside -->
    <g fill="#182A1B" opacity="0.7">
        <path d="M 1320 800 C 1360 620, 1480 600, 1540 700 C 1600 640, 1700 720, 1660 830 Z"/>
        <path d="M 1600 800 C 1660 580, 1780 560, 1860 680 Z"/>
    </g>
    <!-- Teak Door Frames -->
    <rect x="1240" y="250" width="30" height="580" fill="#7A3D18"/>
    <rect x="1560" y="250" width="30" height="580" fill="#7A3D18"/>
    <rect x="1890" y="250" width="30" height="580" fill="#7A3D18"/>

    <!-- Polished Marble Floor with Warm Reflections -->
    <polygon points="0,730 1920,730 1920,1080 0,1080" fill="#E4DCD0"/>
    <polygon points="0,730 1920,730 1920,1080 0,1080" fill="#FFA726" opacity="0.12"/>

    <!-- Luxury Teak & Linen Low Sofas -->
    <rect x="180" y="720" width="780" height="190" fill="#5E3113" rx="16"/>
    <rect x="210" y="680" width="720" height="150" fill="#EDE4D8" rx="12"/>
    <rect x="230" y="640" width="220" height="90" fill="#E0D5C5" rx="8"/>
    <rect x="470" y="640" width="220" height="90" fill="#E0D5C5" rx="8"/>
    <rect x="710" y="640" width="200" height="90" fill="#8F4B23" rx="8"/>

    <!-- Solid Teak Coffee Table & Ceramic Vases -->
    <rect x="460" y="870" width="560" height="90" fill="#4A260E" rx="8"/>
    <rect x="490" y="850" width="500" height="40" fill="#7A3D18" rx="6"/>
    <ellipse cx="680" cy="840" rx="28" ry="14" fill="#D3C9BD"/>
    <ellipse cx="780" cy="835" rx="18" ry="24" fill="#CBB69D"/>
    </svg>"""

def get_staircase_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <defs>
        <radialGradient id="pendantGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#FFF3D1"/>
            <stop offset="40%" stop-color="#FFB300" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#FF6F00" stop-opacity="0"/>
        </radialGradient>
    </defs>
    <rect width="1920" height="1080" fill="#171412"/>
    <!-- Double-height wall with dark slate finish -->
    <rect x="0" y="0" width="1280" height="1080" fill="#25211E"/>
    """ + "".join([f'<line x1="0" y1="{y}" x2="1280" y2="{y}" stroke="#1B1715" stroke-width="4"/>' for y in range(80, 1080, 70)]) + """

    <!-- Upper Gallery / Mezzanine Bridge -->
    <rect x="0" y="160" width="1920" height="60" fill="#45230D"/>
    <rect x="0" y="130" width="1920" height="30" fill="#A4B3BC" opacity="0.3" stroke="#667782" stroke-width="2"/>

    <!-- Floating Teak Stair Treads -->
    """ + "".join([f'''
    <polygon points="{280 + i*75},{780 - i*62} {620 + i*75},{780 - i*62} {640 + i*75},{820 - i*62} {300 + i*75},{820 - i*62}" fill="#804118"/>
    <polygon points="{280 + i*75},{780 - i*62} {620 + i*75},{780 - i*62} {600 + i*75},{765 - i*62} {260 + i*75},{765 - i*62}" fill="#A65825"/>
    ''' for i in range(10)]) + """

    <!-- Frameless Glass Balustrade & Teak Handrail -->
    <polygon points="260,760 960,190 1010,210 310,810" fill="#9FB4C4" opacity="0.25"/>
    <line x1="260" y1="760" x2="960" y2="190" stroke="#7A3F18" stroke-width="12"/>

    <!-- Cascading Amber Glass Pendant Lights -->
    """ + "".join([f'''
    <line x1="{x}" y1="0" x2="{x}" y2="{y}" stroke="#B8860B" stroke-width="2"/>
    <circle cx="{x}" cy="{y}" r="45" fill="url(#pendantGlow)"/>
    <circle cx="{x}" cy="{y}" r="22" fill="#FFE599"/>
    ''' for x, y in [(1380, 360), (1450, 480), (1330, 560), (1520, 640), (1410, 740), (1480, 840)]]) + """

    <!-- Polished Floor -->
    <polygon points="0,880 1920,880 1920,1080 0,1080" fill="#EAE3D8"/>
    <polygon points="0,880 1920,880 1920,1080 0,1080" fill="#FFA726" opacity="0.15"/>
    </svg>"""

def get_courtyard_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <rect width="1920" height="1080" fill="#1D1A17"/>
    <!-- Glass Atrium Enclosure -->
    <rect x="520" y="160" width="880" height="760" fill="#0F1813"/>
    <rect x="520" y="160" width="880" height="760" fill="none" stroke="#684124" stroke-width="14"/>

    <!-- Lush Banana Tree & Tropical Courtyard Plants -->
    <ellipse cx="960" cy="900" rx="340" ry="60" fill="#121812"/>
    <g fill="#244A29">
        <path d="M 960 900 Q 880 580 720 460 Q 860 620 950 880 Z"/>
        <path d="M 960 900 Q 940 480 960 320 Q 980 510 970 880 Z"/>
        <path d="M 960 900 Q 1060 560 1200 440 Q 1070 630 970 880 Z"/>
    </g>
    <g fill="#376E3E">
        <ellipse cx="710" cy="450" rx="140" ry="65" transform="rotate(-30 710 450)"/>
        <ellipse cx="960" cy="310" rx="75" ry="160" transform="rotate(5 960 310)"/>
        <ellipse cx="1210" cy="430" rx="150" ry="70" transform="rotate(28 1210 430)"/>
    </g>

    <!-- Warm Amber Sconces & Traditional Brass Oil Lamp -->
    <circle cx="480" cy="520" r="16" fill="#FFA726"/>
    <circle cx="1440" cy="520" r="16" fill="#FFA726"/>
    <polygon points="940,890 980,890 965,810 955,810" fill="#D4AF37"/>
    <ellipse cx="960" cy="805" rx="20" ry="8" fill="#D4AF37"/>
    <circle cx="960" cy="795" r="8" fill="#FFF3D1"/>

    <!-- Corridor Framing with Polished Travertine -->
    <polygon points="0,880 1920,880 1920,1080 0,1080" fill="#DFD7CB"/>
    <rect x="0" y="0" width="480" height="880" fill="#28221D"/>
    <rect x="1440" y="0" width="480" height="880" fill="#28221D"/>
    """ + "".join([f'<rect x="{x}" y="80" width="14" height="740" fill="#753C18"/>' for x in range(60, 440, 42)]) + """
    """ + "".join([f'<rect x="{x}" y="80" width="14" height="740" fill="#753C18"/>' for x in range(1480, 1860, 42)]) + """
    </svg>"""

def get_bedroom_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <rect width="1920" height="1080" fill="#1C1815"/>
    <!-- Headboard wall with fluted teak acoustic slats -->
    <rect x="360" y="180" width="1200" height="540" fill="#44240E"/>
    """ + "".join([f'<rect x="{x}" y="180" width="10" height="540" fill="#6B3917"/>' for x in range(370, 1550, 22)]) + """
    <!-- Concealed warm headboard light -->
    <rect x="360" y="460" width="1200" height="12" fill="#FFA726" opacity="0.8"/>

    <!-- King Size Bed with Natural Linen & Teak Frame -->
    <rect x="540" y="580" width="840" height="340" fill="#E8DFD3" rx="18"/>
    <!-- Pillows -->
    <rect x="620" y="510" width="280" height="120" fill="#F4ECE2" rx="12"/>
    <rect x="1020" y="510" width="280" height="120" fill="#F4ECE2" rx="12"/>
    <!-- Amber Throw Blanket -->
    <polygon points="540,740 1380,740 1380,920 540,920" fill="#A85724" rx="12"/>

    <!-- Bedside Floating Teak Tables & Pendants -->
    <rect x="340" y="650" width="160" height="40" fill="#613414" rx="4"/>
    <circle cx="420" cy="580" r="18" fill="#FFC107"/>
    <line x1="420" y1="0" x2="420" y2="580" stroke="#B8860B" stroke-width="2"/>

    <rect x="1420" y="650" width="160" height="40" fill="#613414" rx="4"/>
    <circle cx="1500" cy="580" r="18" fill="#FFC107"/>
    <line x1="1500" y1="0" x2="1500" y2="580" stroke="#B8860B" stroke-width="2"/>

    <!-- Wool Rug on Parquet Floor -->
    <polygon points="0,860 1920,860 1920,1080 0,1080" fill="#2E241C"/>
    <rect x="380" y="880" width="1160" height="180" fill="#D3C9BD" rx="24"/>
    </svg>"""

def get_kitchen_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">
    <rect width="1920" height="1080" fill="#1E1A17"/>
    <!-- Quartzite back wall -->
    <rect x="0" y="160" width="1920" height="520" fill="#3A3632"/>
    <line x1="0" y1="420" x2="1920" y2="420" stroke="#FFA726" stroke-width="6"/>

    <!-- Fluted Teak Floating Shelves -->
    <rect x="240" y="280" width="1440" height="24" fill="#6B3917"/>
    <!-- Ceramics on shelf -->
    <ellipse cx="440" cy="260" rx="30" ry="20" fill="#E8DFD3"/>
    <rect x="620" y="220" width="30" height="60" fill="#C9B8A3" rx="4"/>
    <ellipse cx="820" cy="255" rx="45" ry="25" fill="#E0D2C0"/>

    <!-- Monolithic Waterfall Island in Quartzite & Fluted Teak -->
    <polygon points="340,640 1580,640 1680,980 240,980" fill="#221C18"/>
    <polygon points="340,640 1580,640 1520,680 400,680" fill="#ECE5DA"/>
    <!-- Fluted teak island base -->
    <rect x="420" y="680" width="1080" height="270" fill="#4B270F"/>
    """ + "".join([f'<rect x="{x}" y="680" width="12" height="270" fill="#753C18"/>' for x in range(430, 1490, 24)]) + """

    <!-- Sculptural Stools -->
    <ellipse cx="580" cy="940" rx="45" ry="15" fill="#221C18"/>
    <line x1="580" y1="940" x2="580" y2="820" stroke="#111" stroke-width="6"/>
    <ellipse cx="580" cy="820" rx="40" ry="12" fill="#8C4A21"/>

    <ellipse cx="880" cy="940" rx="45" ry="15" fill="#221C18"/>
    <line x1="880" y1="940" x2="880" y2="820" stroke="#111" stroke-width="6"/>
    <ellipse cx="880" cy="820" rx="40" ry="12" fill="#8C4A21"/>

    <ellipse cx="1180" cy="940" rx="45" ry="15" fill="#221C18"/>
    <line x1="1180" y1="940" x2="1180" y2="820" stroke="#111" stroke-width="6"/>
    <ellipse cx="1180" cy="820" rx="40" ry="12" fill="#8C4A21"/>

    <!-- Linear Brass Pendant -->
    <rect x="440" y="520" width="1040" height="12" fill="#D4AF37"/>
    <line x1="640" y1="0" x2="640" y2="520" stroke="#B8860B" stroke-width="2"/>
    <line x1="1280" y1="0" x2="1280" y2="520" stroke="#B8860B" stroke-width="2"/>
    <rect x="440" y="528" width="1040" height="4" fill="#FFF3D1"/>
    </svg>"""

# Generate base SVGs
print("Generating SVGs...")
svgs = {
    "/tmp/svg_build/hero-exterior.svg": get_hero_svg(include_sky=True, transparent=False),
    "/tmp/svg_build/hero-exterior-cutout.svg": get_hero_svg(include_sky=False, transparent=True),
    "/tmp/svg_build/dusk-house.svg": get_dusk_svg(),
    "/tmp/svg_build/living.svg": get_living_svg(),
    "/tmp/svg_build/staircase.svg": get_staircase_svg(),
    "/tmp/svg_build/courtyard.svg": get_courtyard_svg(),
    "/tmp/svg_build/bedroom.svg": get_bedroom_svg(),
    "/tmp/svg_build/kitchen.svg": get_kitchen_svg(),
}

for path, content in svgs.items():
    with open(path, "w") as f:
        f.write(content.strip())

print("Converting SVGs to JPG/PNG assets with ffmpeg...")
# Hero images
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/hero-exterior.svg", f"{PUBLIC_DIR}/hero-exterior.jpg"], check=True)
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/hero-exterior-cutout.svg", f"{PUBLIC_DIR}/hero-exterior-cutout.png"], check=True)
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/dusk-house.svg", f"{PUBLIC_DIR}/dusk-house.jpg"], check=True)

# Rooms
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/living.svg", f"{PUBLIC_DIR}/rooms/living.jpg"], check=True)
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/staircase.svg", f"{PUBLIC_DIR}/rooms/staircase.jpg"], check=True)
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/courtyard.svg", f"{PUBLIC_DIR}/rooms/courtyard.jpg"], check=True)
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/bedroom.svg", f"{PUBLIC_DIR}/rooms/bedroom.jpg"], check=True)
subprocess.run(["ffmpeg", "-y", "-i", "/tmp/svg_build/kitchen.svg", f"{PUBLIC_DIR}/rooms/kitchen.jpg"], check=True)

# Projects
subprocess.run(["cp", f"{PUBLIC_DIR}/hero-exterior.jpg", f"{PUBLIC_DIR}/projects/p1.jpg"], check=True)
subprocess.run(["cp", f"{PUBLIC_DIR}/rooms/courtyard.jpg", f"{PUBLIC_DIR}/projects/p2.jpg"], check=True)
subprocess.run(["cp", f"{PUBLIC_DIR}/rooms/living.jpg", f"{PUBLIC_DIR}/projects/p3.jpg"], check=True)
subprocess.run(["cp", f"{PUBLIC_DIR}/rooms/staircase.jpg", f"{PUBLIC_DIR}/projects/p4.jpg"], check=True)

print("Base images generated successfully!")
