# Project Description: AI Automation Agents for Ecommerce Landing Pages

**Client**: Med Aboussi  
**Company**: Ecommerce Performance Marketing  
**Price**: $500 (all 5 agents)  
**Timeline**: 7-10 days  

---

## Overview

5 AI agents that automate Med's marketing team's workflow for creating, translating, optimizing, and compliance-checking landing pages/funnels. All agents follow the same core pattern: HTML in → LLM processes → HTML out.

**Each agent is a standalone tool that operates independently.**

---

## Agent Summary

| Agent | Purpose | Input | Output |
|-------|---------|-------|--------|
| Agent 1 | Copy & Image Injection | Template + raw copy | Complete HTML page |
| Agent 2 | Translation & Localisation | HTML + target language | Translated HTML |
| Agent 3 | Policy & Compliance | HTML + policy rules | Compliant HTML + change log |
| Agent 4 | Funnel Optimization (CRO) | HTML + conversion playbook | Enhanced HTML |
| Agent 5 | Product Research | Keywords + markets | Structured research report |

---

## Agent 1: Copy & Image Injection Agent

**Purpose**: Automatically generates complete landing pages by filling predefined HTML templates with marketing copy and images.

**Input**:
- HTML template (one of 5-6 predefined templates with placeholders)
- Raw advertorial copy (unstructured text from copywriters)

**What it does**:
1. Receives selected template + raw copy
2. Recognizes copy patterns (headline, hook, body, product section, testimonials, CTA, legal)
3. Maps each copy section to the correct placeholder in the template
4. Detects image placeholders (hero, product, testimonial, authority)
5. Generates or fetches context-appropriate images based on surrounding copy
6. Places images into correct positions
7. Outputs final HTML + CSS ready to publish

**Output**:
- Complete HTML page with all placeholders filled
- All images placed
- Optional summary of what was placed where

**Rules**:
- Agent does NOT design layouts, only fills known layouts
- Template placeholders are predefined and maintained by Med's team
- Copy mapping follows hierarchy: headline → hook → body → product → proof → CTA
- Images must match the tone and context of surrounding copy (doctor image near authority text, customer selfie near testimonials, etc.)

**Depends on**: Templates must exist with explicit placeholders before this agent can work.

**Complexity**: Medium-high (image generation + context-aware placement is the tricky part)

---

## Agent 2: Translation & Localisation Agent

**Purpose**: Translates existing landing pages into other languages (German first) while keeping HTML structure identical and making the copy sound fully native.

**Input**:
- Full HTML of an existing landing page
- Target language (e.g., German)

**What it does**:
1. Receives full HTML
2. Extracts all visible text nodes (leaves HTML tags, CSS, classes, IDs untouched)
3. Translates all text naturally (not literal translation, native-sounding)
4. Applies light localisation:
   - Names: "John M., Ohio" → "Thomas K., München"
   - Locations: US cities → German cities
   - Institutions: "American research department" → "Deutsches Forschungsinstitut"
   - Cultural references: units, phrasing adjusted as needed
5. Proofreads translated text for awkward phrasing
6. Reinserts translated text into exact same HTML positions
7. Validates output HTML structure matches input

**Output**:
- Full HTML with identical structure, all text translated
- Optional summary of localisation changes (names, locations swapped)

**Rules**:
- NEVER modify HTML structure, CSS, class names, IDs, links, or URLs
- NEVER change meaning of claims
- NEVER add new claims or promises
- NEVER remove disclaimers
- Testimonials: translate naturally, localise names/locations, preserve emotional tone
- Legal text: translate accurately, preserve original meaning, use appropriate legal phrasing
- Result should read as if a native speaker originally wrote it

**Depends on**: Nothing. Works on any existing HTML page.

**Complexity**: Medium (HTML preservation is the main challenge)

---

## Agent 3: Policy & Compliance Agent

**Purpose**: Scans landing pages for advertising policy violations and fixes ONLY the violating copy, leaving everything else untouched.

**Input**:
- Full HTML of a landing page
- Policy instructions (e.g., "Remove medical cure claims", "Avoid guaranteed results", "Remove before/after implications")

**What it does**:
1. Receives full HTML + policy rules
2. Scans ALL text content in the HTML
3. Identifies every instance that violates the provided policy rules
4. For each violation:
   - Applies a targeted edit at phrase or sentence level
   - Keeps surrounding copy unchanged
   - Preserves reading flow and persuasion
   - Maintains the same marketing angle
5. Leaves all compliant copy completely untouched
6. Generates a change log with before/after for every edit

**Output**:
- Full HTML with identical structure, only policy-violating text changed
- Change log:
  - Which sections were modified
  - Original text (before)
  - Updated text (after)
  - Reason for change (linked to which policy rule)

**Rules**:
- NEVER change HTML structure or CSS
- NEVER reorder sections
- NEVER add new claims
- NEVER invent disclaimers
- NEVER weaken compliant copy
- NEVER apply changes where no violation exists
- Edit only at phrase/sentence level, not entire paragraphs
- Testimonials: rephrase only the violating part, keep emotional tone
- If removal is unavoidable, remove minimum text required, keep formatting intact
- This is a surgical compliance editor, not a rewriter

**Depends on**: Nothing. Works on any existing HTML page.

**Complexity**: Medium (prompt engineering for "surgical edits without over-editing" is the challenge)

---

## Agent 4: Funnel Optimization Agent (CRO)

**Purpose**: Analyzes an existing landing page for missing conversion elements and adds 1-3 smart enhancements to increase conversion rate.

**Input**:
- Full HTML + CSS of an existing page
- Optional context: product type, market (e.g., Germany), traffic source (native, social, search)
- Conversion playbook (predefined library of proven conversion elements)

**What it does**:
1. Receives existing page HTML
2. Analyzes the page against the conversion playbook checklist:
   - Is there enough trust above the fold?
   - Is there social proof?
   - Is there authority or expert presence?
   - Is the product visually clear?
   - Is the page text-heavy without visual breaks?
   - Are there reassurance elements near CTAs?
   - Are key conversion elements missing entirely?
3. Identifies what's missing
4. Selects 1-3 enhancements from the playbook (limited to prevent clutter):
   - Trust: testimonial blocks, review-style blocks, "used by thousands" signals
   - Authority: doctor/expert section, expert quotes, professional portraits
   - Clarity: benefit bullets, "how it works" micro-sections, FAQ blocks
   - Reassurance: refund/guarantee badges, shipping clarity
   - Visual: images breaking long text, product close-ups
5. Generates new HTML blocks that reuse existing CSS classes for consistency
6. Inserts blocks at logical positions between existing sections
7. Generates/fetches contextual images for new sections

**Output**:
- Updated HTML + CSS (same page, just enhanced)
- Optimization summary:
  - What was added
  - Why it was added
  - Where it was added

**Rules**:
- NEVER rewrite the main copy
- NEVER change the core message
- NEVER redesign the layout
- NEVER remove sections
- NEVER change brand tone
- NEVER touch pricing or offer logic
- NEVER introduce new design systems or break responsiveness
- Apply limited changes per run (1-3 max)
- Prefer adding over modifying
- If page already has strong trust elements, do less
- New blocks must reuse existing CSS classes, match spacing, typography, and layout
- This agent augments, it does not rebuild

**Depends on**: Conversion playbook (does Med have this written down, or is it tribal knowledge?)

**Complexity**: HIGH — Hardest agent. Understanding existing CSS, generating matching HTML blocks, placing them correctly, and image generation all in one. Most of the time will be spent on prompt engineering and testing.

---

## Agent 5: Product Research Agent (Guided Approach)

**Purpose**: Helps discover potential winning products by guiding the user through Facebook Ad Library / spy tool research, then structuring and analyzing the raw data they collect.

**Input**:
- Keywords (e.g., "pain relief", "posture", "sleep", "foot pain")
- Product type/category (e.g., "health devices", "supplements", "beauty tools")
- Target markets (e.g., Germany, USA, UK)
- Selection criteria (ad activity, angle diversity, competition level, policy risk)

**What it does**:
1. Receives keywords, markets, and criteria
2. Gives the user step-by-step instructions:
   - "Go to Facebook Ad Library"
   - "Search 'pain relief' in Germany"
   - "Filter by active ads"
   - "Copy the first 20 results and paste them here"
3. User pastes raw data from Ad Library / spy tools
4. Agent automatically:
   - Parses the raw text into structured data
   - Identifies individual products
   - Extracts: product name, advertiser, ad copy angles, category, markets, links
   - Evaluates against selection criteria (activity, competition, policy risk)
   - Flags products worth testing
5. Repeats for each keyword/market combination

**Output**:
- Structured research report per product:
  - Product name
  - Category
  - Market(s)
  - Ad Library link
  - Landing page link (if found)
  - Short description of the offer
  - Observed ad angles
  - Competition / saturation notes
  - Policy risk notes
  - Verdict: worth testing or not

**Rules**:
- NEVER invent product details
- NEVER guess links it cannot verify
- NEVER assume performance metrics not visible
- NEVER label products as "winners"
- NEVER create marketing copy
- NEVER suggest claims or angles
- It only finds, structures, and reports

**Note**: Filip proposed this guided approach instead of automated scraping (Med's original spec). Scraping Facebook Ad Library is unreliable, breaks constantly, and violates ToS. The guided approach gives the same structured output without the maintenance headache. If Med insists on full automation, that's a separate project with separate pricing.

**Depends on**: Nothing. No HTML involved.

**Complexity**: Low-medium (simple conversational agent loop with structured output)

---

## Shared Technical Pattern

All 5 agents follow the same core architecture:

```
Input (HTML / text / data)
    ↓
Parse & Extract (BeautifulSoup for HTML, text processing for Agent 5)
    ↓
LLM Processing (OpenAI / Anthropic API with specific instructions per agent)
    ↓
Apply Changes (reinsert into HTML / structure data)
    ↓
Validate Output (HTML structure check, change log)
    ↓
Return (modified HTML + summary/log)
```

**Tech Stack**: Python, FastAPI, BeautifulSoup/lxml, OpenAI/Anthropic API, Image Generation API (TBD)

---

## Open Questions (To Resolve on Call)

| # | Question | Why It Matters |
|---|----------|----------------|
| 1 | What do the HTML templates actually look like? Placeholder format? | Determines how Agent 1 parser works |
| 2 | What funnel builder do they use? | Tells us how clean/messy the HTML exports are |
| 3 | Are templates ready or still being built? | Agent 1 is blocked without them |
| 4 | Image generation: which API? Who pays? Or do they have an image library? | Adds cost and complexity to Agents 1 & 4 |
| 5 | How will the team use these agents? CLI? API? Web UI? | UI work = major scope increase |
| 6 | Does the conversion playbook exist in writing? | Agent 4 needs this as input |
| 7 | Is Med OK with guided approach for Agent 5? | If he wants scraping, that's a different project |
| 8 | Which agent is highest priority? | Determines delivery order |
| 9 | How many revision rounds per agent? | Prevents infinite iteration |
| 10 | What languages beyond German? | Affects Agent 2 design |

