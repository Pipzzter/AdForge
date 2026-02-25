# Call Prep: Med Aboussi - AI Automation Agents

## What You Already Agreed To

- **Price**: $500 for all 5 agents (Med's budget was $400-500, you offered $500)
- **Timeline**: 7-10 days (Med's timeline, you said "doable")
- **Scope**: 5 agents total
- **Agent 5 approach**: Guided research assistant (no scraping), user copy-pastes data, agent structures/analyzes it
- **Your Upwork bid**: $587.50 (this is what shows on the contract side)

**⚠️ Potential conflict**: You said $500 in chat, but your Upwork bid is $587.50. Clarify on the call which number applies. Stick to $500 if Med brings it up since that's what you committed to in writing.

---

## The 5 Agents (What Each One Actually Does)

### Agent 1: Copy & Image Injection Agent
**What it does**: Takes a predefined HTML template + raw advertorial copy → fills placeholders with correct content + generates/places images.

**Key details you need to confirm on the call:**
- How many templates? (They said 5-6)
- Where are templates stored? (Their funnel builder)
- Do they have a placeholder naming convention already?
- Image generation: Which API? (DALL-E, Midjourney API, Flux?) Who pays for image API costs?
- How does "template selection" work? CLI? Web UI? API endpoint?

**Your approach**: Parse HTML template, identify placeholders, use LLM to map copy sections to placeholders, call image generation API for visual slots, output final HTML.

**Complexity**: Medium-high. Image generation + placement is the tricky part.

---

### Agent 2: Translation & Localisation Agent
**What it does**: Takes full HTML → translates all visible text to target language (German first) → localises names, locations, references → outputs identical HTML structure with translated text.

**Key details you need to confirm on the call:**
- Primary language: German. Any others planned?
- Do they want a review step before publishing, or fully automatic?
- How many pages per day do they expect to translate?
- Token cost concern: Long landing pages = lots of tokens. Are they OK with per-page cost?

**Your approach**: Parse HTML, extract text nodes only, translate with LLM (preserving HTML structure), apply localisation rules (name swaps, location swaps), validate output HTML structure matches input.

**Complexity**: Medium. The HTML preservation is the main challenge.

---

### Agent 3: Policy & Compliance Agent
**What it does**: Takes full HTML + policy violation instructions → scans all copy → fixes ONLY violating sections → outputs compliant HTML + change log.

**Key details you need to confirm on the call:**
- Where do policy instructions come from? (Ad platform rejection emails?)
- Do they have a standard set of policy rules, or is it per-case?
- Do they want a "review before apply" mode, or auto-apply?
- Change log format: Markdown? JSON? CSV?

**Your approach**: Parse HTML, extract text, run LLM with policy rules to identify violations, apply targeted edits at phrase/sentence level, generate before/after change log.

**Complexity**: Medium. The "surgical edit" requirement (don't over-edit) needs good prompting.

---

### Agent 4: Funnel Optimization Agent (CRO)
**What it does**: Takes existing HTML page → analyzes for missing conversion elements (trust, authority, proof) → adds 1-3 enhancements → outputs improved HTML + summary.

**Key details you need to confirm on the call:**
- The "conversion playbook" — do they have this written down already, or do you need to build it?
- Image generation again: Same question as Agent 1 about APIs and costs
- How do they measure success? A/B testing?
- "Reuse CSS classes already in the page" — this means the agent needs to understand existing page styles

**Your approach**: Parse HTML, analyze sections with LLM against the conversion playbook checklist, identify gaps, generate new HTML blocks that match existing CSS, insert at logical positions, generate summary.

**Complexity**: High. This is the hardest agent. Understanding existing CSS, generating blocks that visually match, and placing them correctly is non-trivial.

---

### Agent 5: Product Research Agent
**What it does**: Helps discover winning products from Facebook Ad Library / spy tools.

**What you proposed (different from their spec)**: Instead of automated scraping, a guided assistant. User searches manually, copies raw data, agent structures and analyzes it.

**Key details you need to confirm on the call:**
- Are they OK with the guided approach? (They might push back and want full automation)
- If they insist on scraping: This is a different project entirely. Facebook Ad Library scraping is fragile, breaks constantly, and violates ToS. Be clear about this risk.
- Output format: What do they do with the research? Feed it into Agent 1?

**Your approach**: Build a conversational agent that gives step-by-step instructions (search X keyword on Ad Library, filter by country Y, paste what you see). User pastes raw data, agent structures it into their required format.

**Complexity**: Low-medium (with guided approach). High (if they want scraping).

---

## 🔍 Real-World Example for Each Agent

### Agent 1: Copy & Image Injection — Example

**Scenario**: Med's team found a new product (posture corrector). Copywriter wrote the advertorial. Now they need a landing page.

**What happens today (manual)**:
1. Someone opens their funnel builder
2. Picks a template
3. Manually copies the headline into the headline spot
4. Manually copies the body text into sections
5. Manually finds/creates images for hero, product, testimonials
6. Manually places images
7. Exports HTML
8. Takes 1-2 hours per page

**What happens with Agent 1**:
1. Team member selects template (e.g. "Template 3 - Health Product")
2. Pastes the raw advertorial copy
3. Agent automatically:
   - Maps "DISCOVER THE BREAKTHROUGH..." → headline placeholder
   - Maps "For years, doctors have been..." → hook placeholder
   - Maps the long story → body placeholder
   - Maps "Here's what Sarah, 54, from Munich said..." → testimonial placeholder
   - Maps "Order now and get..." → CTA placeholder
   - Generates a doctor portrait image → places in authority section
   - Generates a product photo → places in product section
   - Generates a customer selfie → places in testimonial section
4. Outputs complete HTML ready to publish
5. Takes 30 seconds

**Your code**: FastAPI endpoint. Input: template_id + raw_copy. BeautifulSoup parses template, finds placeholders. LLM splits copy into sections and maps to placeholders. Image API generates images based on copy context. Output: final HTML file.

---

### Agent 2: Translation — Example

**Scenario**: Med has a working English landing page for a foot pain product. They want to launch it in Germany.

**What happens today (manual)**:
1. Someone copies all the text from the page
2. Translates it (Google Translate or a translator)
3. Manually replaces all text in the HTML
4. Changes "John M., Ohio" to "Thomas K., München"
5. Changes "American Podiatry Association" to something German
6. Proofreads the whole thing
7. Takes 2-3 hours per page

**What happens with Agent 2**:
1. Team member pastes the full HTML
2. Selects target language: German
3. Agent automatically:
   - Extracts all text nodes from HTML (leaves tags, classes, CSS untouched)
   - Translates everything naturally (not Google Translate quality)
   - "John M., Ohio" → "Thomas K., München"
   - "US doctors recommend..." → "Deutsche Ärzte empfehlen..."
   - "Free shipping across America" → "Kostenloser Versand in ganz Deutschland"
   - Proofreads for awkward phrasing
   - Reinserts translated text into exact same HTML positions
4. Outputs identical HTML structure, all text in German
5. Takes 15 seconds

**Your code**: FastAPI endpoint. Input: HTML string + target_language. BeautifulSoup extracts text nodes with their XPaths. LLM translates batch of text nodes + applies localisation rules. Reinsert into original HTML. Validate HTML structure matches original (same number of tags, same structure).

---

### Agent 3: Policy Compliance — Example

**Scenario**: Med's team ran a landing page for a joint pain supplement. Facebook rejected it with: "Ad contains claims about curing or treating medical conditions."

**What happens today (manual)**:
1. Someone reads the rejection reason
2. Opens the HTML
3. Manually scans every paragraph looking for medical claims
4. Finds: "This supplement CURES joint pain in 14 days"
5. Changes to: "Users reported improved joint comfort within 14 days"
6. Finds: "Clinically proven to eliminate arthritis"
7. Changes to: "Formulated with ingredients studied for joint support"
8. Misses a claim hidden in the testimonials section
9. Resubmits, gets rejected AGAIN
10. Takes 1-2 hours, multiple rounds

**What happens with Agent 3**:
1. Team member pastes the full HTML
2. Pastes the policy instructions: "Remove medical cure claims, avoid guaranteed results, remove before/after implications"
3. Agent automatically:
   - Scans EVERY text node in the entire HTML
   - Finds: "CURES joint pain in 14 days" → flags as cure claim
   - Replaces: "Users reported improved joint comfort within 14 days"
   - Finds: "Clinically proven to eliminate arthritis" → flags as medical claim
   - Replaces: "Formulated with clinically studied ingredients for joint support"
   - Finds in testimonials: "My arthritis is GONE" → flags as cure claim in testimonial
   - Replaces: "My joints feel so much better now"
   - Leaves all compliant copy UNTOUCHED
   - Generates change log:
     ```
     Line 47: "CURES joint pain" → "improved joint comfort" (Reason: cure claim)
     Line 112: "eliminate arthritis" → "joint support" (Reason: medical claim)
     Line 198: "arthritis is GONE" → "joints feel better" (Reason: cure claim in testimonial)
     ```
4. Outputs compliant HTML + change log
5. Takes 10 seconds, catches everything on first pass

**Your code**: FastAPI endpoint. Input: HTML string + policy_rules (list of strings). Extract all text nodes. LLM scans each section against policy rules, returns violations with replacements. Apply replacements surgically. Generate before/after change log. Output: modified HTML + change log JSON.

---

### Agent 4: Funnel Optimization (CRO) — Example

**Scenario**: Med has a landing page for an anti-aging cream. The page has a headline, product description, one CTA, and a footer. It converts at 1.2%. He wants to improve it.

**What happens today (manual)**:
1. CRO expert reviews the page
2. Says: "No social proof, no testimonials, no trust signals, no expert authority, CTA has no urgency"
3. Designer creates a testimonial block with customer photos
4. Designer creates a "Dr. Schmidt recommends" section with a doctor photo
5. Designer adds a "30-day money back guarantee" badge near the CTA
6. Someone codes these into the HTML matching existing styles
7. Takes 4-6 hours of expert + designer time

**What happens with Agent 4**:
1. Team member pastes the existing HTML
2. Optionally adds: product type = "anti-aging cream", market = "Germany", traffic source = "Facebook"
3. Agent automatically:
   - Analyzes the page against the conversion playbook checklist
   - Finds: ❌ No social proof anywhere
   - Finds: ❌ No authority/expert presence
   - Finds: ❌ No reassurance near CTA
   - Finds: ✅ Product description is clear (leave alone)
   - Finds: ✅ Headline is strong (leave alone)
   - Decides to add 3 enhancements (max, to avoid clutter):
     1. Testimonial block with 3 short reviews → inserts below product section
     2. Expert endorsement section → inserts above CTA
     3. Guarantee badge → inserts next to CTA button
   - Reuses existing CSS classes from the page for consistent styling
   - Generates customer portrait images for testimonials
   - Generates doctor portrait for expert section
4. Outputs improved HTML + summary:
   - "Added testimonial block below product section (trust)"
   - "Added expert endorsement above CTA (authority)"
   - "Added guarantee badge next to CTA (reassurance)"
5. Takes 20 seconds

**Your code**: FastAPI endpoint. Input: HTML string + optional context (product type, market, traffic source). LLM analyzes page against conversion playbook checklist. LLM identifies top 3 missing elements. LLM generates HTML blocks using existing CSS classes from the page. Insert blocks at logical positions. Image API generates contextual images. Output: enhanced HTML + optimization summary.

**Why this is the hardest agent**: The LLM needs to understand the existing page's CSS well enough to generate blocks that look like they belong. This is where prompt engineering and iteration will eat most of your time.

---

### Agent 5: Product Research (Guided) — Example

**Scenario**: Med wants to find new health products trending in the German market for native ads.

**What happens today (manual)**:
1. Someone opens Facebook Ad Library
2. Searches "Schmerzlinderung" (pain relief) in Germany
3. Scrolls through hundreds of ads
4. Opens promising ones, checks the advertiser, checks how many ad variants they run
5. Visits the landing page, evaluates the product
6. Takes notes in a spreadsheet
7. Repeats for 10+ keywords
8. Takes 3-4 hours per research session

**What happens with Agent 5 (guided approach)**:
1. Team member opens the agent
2. Agent asks: "What keywords should I research?" → User types: "pain relief, posture, sleep, foot pain"
3. Agent asks: "What markets?" → User types: "Germany, USA"
4. Agent says: "Go to Facebook Ad Library. Search 'pain relief' in Germany. Filter by active ads. Scroll down and copy the first 20 results. Paste them here."
5. User copies and pastes the raw text/data
6. Agent structures it automatically:
   ```
   Product: BackRelief Pro 3000
   Category: Health Device / Posture
   Market: Germany
   Advertiser: HealthTech GmbH
   Ad variations: 12 (high activity)
   Landing page: backrelief-pro.de/offer
   Angles observed: "Doctor recommended", "30-day guarantee", "Before/after"
   Competition: Medium (3 other advertisers for similar product)
   Risk: Low (no medical cure claims)
   Verdict: Worth testing
   ```
7. Repeats for each keyword/market combo
8. Takes 30 minutes instead of 3-4 hours (user does 5 min of copy-paste, agent does 25 min of analysis)

**Your code**: FastAPI endpoint or simple CLI chat. Conversational loop: agent gives instructions → user pastes data → LLM parses raw text into structured format → applies evaluation criteria → outputs structured research report (JSON or Markdown).

---

## ⚠️ Critical Questions for the Call

### Must-Ask (Deal Breakers)
1. **HTML placeholder format — need to see an actual file:**
   - Med already confirmed: templates have explicit placeholders, fixed layouts, maintained in their funnel builder. This is good news (clean structure, not guesswork).
   - **What you still need to know**: "Can you send me one template so I can see the actual placeholder format?" Is it `<!-- HEADLINE -->`, `{{headline}}`, `data-placeholder="headline"`, or literal text like "Headline goes here" inside a div?
   - **Also ask**: What funnel builder do they use? (ClickFunnels, GoHighLevel, Unbounce, custom?) This tells you how clean or messy the exported HTML will be around the placeholders.
   - **Why this matters**: The placeholder format determines how your parser works. If it's clean markers, parsing is trivial. If the "placeholder" is just raw text inside deeply nested funnel-builder divs with inline styles, it's messier.
   - **Bottom line**: Ask Med to send one sample HTML template before you start coding. This is the single most important thing to get from the call.
2. **Image generation**: Who pays for API costs? (DALL-E, Flux, etc.) This is NOT included in $500 — or is it? Or do they have their own image library the agents pull from?
3. **How do they use these agents?** CLI commands? Web interface? API endpoints? This determines how much UI work is needed.
4. **One agent at a time or all 5 simultaneously?** Can you deliver sequentially (Agent 1 first, then 2, etc.)?
5. **Are the templates and playbooks ready?** Or do you need to build those too?
6. **Revisions**: How many rounds of revisions per agent?

### Good to Ask
6. **Priority order**: Which agent do they need first?
7. **Who tests the agents?** Med's team? Do they need documentation/instructions?
8. **Long-term collaboration**: What comes after these 5? (Shows you're thinking ahead)

---

## ⚠️ What If Templates Don't Exist Yet?

Med's spec says "we will maintain 5-6 predefined templates internally" — but "will" is future tense. They might not exist yet.

**Impact per agent if there are NO templates:**

| Agent | Needs Templates? | Blocked? |
|-------|-------------------|----------|
| 1. Copy & Image Injection | YES — entire agent is "fill templates" | ❌ BLOCKED |
| 2. Translation | NO — works on any HTML page | ✅ Can start |
| 3. Policy Compliance | NO — works on any HTML page | ✅ Can start |
| 4. Funnel Optimization | NO — works on any HTML page | ✅ Can start |
| 5. Product Research | NO — no HTML involved | ✅ Can start |

**If Med says templates aren't ready:**
> "No problem. I'll start with Translation, Policy, CRO, and Research. Those work on any existing page. When your templates are ready, I'll plug in Agent 1. Can you give me a rough timeline for when they'll be done?"

**If Med expects YOU to build templates:**
> "Building HTML templates is front-end design work, that's a separate scope from the AI agents. I can build the agents that fill them, but the templates themselves would need a designer or a separate agreement."

**Do NOT agree to build templates for $500.** That's web design on top of 5 AI agents. The $500 is already tight for the agent work alone.

---

## ⚠️ Pricing Reality Check

### Without Copilot (Manual Estimate)

| Agent | Estimated Hours | At $50/hr |
|-------|----------------|-----------|
| 1. Copy & Image Injection | 12-15 hrs | $600-750 |
| 2. Translation | 8-10 hrs | $400-500 |
| 3. Policy Compliance | 8-10 hrs | $400-500 |
| 4. Funnel Optimization (CRO) | 15-20 hrs | $750-1,000 |
| 5. Product Research (guided) | 6-8 hrs | $300-400 |
| **Total** | **49-63 hrs** | **$2,450-3,150** |

### With Copilot (Realistic Estimate)

| Agent | Hours | Notes |
|-------|-------|-------|
| 1. Copy & Image Injection | 6-8 hrs | HTML parsing + LLM mapping is boilerplate, image API is straightforward |
| 2. Translation | 3-4 hrs | Extract text nodes → LLM translate → reinsert. Very standard pattern |
| 3. Policy Compliance | 3-4 hrs | Same pattern as translation, just different LLM instructions |
| 4. Funnel Optimization (CRO) | 8-10 hrs | Hardest one. Prompt engineering for matching existing CSS takes iteration |
| 5. Product Research (guided) | 2-3 hrs | Simple conversational agent loop |
| **Total** | **22-29 hrs** | **$17-23/hr effective rate** |

### What This Means
- With Copilot, the coding is genuinely fast. All agents follow the same core pattern: parse HTML → LLM call → structured output.
- The real time sink is prompt engineering and testing with Med's actual templates, not writing code.
- At 22-29 hours, $500 is still below rate but workable.
- **Long-term play**: Med said "strong potential for long-term collaboration" and "building internal AI infrastructure." Deliver well, get the review, get ongoing work at better rates.

### How to Handle on the Call
- **Do NOT raise the price now.** You committed to $500 in writing. Changing it kills trust.
- **DO scope tightly.** Make sure the $500 covers the initial working versions, not infinite revisions.
- **DO discuss what's NOT included**: Web UI, hosting, API costs, ongoing maintenance
- **DO frame future work**: "These 5 agents are V1. Once you're using them, we can talk about enhancements, new agents, and maintenance."

---

## Call Script (Keep Med Talking)

**Strategy**: Ask open-ended questions. Let Med explain. The more he talks, the more you learn, and the more invested he becomes. Don't rush to solutions. Listen, nod, ask follow-ups.

**Opening (keep it short, then hand him the mic):**
"Hey Med, thanks for making time. I went through all 5 agent specs. Before I get into how I'd build these, I want to make sure I fully understand your world. Can I ask you a few things?"

---

### Phase 1: Their Business (Get Him Talking About Himself)

These questions have nothing to do with the agents yet. They get Med talking about his business, which tells you everything about context, priorities, and how he thinks.

1. "So you're in ecommerce performance marketing. What kind of products do you guys run? Health, beauty, gadgets?"
2. "How big is the marketing team that would be using these agents?"
3. "What does the current workflow look like? Like right now, when you need a new landing page, what happens step by step?"
4. "How many landing pages or funnels are you guys launching per week? Per month?"
5. "What's the bottleneck right now? Is it the copy, the design, the translation, or all of it?"
6. "Are you running ads mostly on Facebook? Google? Native?"
7. "Which markets are you active in? Just Germany, or others too?"

**Follow-up triggers:**
- If he mentions team size → "Who specifically would be using these agents day to day?"
- If he mentions volume → "So if you're doing X pages a month, that's a lot of manual work. Where does most of the time go?"
- If he mentions markets → "Are you planning to expand into more markets? That would affect how we build the translation agent."

---

### Phase 2: Their Current Tools & Setup

This is where you learn what you're actually working with technically. Still asking, not telling.

8. "What funnel builder are you guys using? ClickFunnels, GoHighLevel, something custom?"
9. "When you export a page from there, what does the HTML look like? Is it clean or is it the typical funnel-builder mess with a thousand nested divs?"
10. "You mentioned 5-6 templates in the spec. Are those built already, or still in progress?"
11. "Can you walk me through what a template looks like right now? Like where the placeholders are, how they're marked?"
12. "Where does the advertorial copy come from? Do you guys write it internally, or do copywriters deliver it?"
13. "When the copy comes in, what format is it in? A Google Doc? A Word file? Just pasted text?"

**Follow-up triggers:**
- If he mentions a specific funnel builder → "Have you exported HTML from there before? I want to make sure the agents can parse it cleanly."
- If he says templates are ready → "Can you send me one sample after the call? That's the single most important thing for me to start."
- If he says templates aren't ready → "No problem. When do you think those will be locked in? I can start with the agents that don't need templates first."

---

### Phase 3: The Agents (Go One by One, Let Him Explain Each)

Don't summarize what each agent does. Instead, ask him to explain it to YOU. People love explaining their vision.

**Agent 1 — Copy & Image Injection:**
14. "Walk me through Agent 1 from your perspective. Someone on your team has a template and copy. What do they do? What do they expect to get back?"
15. "The spec mentions image generation. What kind of images are you imagining? AI-generated, stock photos, or do you have your own library?"
16. "For the images, are you currently using any image generation tool? DALL-E, Midjourney, Flux, anything?"
17. "Who decides what images go where? Is that in the template already, or does the agent decide?"

**Agent 2 — Translation:**
18. "For translation, is German the only language right now, or are there others coming?"
19. "The localisation part is interesting. Swapping American names for German names, cities, references. Do you have rules for this already, or should the agent figure it out?"
20. "After translation, does someone review it before publishing, or do you want it to go straight to production?"
21. "How many pages do you typically need translated per week?"

**Agent 3 — Policy Compliance:**
22. "The policy agent is fascinating. Where do the policy rules come from? Ad platform rejections?"
23. "Do you get the same types of violations repeatedly, or is it different every time?"
24. "Do you have a list of common violations I can look at? That would help me build the initial rule set."
25. "When a page gets rejected, what happens now? Someone manually goes through and edits?"

**Agent 4 — Funnel Optimization (CRO):**
26. "The CRO agent has a conversion playbook in the spec. Do you have that playbook written down already, or is it more tribal knowledge in the team?"
27. "When you say 'add a testimonial block' or 'add an expert section', do you have examples of what those should look like?"
28. "How do you measure if the optimization worked? A/B testing? Just gut feeling?"
29. "What does 'over-optimization' look like to you? Where's the line?"

**Agent 5 — Product Research:**
30. "I suggested the guided approach instead of scraping. What's your reaction to that?"
31. "How does product research work right now? Someone manually browses Ad Library?"
32. "How often do you do product research? Daily? Weekly?"
33. "What happens after a product is identified? Does it go straight into a funnel?"

---

### Phase 4: Workflow & Integration

34. "How do you see your team actually using these agents? Is it a command-line thing, or do you need a simple interface?"
35. "Do the agents need to connect to each other? Like, product research feeds into copy injection, which feeds into translation?"
36. "Where should these agents live? Your server? A cloud service? Or just scripts that someone runs?"
37. "Who on your team is the most technical? Who would I coordinate with if you're not available?"

---

### Phase 5: Priorities & Timeline

38. "If you could only have one agent first, which one would it be?"
39. "What's driving the 7-10 day timeline? Is there a launch coming up?"
40. "Would it work for you if I delivered them one at a time? Like Translation first, then Policy, then the rest?"

---

### Phase 6: Close (Only After He's Talked a Lot)

Only move here when the conversation is naturally winding down.

41. "Is there anything in the specs that I haven't asked about that you think is important?"
42. "Any concerns on your end about the approach?"

Then close:
"Alright, I've got a really clear picture now. Let's set up the contract on Upwork and I can start. It takes 2 minutes."

---

### Bonus: Follow-Up Questions (Use Anytime the Conversation Slows)

- "Tell me more about that."
- "How does that work currently?"
- "What's the ideal outcome for you?"
- "What would make this a home run for your team?"
- "What's the worst thing that could happen if we get this wrong?"
- "Have you tried solving this before? What happened?"

---

## ⚠️ Reminders During the Call

- **Contract first.** Do not agree to start working before the Upwork contract is signed.
- **Don't promise "today" or "tomorrow"** for any deliverable. Say "I'll have Agent X ready within 2 days of contract start."
- **If Med asks for more agents or features**: "That's beyond the current scope. We can add that as a follow-up once these 5 are delivered."
- **If Med pushes on scraping for Agent 5**: "Scraping Facebook Ad Library is unreliable and breaks constantly. The guided approach gives you the same data without the maintenance headache. If you want full automation later, that's a separate project."
- **If Med asks about UI/dashboard**: "The $500 covers the core agent logic. If you need a web interface on top of that, we can discuss that as a separate phase."
- **Track what you agree to.** After the call, update the scope.md file immediately.

