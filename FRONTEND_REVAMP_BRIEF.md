# Iconic Design — Frontend Revamp Brief
### Asset & Decision Request Document
**Prepared by:** Development Team  
**Handed to:** Client (Shakir Ali, Founder — Iconic Design)  
**Purpose:** To collect every asset, preference, and decision needed before the revamp begins. Please fill in or attach your answers to each section and return this document.

---

> **Why this document exists**  
> The current website uses a **Dark Navy Blue + White + Gold** theme. You have requested a new look — different colors, a new logo, and a different font for the brand name. To rebuild the frontend with **zero mismatches**, we need exact files and decisions from you before any code is written. Every specification below is used directly in the website, so please be as precise as possible.

---

## SECTION 1 — Brand Colors (New Theme)

The current theme uses these colors (for your reference):

| Role | Current Color | Hex Code |
|---|---|---|
| Background / Navbar | Dark Navy | `#0f1e3c` |
| Accent / Buttons / Highlights | Gold | `#d4af37` |
| Secondary Blue | Medium Blue | `#1e40af` |
| Page Background | Off-White | `#fafafa` |

### What we need from you:

Please provide the **new** colors you want, with exact hex codes if possible. If you don't have hex codes, describe the color and we will match it.

| Role | Your New Color | Hex Code (if known) |
|---|---|---|
| **Primary / Navbar background** | | |
| **Main accent / Buttons / Highlights** | | |
| **Secondary / Supporting accent** | | |
| **Page background** | | |
| **Headings text color** | | |
| **Body / Paragraph text color** | | |

> **Tip:** If you have a brand style guide, color board, or even a reference image/Pinterest board showing the palette you like, share that — it is more reliable than describing colors in words.

---

## SECTION 2 — Logo

### Current Logo
The current logo is an image file (`logo_transparent.png`) used in two places:
1. **The Favicon** — tiny icon shown in the browser tab (currently 32x32 px displayed)
2. **The Navbar logo mark** — shown at **55 px tall** next to the brand name text

### What we need from you:

#### 2A — New Logo File

| Requirement | Specification |
|---|---|
| **File format** | **PNG with transparent background** (mandatory — the navbar has a dark/colored background) |
| **Minimum canvas size** | At least **400 x 400 px** (square is ideal for logo marks) |
| **Color** | Must be visible on both **dark** and **light** backgrounds, OR provide two versions |
| **Style** | If it contains text (e.g. "ID"), that text must be legible at 55 px height |

> WARNING: Do NOT send a JPG or a logo on a white background. It will show as a white box on the navbar. The file must have a transparent (checkered) background when opened in any image editor.

#### 2B — Favicon Version
If your logo doesn't work at tiny sizes (e.g. it has fine detail or small text), we need a **simplified version** for the favicon.

| Requirement | Specification |
|---|---|
| **File format** | PNG with transparent background |
| **Canvas size** | **64 x 64 px** minimum (will be scaled down to 32 px in browser) |
| **Content** | A single icon/symbol only — no full text at this size |

**Do you want a separate simplified favicon icon?**
- [ ] Yes — I will provide a separate icon file
- [ ] No — use the same logo file for both

---

## SECTION 3 — Brand Name Typography (Navbar)

### Current Style
The navbar currently shows the brand name split into two parts:

```
ICONIC  •  DESIGN
```
- **"ICONIC"** — Font: Playfair Display (serif), Size: 2.6rem, Color: White
- **"•"** — A small gold dot/circle separator (14x14 px)
- **"DESIGN"** — Font: Montserrat (sans-serif), Size: 1.1rem, Color: Gold, Letter-spacing: 6px, ALL CAPS

### What we need from you:

#### 3A — Font for "ICONIC" (the main word)
The client wants a different font. Please choose one of the options below OR provide the font name yourself.

**Option A — Serif (Elegant / Classic)**
- Cormorant Garamond (currently loaded on the site)
- EB Garamond
- Libre Baskerville
- Lora
- Bodoni Moda

**Option B — Sans-Serif (Modern / Clean)**
- Raleway
- DM Sans
- Josefin Sans
- Cinzel (Roman/architectural feel)
- Bebas Neue (bold, all caps)

**Option C — Script / Decorative**
- Great Vibes (currently used in footer — flowing cursive)
- Italiana
- Alex Brush
- Dancing Script

**Option D — Custom / Purchased Font**
- [ ] I have a specific font — font name: _______________
- [ ] I will provide the font file (.woff2 or .ttf format required)

**Your choice for "ICONIC":** _______________

#### 3B — Font for "DESIGN" (the subtitle word)
**Your choice for "DESIGN":** _______________  
*(Can be the same font or a different one)*

#### 3C — Color of "ICONIC"
**Current:** White (#ffffff)  
**Your new color:** _______________

#### 3D — Color of "DESIGN"
**Current:** Gold (#d4af37)  
**Your new color:** _______________

#### 3E — The Separator between "ICONIC" and "DESIGN"
**Current:** Small gold dot (circle shape)  
**Options:**
- [ ] Keep the dot separator
- [ ] Remove it — just a space between the words
- [ ] Replace with a line/dash — e.g. ICONIC — DESIGN
- [ ] Replace with a period — e.g. iconic.design
- [ ] Other: _______________

#### 3F — Capitalization style
- [ ] ICONIC DESIGN (all caps, current style)
- [ ] Iconic Design (title case)
- [ ] iconic design (all lowercase)
- [ ] iconic.design (domain-style)
- [ ] Other: _______________

---

## SECTION 4 — Hero Section (Homepage Banner)

### Current Setup
The hero is a **full-screen banner** (100% of the screen height) with:
- A **background image** (`hero_bg.png`) with a dark overlay on top
- A **glassmorphic card** (frosted glass effect) containing the headline text and CTA buttons
- The card sits on the **left side** on desktop, **centered** on mobile

### What we need from you:

#### 4A — Hero Background Image

| Requirement | Specification |
|---|---|
| **File format** | JPG or PNG (JPG preferred for file size) |
| **Minimum resolution** | **1920 x 1080 px** |
| **Ideal resolution** | **2560 x 1440 px** or higher |
| **Orientation** | Landscape (wider than tall) — **mandatory** |
| **Subject** | A luxury interior space, room, or your actual project photo |
| **Important** | The **left ~40%** of the image will be partially obscured by the text card — keep the key visual on the **right side** |
| **Dark overlay** | We apply a dark semi-transparent overlay on top of your image. A bright, vibrant image works better than an already-dark one |

> NOTE: If you want to use a real project photo, send the highest-quality photo available. Minimum 2 MB file size recommended for full-screen sharpness.

**File name to send:** `hero_bg.jpg` or `hero_bg.png`  
**Your hero image decision:** _______________

#### 4B — Dark Overlay Strength
The current overlay is approximately 72% dark navy. After the color change, this will need adjusting.

**How dark should the overlay be?**
- [ ] Very dark (barely see the image) — text is very readable
- [ ] Medium (current style — image is visible but muted)
- [ ] Light (image is very visible) — works only if image is not too bright

#### 4C — Overlay Color
**Current:** Dark navy blue  
**After revamp:** Should match your new primary/navbar color  
**Confirm:** Use the new primary color as the overlay? — [ ] Yes / [ ] No, use: _______________

#### 4D — Hero Text Content
These are the words displayed in large text on the hero card. They can be changed from the admin panel at any time — but if you want different defaults, provide them now.

| Field | Current Text | Your New Text |
|---|---|---|
| **Badge** (small pill text above headline) | "India's Premier Interior Designers" | |
| **Headline (H1)** | "Crafting Iconic Interiors" | |
| **Sub-text (paragraph)** | "With over 25 years of experience, Iconic Design delivers premium interior design, luxury decoration, and bespoke residential environments tailored to your lifestyle." | |

---

## SECTION 5 — Additional Visual Assets

### 5A — Founder / About Photo
The About section shows a portrait photo of you (the founder) in a **4:5 aspect ratio card** (portrait orientation — like an Instagram portrait).

| Requirement | Specification |
|---|---|
| **File format** | JPG or PNG |
| **Minimum size** | **800 x 1000 px** |
| **Aspect ratio** | **4 wide : 5 tall** (portrait) — we will auto-crop to this |
| **Subject position** | Keep face/upper body in the **top 60%** of the frame — bottom will be cropped |
| **Background** | Any background works — solid, blurred, or a room setting |

**File name to send:** `founder_photo.jpg`  
**Do you want to update this photo?** — [ ] Yes / [ ] No, keep current

---

## SECTION 6 — Overall Style Direction

Please pick the option that best describes the new look you want:

#### 6A — General Mood
- [ ] **Warm & Earthy** — Beige, terracotta, warm browns, cream tones
- [ ] **Minimal & Modern** — White, light grey, black, clean lines
- [ ] **Rich & Luxurious** — Deep emerald/forest green, gold, off-white
- [ ] **Bold & Contemporary** — Dark charcoal, copper/rose gold, white
- [ ] **Soft & Feminine** — Blush, sage green, dusty rose, champagne
- [ ] **Other** — Describe: _______________

#### 6B — Reference Websites or Images
This is the most helpful thing you can share. Please provide:
- Links to 2–3 websites whose look you admire
- Or screenshots/images of interiors or designs with a color palette you like

**References:** _______________

#### 6C — What must stay the same?
- [ ] Keep the gold accent color (only change the blues)
- [ ] Keep the Playfair Display font for headings
- [ ] Keep the glassmorphic hero card style
- [ ] Keep the dark navbar (just change the color)
- [ ] Keep the footer layout
- [ ] Nothing — full change

---

## SECTION 7 — File Delivery Instructions

### How to send us the files

Please send all files via WhatsApp / Google Drive / WeTransfer to the developer. Name each file exactly as listed below to avoid confusion.

| File | File Name | Format | Size |
|---|---|---|---|
| New Logo (main) | `logo_new.png` | PNG, transparent bg | Min 400x400 px |
| New Logo (favicon) | `logo_favicon.png` | PNG, transparent bg | Min 64x64 px |
| Hero Background | `hero_bg.jpg` | JPG | Min 1920x1080 px |
| Founder Photo (if updating) | `founder_photo.jpg` | JPG | Min 800x1000 px |
| Custom Font (if applicable) | `brand_font.woff2` or `.ttf` | Font file | — |
| Color Reference / Mood Board | `color_reference.jpg` | JPG/PNG/PDF | Any |

### Checklist before sending

- [ ] Logo is PNG with **transparent background** (not white)
- [ ] Hero image is at least **1920 x 1080 px** and landscape orientation
- [ ] Founder photo is at least **800 x 1000 px** (portrait orientation)
- [ ] All color hex codes are filled in Section 1, OR a mood board image is attached
- [ ] Font preference is filled in Section 3, OR font files are attached
- [ ] This document is returned with all sections answered

---

## SECTION 8 — Timeline & Notes

| Item | Details |
|---|---|
| **Asset submission deadline** | _______________ |
| **Revamp target completion** | _______________ |
| **Any other special requests** | _______________ |

---

*Document version: 1.0 — Iconic Design Frontend Revamp*  
*For questions, contact your developer directly.*
