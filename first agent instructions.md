# BRIEF FOR AI ENGINEER

**Project:** Template-Aware Copy & Image Injection AI Agent

---

## 1. Project Goal

Build an AI agent that automatically generates complete landing pages by filling predefined HTML templates with provided marketing copy and relevant images.

**Expected workflow:**

1. User selects one of our pre-saved HTML templates
2. User provides advertorial copy (raw or lightly structured)
3. The AI agent:
   - Understands the template layout
   - Understands the copy
   - Fills the template correctly
   - Generates and places images where required
4. The system outputs final HTML + CSS, ready to publish

> No manual copy placement should be needed in normal usage.

---

## 2. Template System (Very Important)

We will maintain 5–6 predefined templates internally. Each template:

- Has a base layout with sections (headline, hook, body, reviews, CTA, etc.)
- Contains explicit placeholders for content
- Defines the styling and visual structure

**Example placeholders** (conceptual, not code-specific):

- `"Headline goes here"`
- `"Hook text goes here"`
- `"Body content goes here"`
- `"Product section content"`
- `"Testimonial/Review content"`
- `"CTA text"`
- `"Image placeholder"`

These placeholders are edited and maintained by us inside our funnel builder.

**The AI agent uses templates as a starting point but MUST adapt the HTML structure to match the provided content.** For example: if the template has 2 review slots but the raw text contains 4 reviews, the agent must duplicate the review section markup to render all 4 reviews. The styling remains consistent (using the same CSS classes), but the number of repeated sections is driven by the content, not the template.

---

## 3. What the AI Agent Must Understand

### A. Template Awareness

When a template is selected, the AI agent must already understand:

- Where the main headline lives
- Where the hook/subheadline lives
- Where hero images are expected
- Where the long advertorial body goes
- Where the product presentation section is
- Where testimonials/reviews appear
- Where CTAs appear
- Where legal/disclaimer text goes
- **Which sections are repeatable** (e.g., reviews, testimonials, product cards)

This understanding is predefined per template, not inferred dynamically. The agent should treat templates as known page blueprints, but **must dynamically expand or contract repeatable sections** to match the content provided.

### B. Copy Understanding

The user provides full advertorial copy without manually assigning sections. The AI agent must recognize common advertorial copy patterns, such as:

- Headline-style statements
- Hook or follow-up lines
- Long-form narrative or educational text
- Product explanation
- Testimonial-style content
- Call-to-action language
- Legal or compliance language

> This does not need to be perfect or academic. It only needs to be consistent and usable.

---

## 4. Copy Placement Strategy

Using the selected template, the known placeholder locations, and the recognized copy patterns — the agent places copy into the correct placeholders.

The system should aim for:

- Natural reading flow
- Correct hierarchy: **headline → hook → body → product → proof → CTA**
- Clean visual structure

The AI agent is expected to behave like a junior funnel builder who already knows the layout and is simply populating it correctly.

---

## 5. Image Generation & Placement (Critical)

This system is **not text-only**. The AI agent must also:

1. **Detect** where images are required in the template (hero, body, product, testimonial images, etc.)
2. **Understand** what the surrounding copy is about
3. **Generate or fetch** images that match the context:
   - Section about a doctor → generate a doctor image
   - Copy mentions a crying doctor → generate an emotional doctor image
   - Section introduces a product → generate a clean product-focused image
   - Testimonials exist → generate appropriate human portrait images
4. **Call** the relevant image generation or image API
5. **Place** the generated images into the correct image placeholders in the template

**Images must:**

- Fit the layout
- Match the tone of the copy
- Not feel random or generic

---

## 6. Output Requirements

The system must output:

- ✅ Final HTML
- ✅ Final CSS
- ✅ Fully populated with copy + images
- ✅ Ready to deploy without further editing

**Optionally**, the system may also output:

- A short summary of what content was placed where
- Warnings if some copy could not be placed cleanly

---

## 7. What the AI Agent IS Responsible For

- Filling known templates with copy
- Matching copy to the correct placeholder
- **Dynamically adapting repeatable sections** (e.g., reviews, testimonials) to match the number of items in the provided content
- Generating context-appropriate images
- Returning complete page code (HTML + CSS)

---

## 8. What the AI Agent Is NOT Responsible For

- Designing entirely new layouts from scratch
- Making strategic funnel decisions
- Inventing marketing claims

> The templates define the base structure and styling. The agent's job is to populate templates and adapt repeatable sections to fit the content — **execution, not strategy.**

---

## 9. Definition of Success

This AI agent is successful if:

- ✅ Pages can be generated end-to-end automatically
- ✅ Output HTML renders correctly without layout issues
- ✅ Images feel relevant and intentional
- ✅ Manual copy rearranging is rarely needed
- ✅ The system can be used daily for production

---

## 10. One-Sentence Summary

> Build an AI agent that takes our predefined HTML templates, understands the copy and context, automatically fills all placeholders (text + images), dynamically adapts repeatable sections to match the content, and outputs a fully ready landing page.
