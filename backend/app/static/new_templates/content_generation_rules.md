# Content Generation Rules for Landing Page Templates

This document defines the AI-generated content rules for all placeholders across templates.

---

## PART 1: GLOBAL PLACEHOLDER RULES (Apply to ALL templates)

### 1.1 Author Info Section
**Placeholder:** `[Author info goes here]`

**Output Format:**
```
[Author Name] | Verifiziert | [Date] | [Credentials/Bio snippet]
```

**Example:**
```
Dr. Maria Schmidt | Verifiziert | 23. Januar 2025 | Fachärztin für Innere Medizin, 15 Jahre Erfahrung
```

**Rules:**
- Always include the "Verifiziert" (Verified) label
- Use German date format (DD. Month YYYY)
- Include relevant credentials/specialization
- Keep credentials concise (1 line)

---

### 1.2 Date of Last Edit
**Placeholder:** `[Date of last edit goes here]`

**Output Format:**
```
Zuletzt aktualisiert: [German formatted date]
```

**Example:**
```
Zuletzt aktualisiert: 15. Februar 2025
```

**Rules:**
- Use German date format
- Prefix with "Zuletzt aktualisiert:" (Last updated:)
- Date should be recent (within last 30 days)

---

### 1.3 Body Section Text Formatting
**Placeholder:** `[Body section goes here]`

**Core Rule:** Each body section should be 2-3 short sentences per paragraph. Vary the rhythm between sections.

**Style Guidelines:**
- Short punchy paragraphs (2-3 sentences max)
- Use `<br>` tags between major beats for visual breathing room
- Fragment sentences for emphasis ("Three weeks later." / "Nothing worked.")
- Specific details (names, ages, numbers, timeframes)
- Each section should have its own flow - don't repeat the same pattern
- NO walls of text
- NO generic marketing language

**Example Rhythms (vary across sections):**

*Rhythm A - Story Opening:*
```html
Maria war 47, als es begann. Jeden Morgen das gleiche Spiel.
<br>
Der Wecker klingelt um 6:00 Uhr. Aber aufstehen? Unmöglich.
```

*Rhythm B - Building Tension:*
```html
Sie probierte Tabletten. Dann Tee. Dann Meditation.
<br>
Nichts funktionierte.
<br>
Drei Monate später wurde es schlimmer.
```

*Rhythm C - Emotional Beat:*
```html
"Ich konnte nicht mehr", sagt sie heute.
<br>
Dunkle Augenringe. Erschöpft. Hoffnungslos.
```

*Rhythm D - Cliffhanger:*
```html
Dann fand sie etwas Unerwartetes.
<br>
Etwas, das ihre Kollegen jahrelang ignoriert hatten.
```

---

### 1.4 Reviews/Testimonials
**Placeholders:** `[Review goes here]`, `[Review person name goes here]`, `[Review person image goes here]`, `[Review person location goes here]` (template 004 only)

**Rules:**
- Keep reviews SHORT (2-4 sentences max)
- Write like real humans (casual, not polished)
- Include small imperfections (not every review is 100% positive)
- Mention specific results or timeframes
- Vary the tone (some enthusiastic, some matter-of-fact)
- Use German language

**BAD Example (too generic):**
```
"Dieses Produkt hat mein Leben verändert! Ich kann nicht glauben, wie erstaunlich es ist. Ich empfehle es jedem!"
```

**GOOD Example (human-like):**
```
"Hat etwa 2 Wochen gedauert, bis ich etwas gemerkt habe. Jetzt schlafe ich zum ersten Mal seit Monaten durch. Hätte es früher finden sollen."
```

**More GOOD Examples:**
```
"Anfangs war ich skeptisch, aber nach 3 Wochen... wow. Mein Mann hat den Unterschied als Erster bemerkt."
```

```
"Nicht perfekt, aber deutlich besser als alles andere, was ich probiert habe. 4 von 5 Sternen."
```

```
"Funktioniert. Einfach. Keine Nebenwirkungen bei mir."
```

---

### 1.5 Social Proof Content
**Placeholders:** `[Social proof goes here]`, `[Social proof person/group goes here]`

**Rules:**
- Quote from experts, doctors, or studies
- Include credentials/affiliation
- Keep scientific but accessible
- Use specific numbers when possible

**Example:**
```
"Nach unserer 12-wöchigen Studie mit 847 Teilnehmern sehen wir signifikante Verbesserungen bei 78% der Gruppe."

– Prof. Dr. Hans Weber, Universitätsklinikum München
```

---

## PART 2: TEMPLATE-SPECIFIC RULES

### Template 001 - Standard Advertorial
- Uses full author info with image
- Has social proof group (repeatable)
- Standard body sections with titles

### Template 002 - Case Study Focus
- Emphasizes case study narrative
- Body sections without titles (just image + content)
- Introduction image should be placed AFTER intro text

### Template 003 - Clean Article Style
- News/article feel
- Post category visible
- Check Availability button in offer section
- Reviews in different order (Image + Review text + Name)

### Template 004 - Listicle Style
- Numbered items (1., 2., 3., etc.)
- Reviewer location included
- Hook after headline image
- Product reveal section

**Listicle Title Format:**
```
1. [Title for first point]
2. [Title for second point]
3. [Title for third point]
```

### Template 005 - Comprehensive
- Has subheadline
- Social proof group (repeatable)
- References section
- Larger social proof section (reduce size in CSS)

---

## PART 3: IMAGE CONTEXT RULES

When generating images, use these context sources:

| Placeholder | Context Source | Description |
|------------|----------------|-------------|
| Headline image | headline + introduction | Hero image for entire page |
| Author image | author_info | Professional headshot |
| Body section image | That body section's content | Relevant to specific section |
| Product image | product_content | Clear product shot |
| Case study image | case_study content | Before/after, person, situation |
| Listicle item image | That listicle item's content | Illustrates specific point |
| Social proof image | social_proof content | Expert/doctor photo |
| Review person image | review content | Realistic human matching reviewer |
| Offer image | offer_content | Product bundle, packaging |

---

## PART 4: FORMATTING RULES

### Line Breaks
- Use `<br>` for visual breathing room between beats
- Don't overuse - 1-2 per section maximum
- Use after dramatic statements or quotes

### Paragraphs
- Maximum 3 sentences per paragraph
- Vary paragraph length (1-3 sentences)
- Each section should have different rhythm

### Emphasis
- Use `<strong>` or `<b>` sparingly
- Fragment sentences for impact
- Specific numbers always stand out

### Language
- Write in German
- Conversational but professional tone
- Avoid marketing buzzwords
- Be specific, not generic

