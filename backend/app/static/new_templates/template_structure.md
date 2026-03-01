# Template Placeholder Structure

This document describes all placeholders in each HTML template, listed in document order.
Each placeholder is marked as either `[TXT]` (text content) or `[IMG]` (image src attribute).

---

## How Repeatable Sections Work

### The Problem
Templates have ONE instance of each repeatable section (e.g., one review block), but user content may have MULTIPLE items (e.g., 5 reviews).

### The Solution: HTML Comment Markers

Each repeatable section in the templates is wrapped with HTML comment markers:

```html
<!-- REPEAT:review:START -->
<div class="review-card ...">
  <img src="[Review person image goes here]" />
  <h4>[Review person name goes here]</h4>
  <p>[Review goes here]</p>
</div>
<!-- REPEAT:review:END -->
```

### Marker Summary by Template

| Template | Repeatable Sections |
|----------|---------------------|
| template_001 | `body`, `social_proof`, `review` |
| template_002 | `body`, `review` |
| template_003 | `body`, `review` |
| template_004 | `body`, `review` |
| template_005 | `body`, `social_proof`, `review` |

### Implementation Strategy

**Step 1: Find Markers**
```python
import re

def extract_repeatable_block(html, section_name):
    pattern = rf'<!--\s*REPEAT:{section_name}:START\s*-->(.*?)<!--\s*REPEAT:{section_name}:END\s*-->'
    match = re.search(pattern, html, re.DOTALL)
    if match:
        return match.group(0), match.group(1)  # full match, inner content
    return None, None
```

**Step 2: Clone and Fill**

For each item in user content:
1. Clone the extracted HTML block (the content between START and END markers)
2. Replace placeholders with actual content
3. Regenerate all `id="cc-id-xxx"` attributes to avoid duplicates

**Step 3: Replace Original**

Replace the original marked block with all cloned blocks (without the markers).

### ID Regeneration

All `id="cc-id-..."` attributes must be regenerated to avoid duplicate IDs:

```python
import re
import uuid

def regenerate_ids(html_block, prefix):
    def replace_id(match):
        return f'id="cc-id-{prefix}-{uuid.uuid4().hex[:8]}"'
    return re.sub(r'id="cc-id-[^"]*"', replace_id, html_block)
```

### Example: Processing 3 Reviews

**Input:** User provides 3 reviews
```python
reviews = [
    {"name": "Maria S.", "text": "Amazing product!", "image": "url1"},
    {"name": "John D.", "text": "Life changing!", "image": "url2"},
    {"name": "Anna K.", "text": "Highly recommend!", "image": "url3"}
]
```

**Template has:**
```html
<!-- REPEAT:review:START -->
<div class="review-card" id="cc-id-abc123">
  <img src="[Review person image goes here]" id="cc-id-def456" />
  <h4 id="cc-id-ghi789">[Review person name goes here]</h4>
  <p id="cc-id-jkl012">[Review goes here]</p>
</div>
<!-- REPEAT:review:END -->
```

**Output:** 3 review cards (markers removed, IDs regenerated):
```html
<div class="review-card" id="cc-id-rev1-a1b2c3d4">
  <img src="url1" id="cc-id-rev1-e5f6g7h8" />
  <h4 id="cc-id-rev1-i9j0k1l2">Maria S.</h4>
  <p id="cc-id-rev1-m3n4o5p6">Amazing product!</p>
</div>
<div class="review-card" id="cc-id-rev2-q7r8s9t0">
  ...
</div>
<div class="review-card" id="cc-id-rev3-u1v2w3x4">
  ...
</div>
```

### Important Notes

1. **Markers are removed** from final output
2. **Empty content**: If user provides 0 items, remove the entire block (including markers)
3. **Preserve styling**: Keep all `class`, `style`, and `data-*` attributes intact

---

## Template 001

| Order | Type | Placeholder | Description |
|-------|------|-------------|-------------|
| 1 | TXT | `[Headline goes here]` | Main headline/title of the advertorial |
| 2 | TXT | `[Hook goes here]` | Opening hook text to grab attention |
| 3 | IMG | `[Headline image goes here]` | Hero/main image below the headline |
| 4 | IMG | `[Author image goes here]` | Author profile photo |
| 5 | TXT | `[Author info goes here]` | Author name and credentials |
| 6 | TXT | `[Date of last edit goes here]` | Publication/edit date |
| 7 | TXT | `[Introduction goes here]` | Introduction paragraph(s) |
| 8 | TXT | `[Body section title goes here]` | Title for body content section |
| 9 | IMG | `[Body section image goes here]` | Image for body content section |
| 10 | TXT | `[Body section goes here]` | Main body content text |
| 11 | TXT | `[Product presentation title goes here]` | Title for product section |
| 12 | IMG | `[Product presentation image goes here]` | Product image |
| 13 | TXT | `[Product presentation goes here]` | Product description text |
| 14 | IMG | `[Social proof person/group image goes here]` | Image of person/group providing social proof |
| 15 | TXT | `[Social proof person/group goes here]` | Name/description of social proof source |
| 16 | TXT | `[Social proof goes here]` | Social proof content/quote |
| 17 | IMG | `[Main social proof image goes here]` | Main social proof section image |
| 18 | TXT | `[Main Social proof goes here]` | Main social proof content |
| 19 | TXT | `[Offer section title goes here]` | Title for the offer/CTA section |
| 20 | IMG | `[Offer section image goes here]` | Image for offer section |
| 21 | TXT | `[Offer section goes here]` | Offer details and CTA text |
| 22 | IMG | `[Review person image goes here]` | Reviewer profile photo *(repeatable)* |
| 23 | TXT | `[Review person name goes here]` | Reviewer name *(repeatable)* |
| 24 | TXT | `[Review goes here]` | Review/testimonial text *(repeatable)* |

---

## Template 002

| Order | Type | Placeholder | Description |
|-------|------|-------------|-------------|
| 1 | TXT | `[Headline goes here]` | Main headline/title of the advertorial |
| 2 | TXT | `[Subheadline goes here]` | Secondary headline/subtitle |
| 3 | IMG | `[Headline image goes here]` | Hero/main image |
| 4 | TXT | `[Hook goes here]` | Opening hook text |
| 5 | IMG | `[Author image goes here]` | Author profile photo |
| 6 | TXT | `[Author info goes here]` | Author name and credentials |
| 7 | TXT | `[Date of last edit goes here]` | Publication/edit date |
| 8 | TXT | `[Introduction goes here]` | Introduction paragraph(s) |
| 9 | IMG | `[Introduction image goes here]` | Image for introduction section |
| 10 | TXT | `[Body section goes here]` | Main body content text |
| 11 | IMG | `[Body section image goes here]` | Image for body content |
| 12 | TXT | `[Product presentation title goes here]` | Title for product section |
| 13 | IMG | `[Product presentation image goes here]` | Product image |
| 14 | TXT | `[Product presentation goes here]` | Product description text |
| 15 | TXT | `[Case study title goes here]` | Title for case study section |
| 16 | IMG | `[Case study image goes here]` | Case study image |
| 17 | TXT | `[Case study goes here]` | Case study content |
| 18 | TXT | `[Main Social proof title goes here]` | Title for main social proof section |
| 19 | IMG | `[Main social proof image goes here]` | Main social proof image |
| 20 | TXT | `[Main Social proof goes here]` | Main social proof content |
| 21 | TXT | `[Offer section title goes here]` | Title for offer/CTA section |
| 22 | IMG | `[Offer section image goes here]` | Image for offer section |
| 23 | TXT | `[Offer section goes here]` | Offer details and CTA text |
| 24 | IMG | `[Review person image goes here]` | Reviewer profile photo *(repeatable)* |
| 25 | TXT | `[Review person name goes here]` | Reviewer name *(repeatable)* |
| 26 | TXT | `[Review goes here]` | Review/testimonial text *(repeatable)* |

---

## Template 003

| Order | Type | Placeholder | Description |
|-------|------|-------------|-------------|
| 1 | TXT | `[POST CATEGORY GOES HERE]` | Category/breadcrumb label |
| 2 | TXT | `[Headline goes here]` | Main headline/title |
| 3 | IMG | `[Headline image goes here]` | Hero/main image |
| 4 | TXT | `[Author info goes here]` | Author name and credentials |
| 5 | TXT | `[Date of last edit goes here]` | Publication/edit date |
| 6 | TXT | `[Introduction goes here]` | Introduction paragraph(s) |
| 7 | TXT | `[Body section title goes here]` | Title for body content section |
| 8 | IMG | `[Body section image goes here]` | Image for body content |
| 9 | TXT | `[Body section goes here]` | Main body content text |
| 10 | TXT | `[Product presentation title goes here]` | Title for product section |
| 11 | IMG | `[Product presentation image goes here]` | Product image |
| 12 | TXT | `[Product presentation goes here]` | Product description text |
| 13 | TXT | `[Case study title goes here]` | Title for case study section |
| 14 | IMG | `[Case study image goes here]` | Case study image |
| 15 | TXT | `[Case study goes here]` | Case study content |
| 16 | TXT | `[Offer section title goes here]` | Title for offer/CTA section |
| 17 | IMG | `[Offer section image goes here]` | Image for offer section |
| 18 | TXT | `[Offer section goes here]` | Offer details and CTA text |
| 19 | IMG | `[Review person image goes here]` | Reviewer profile photo *(repeatable)* |
| 20 | TXT | `[Review goes here]` | Review/testimonial text *(repeatable)* |
| 21 | TXT | `[Review person name goes here]` | Reviewer name *(repeatable)* |

---

## Template 004 (Listicle Style)

| Order | Type | Placeholder | Description |
|-------|------|-------------|-------------|
| 1 | TXT | `[POST CATEGORY GOES HERE]` | Category/breadcrumb label |
| 2 | TXT | `[Headline goes here]` | Main headline/title |
| 3 | IMG | `[Author image goes here]` | Author profile photo |
| 4 | TXT | `[Author info goes here]` | Author name and credentials |
| 5 | TXT | `[Date of last edit goes here]` | Publication/edit date |
| 6 | IMG | `[Headline image goes here]` | Hero/main image |
| 7 | TXT | `[Hook goes here]` | Opening hook text |
| 8 | TXT | `[Listicle item title goes here (1., 2., 3.,)]` | Numbered list item title *(repeatable)* |
| 9 | TXT | `[Listicle item goes here]` | List item content *(repeatable)* |
| 10 | IMG | `[Listicle item image goes here]` | List item image *(repeatable)* |
| 11 | TXT | `[Product reveal goes here]` | Product reveal/introduction text |
| 12 | IMG | `[Product presentation image goes here]` | Product image |
| 13 | IMG | `[Review person image goes here]` | Reviewer profile photo *(repeatable)* |
| 14 | TXT | `[Review person name goes here]` | Reviewer name *(repeatable)* |
| 15 | TXT | `[Review person location goes here]` | Reviewer location *(repeatable)* |
| 16 | TXT | `[Review goes here]` | Review/testimonial text *(repeatable)* |
| 17 | TXT | `[Offer section title goes here]` | Title for offer/CTA section |
| 18 | IMG | `[Offer section image goes here]` | Image for offer section |
| 19 | TXT | `[Offer section goes here]` | Offer details and CTA text |
| 20 | TXT | `[References goes here]` | References/sources section |

---

## Template 005

| Order | Type | Placeholder | Description |
|-------|------|-------------|-------------|
| 1 | TXT | `[POST CATEGORY GOES HERE]` | Category/breadcrumb label |
| 2 | TXT | `[Headline goes here]` | Main headline/title |
| 3 | IMG | `[Headline image goes here]` | Hero/main image |
| 4 | TXT | `[Subheadline goes here]` | Secondary headline/subtitle |
| 5 | TXT | `[Author info goes here]` | Author name and credentials |
| 6 | TXT | `[Date of last edit goes here]` | Publication/edit date |
| 7 | TXT | `[Introduction goes here]` | Introduction paragraph(s) |
| 8 | TXT | `[Body section title goes here]` | Title for body content section |
| 9 | IMG | `[Body section image goes here]` | Image for body content |
| 10 | TXT | `[Body section goes here]` | Main body content text |
| 11 | TXT | `[Product presentation title goes here]` | Title for product section |
| 12 | IMG | `[Product presentation image goes here]` | Product image |
| 13 | TXT | `[Product presentation goes here]` | Product description text |
| 14 | TXT | `[Main Social proof title goes here]` | Title for main social proof section |
| 15 | IMG | `[Social proof person/group image goes here]` | Image of person/group for social proof |
| 16 | TXT | `[Social proof person/group goes here]` | Name/description of social proof source |
| 17 | TXT | `[Social proof goes here]` | Social proof content/quote |
| 18 | TXT | `[Offer section title goes here]` | Title for offer/CTA section |
| 19 | IMG | `[Offer section image goes here]` | Image for offer section |
| 20 | TXT | `[Offer section goes here]` | Offer details and CTA text |
| 21 | IMG | `[Review person image goes here]` | Reviewer profile photo *(repeatable)* |
| 22 | TXT | `[Review person name goes here]` | Reviewer name *(repeatable)* |
| 23 | TXT | `[Review goes here]` | Review/testimonial text *(repeatable)* |
| 24 | TXT | `[References goes here]` | References/sources section |

---

## Placeholder Comparison Matrix

| Placeholder | T001 | T002 | T003 | T004 | T005 |
|-------------|:----:|:----:|:----:|:----:|:----:|
| `[POST CATEGORY GOES HERE]` | ✗ | ✗ | ✓ | ✓ | ✓ |
| `[Headline goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Headline image goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Subheadline goes here]` | ✗ | ✓ | ✗ | ✗ | ✓ |
| `[Hook goes here]` | ✓ | ✓ | ✗ | ✓ | ✗ |
| `[Author image goes here]` | ✓ | ✓ | ✗ | ✓ | ✗ |
| `[Author info goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Date of last edit goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Introduction goes here]` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `[Introduction image goes here]` | ✗ | ✓ | ✗ | ✗ | ✗ |
| `[Body section title goes here]` | ✓ | ✗ | ✓ | ✗ | ✓ |
| `[Body section image goes here]` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `[Body section goes here]` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `[Product presentation title goes here]` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `[Product presentation image goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Product presentation goes here]` | ✓ | ✓ | ✓ | ✗ | ✓ |
| `[Product reveal goes here]` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `[Listicle item title goes here]` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `[Listicle item goes here]` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `[Listicle item image goes here]` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `[Case study title goes here]` | ✗ | ✓ | ✓ | ✗ | ✗ |
| `[Case study image goes here]` | ✗ | ✓ | ✓ | ✗ | ✗ |
| `[Case study goes here]` | ✗ | ✓ | ✓ | ✗ | ✗ |
| `[Social proof person/group image goes here]` | ✓ | ✗ | ✗ | ✗ | ✓ |
| `[Social proof person/group goes here]` | ✓ | ✗ | ✗ | ✗ | ✓ |
| `[Social proof goes here]` | ✓ | ✗ | ✗ | ✗ | ✓ |
| `[Main Social proof title goes here]` | ✗ | ✓ | ✗ | ✗ | ✓ |
| `[Main social proof image goes here]` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `[Main Social proof goes here]` | ✓ | ✓ | ✗ | ✗ | ✗ |
| `[Offer section title goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Offer section image goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Offer section goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Review person image goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Review person name goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[Review person location goes here]` | ✗ | ✗ | ✗ | ✓ | ✗ |
| `[Review goes here]` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `[References goes here]` | ✗ | ✗ | ✗ | ✓ | ✓ |

---

## Common Placeholders (All Templates)

These placeholders exist in ALL 5 templates:

- `[Headline goes here]` - Main headline
- `[Headline image goes here]` - Hero image
- `[Author info goes here]` - Author credentials
- `[Date of last edit goes here]` - Publication date
- `[Offer section title goes here]` - Offer title
- `[Offer section image goes here]` - Offer image
- `[Offer section goes here]` - Offer content
- `[Review person image goes here]` - Reviewer photo *(repeatable)*
- `[Review person name goes here]` - Reviewer name *(repeatable)*
- `[Review goes here]` - Review text *(repeatable)*

---

## Template Selection Guide

| Use Case | Recommended Template |
|----------|---------------------|
| Standard advertorial with social proof | Template 001 or 005 |
| Advertorial with case study | Template 002 or 003 |
| Listicle-style content (numbered items) | Template 004 |
| Content with subheadline | Template 002 or 005 |
| Content with references/sources | Template 004 or 005 |
| Content with post category | Template 003, 004, or 005 |

---

## Repeatable Section Groups

Sections marked as *(repeatable)* come in **groups** that must be duplicated together. The AI agent should duplicate the entire group's HTML structure based on the number of items in the provided content.

### Body Section Group *(repeatable)*

Templates: 001, 003, 005

| Component | Type | Description |
|-----------|------|-------------|
| `[Body section title goes here]` | TXT | Section heading (optional in some templates) |
| `[Body section image goes here]` | IMG | Image relevant to THIS specific body section's content |
| `[Body section goes here]` | TXT | Body paragraph(s) for this section |

**Note:** Template 002 has body section but WITHOUT title. The group is just: image + content.

**Note:** Template 004 uses "Listicle items" instead of body sections:
- `[Listicle item title goes here (1., 2., 3.,)]`
- `[Listicle item goes here]`
- `[Listicle item image goes here]`

### Review Group *(repeatable)*

Templates: ALL (001, 002, 003, 004, 005)

| Component | Type | Description |
|-----------|------|-------------|
| `[Review person image goes here]` | IMG | Photo of the reviewer (real person face) |
| `[Review person name goes here]` | TXT | Reviewer's name |
| `[Review person location goes here]` | TXT | Reviewer's location *(Template 004 only)* |
| `[Review goes here]` | TXT | The testimonial/review text |

### Social Proof Group *(repeatable)*

Templates: 001, 005

| Component | Type | Description |
|-----------|------|-------------|
| `[Social proof person/group image goes here]` | IMG | Photo of the person/group giving social proof |
| `[Social proof person/group goes here]` | TXT | Name/title of the person or group |
| `[Social proof goes here]` | TXT | The social proof statement/quote |

---

## Non-Repeatable Standalone Sections

These sections appear ONCE per template and should NOT be duplicated.

### Case Study Section *(non-repeatable)*

Templates: 002, 003

| Component | Type | Description |
|-----------|------|-------------|
| `[Case study title goes here]` | TXT | Case study heading |
| `[Case study image goes here]` | IMG | Image relevant to the case study content |
| `[Case study goes here]` | TXT | Case study content/story |

### Main Social Proof Section *(non-repeatable)*

Templates: 001, 002 (partial in 005)

This is a **standalone section** different from the repeatable Social Proof Group above. It typically contains scientific backing, study results, or major credibility elements.

| Component | Type | Templates | Description |
|-----------|------|-----------|-------------|
| `[Main Social proof title goes here]` | TXT | 002, 005 | Section heading for main social proof |
| `[Main social proof image goes here]` | IMG | 001, 002 | Supporting image (charts, study graphics, credentials) |
| `[Main Social proof goes here]` | TXT | 001, 002 | Detailed social proof content (studies, statistics, expert backing) |

**Key Difference:**
- **Social Proof Group** (repeatable): Individual testimonials/quotes from people - can have multiple
- **Main Social Proof Section** (non-repeatable): One major credibility section with studies/statistics/science

### Product Presentation Section *(non-repeatable)*

Templates: 001, 002, 003, 005

| Component | Type | Description |
|-----------|------|-------------|
| `[Product presentation title goes here]` | TXT | Title introducing the product |
| `[Product presentation image goes here]` | IMG | Product shot |
| `[Product presentation goes here]` | TXT | Product description and benefits |

### Product Reveal Section *(non-repeatable)*

Templates: 004 only

| Component | Type | Description |
|-----------|------|-------------|
| `[Product reveal goes here]` | TXT | Text revealing/introducing the product after listicle items |
| `[Product presentation image goes here]` | IMG | Product shot |

### Offer Section *(non-repeatable)*

Templates: ALL

| Component | Type | Description |
|-----------|------|-------------|
| `[Offer section title goes here]` | TXT | CTA/offer section heading |
| `[Offer section image goes here]` | IMG | Product bundle, packaging, or promotional image |
| `[Offer section goes here]` | TXT | Offer details, pricing, CTA text |

### Introduction Section *(non-repeatable)*

Templates: 001, 002, 003, 005

| Component | Type | Templates | Description |
|-----------|------|-----------|-------------|
| `[Introduction goes here]` | TXT | 001, 002, 003, 005 | Opening paragraphs after headline/hook |
| `[Introduction image goes here]` | IMG | 002 only | Image supporting the introduction |

### References Section *(non-repeatable)*

Templates: 004, 005

| Component | Type | Description |
|-----------|------|-------------|
| `[References goes here]` | TXT | Sources, citations, disclaimers |

---

## Image Context Guidelines

Each image placeholder requires contextually appropriate imagery:

### Global/Page-Level Images

| Placeholder | Image Should Show |
|-------------|-------------------|
| `[Headline image goes here]` | Hero image representing the ENTIRE page context/topic. Should capture the main theme of the advertorial. |
| `[Author image goes here]` | Professional headshot of the author/expert |
| `[Product presentation image goes here]` | Clear product shot or product-in-use image |
| `[Offer section image goes here]` | Product packaging, bundle, or promotional image |

### Section-Specific Images (Context from surrounding text)

| Placeholder | Image Should Show |
|-------------|-------------------|
| `[Body section image goes here]` | Image relevant to THAT specific body section's content. Read the body text to determine appropriate imagery. |
| `[Introduction image goes here]` | Image setting up the story/problem (Template 002 only) |
| `[Case study image goes here]` | Image relevant to the case study story - could be before/after, person mentioned, or situation described |
| `[Listicle item image goes here]` | Image illustrating THAT specific numbered point |
| `[Main social proof image goes here]` | Supporting image for main social proof section (charts, studies, credentials) |

### Person Images (Require realistic human faces)

| Placeholder | Image Should Show |
|-------------|-------------------|
| `[Review person image goes here]` | Realistic photo of the reviewer - should match the name/demographic implied |
| `[Social proof person/group image goes here]` | Photo of the expert, doctor, group, or authority providing the social proof |

---

## Content Formatting Guidelines

### Body Section Text
- **MAX 150 words** per section
- **2-3 sentences** per paragraph (short and punchy!)
- Use `<br>` tags for visual breathing room between beats
- Use **fragment sentences** for dramatic effect ("Nothing worked." / "Three weeks later.")
- Include **specific details** (names, ages, numbers, timeframes)
- **VARY THE RHYTHM** - each section should feel different

**Example Rhythms:**

*Rhythm A - Story Opening:*
```html
Maria was 47 when it started. Every morning, the same struggle.<br><br>
The alarm rings at 6 AM. But getting up? <b>Impossible</b>.
```

*Rhythm B - Building Tension:*
```html
She tried pills. Then tea. Then meditation.<br><br>
Nothing worked.<br><br>
Three months later, it got worse.
```

*Rhythm C - Emotional Beat:*
```html
<i>"I couldn't do it anymore,"</i> she says today.<br><br>
Dark circles. Exhausted. Hopeless.
```

### Listicle Item Text (Template 004)
- **MAX 100 words** per item
- Numbered titles: "1. [Title]", "2. [Title]", etc.
- Focus on ONE key point per item
- Keep it scannable

### Reviews/Testimonials
- **2-4 sentences MAXIMUM** - keep them SHORT!
- Write like **real humans** - casual, not polished
- Include **small imperfections** (not every review is 100% positive)
- Mention **specific results/timeframes** ("after 2 weeks", "in 3 days")
- **VARY the tone** - some enthusiastic, some matter-of-fact

**BAD Example (too generic):**
```
"This product changed my life! I can't believe how amazing it is. I recommend it to everyone!"
```

**GOOD Examples (human-like):**
```
"Took about 2 weeks to notice anything. Now I'm sleeping through the night. Wish I found this sooner."
```
```
"Not perfect, but way better than what I tried before. My husband noticed the difference first."
```
```
"Works. Simple as that. No weird side effects either."
```

### Social Proof Content
- **1-2 sentences MAX** per social proof
- Format: "[Short quote]" – [Name], [Title/Credentials]
- Keep it brief and credible

---

## Template Structure Summary

### Template 001 - Standard Advertorial
- Has: Hook, Social proof group, Main social proof
- Repeatable: Body sections, Social proof, Reviews
- Best for: Standard advertorial with expert endorsements

### Template 002 - Case Study Focus  
- Has: Subheadline, Introduction image, Case study section
- Repeatable: Reviews, Case studies
- Best for: Story-driven content with case studies

### Template 003 - Clean Article Style
- Has: Post category, Case study section
- Repeatable: Body sections, Case studies, Reviews
- Best for: News/article style advertorial

### Template 004 - Listicle Style
- Has: Listicle items, Product reveal, Reviewer location, References
- Repeatable: Listicle items, Reviews
- Best for: "X Reasons Why..." or numbered list content

### Template 005 - Comprehensive
- Has: Post category, Subheadline, Social proof group, References
- Repeatable: Body sections, Social proof, Reviews
- Best for: Long-form comprehensive advertorial

