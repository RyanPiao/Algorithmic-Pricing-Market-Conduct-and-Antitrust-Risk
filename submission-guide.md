# Dual-Track Submission Guide for Richeng

## The Strategy

You submit a **short** version to Economics Letters and a **full** version to JUE or JIE. These are different enough papers that simultaneous submission is ethical — different length, different framing, different contribution claims. But you need to manage the overlap carefully.

---

## Track 1: Economics Letters (submit FIRST — within 2 weeks)

### What EL wants
- 2,000-3,000 words (your draft is ~2,200 — perfect)
- 1-2 tables, 1 figure
- A single focused finding, clearly stated
- No lengthy lit review or policy discussion
- Fast turnaround (typically 6-8 weeks to first decision)

### Your EL story (one sentence)
"Algorithmic pricing effects are positive in all 8 cities (sign test p = 0.004) but imprecisely estimated in magnitude (bootstrap p = 0.15), suggesting market structure mediates algorithmic pricing effects."

### To-do before submitting EL
1. **Review the draft** at `drafts/economics-letters-draft.md` — read it fresh, check flow
2. **Format for EL submission**: EL accepts LaTeX or Word. Convert your .md to LaTeX using pandoc or use the Quarto PDF as a starting point. EL has no strict template but expects standard formatting.
3. **Prepare a cover letter** (3-4 sentences): "Dear Editor, I submit [title] for consideration at Economics Letters. The paper provides the first quasi-experimental evidence on algorithmic pricing in a many-seller platform market, complementing Assad et al.'s (2024, JPE) findings in oligopolistic settings. The main finding — positive point estimates in all 8 cities but imprecise under city-level clustering — is timely given the DOJ v. RealPage litigation and FTC surveillance pricing investigation."
4. **Submit via Elsevier's editorial system** (EVISE or Editorial Manager)

### Timeline
- Week 1: Review draft, format, write cover letter
- Week 2: Submit
- Weeks 8-10: Expect first decision (often desk decision in 2-3 weeks)

---

## Track 2: Journal of Urban Economics (start preparing NOW, submit after EL)

### Why JUE over JIE
- Airbnb + cities = perfect topic fit for JUE
- Urban economists are sympathetic to the cluster problem (they deal with it constantly)
- The city-level heterogeneity analysis plays well at JUE
- JUE accepts longer papers with more nuance

### Your JUE story (different from EL)
"How do platform pricing tools affect short-term rental markets in US cities? We study Airbnb's 2023 pricing tool rollout, finding suggestive evidence of small positive price effects bounded between -0.5% and +1.9%, with heterogeneity across cities consistent with local market conditions."

### How JUE differs from EL
| Element | EL version | JUE version |
|---|---|---|
| Length | 2,200 words | 8,000-10,000 words |
| Variance analysis | Dropped | Included (with caveats) |
| Heterogeneity | Dropped | Section 5 (descriptive) |
| Policy discussion | 2 sentences | Full expanded section (antitrust, DOJ, FTC) |
| DiD specification | Mentioned as robustness | Full section with event study |
| Literature | Assad et al. only | Full 4-strand related work |
| Bounding argument | Brief mention | Formal presentation |
| City heterogeneity | Brief table | Detailed discussion of why cities differ |

### Key additions for JUE that aren't in EL
1. **City-level housing market context** — how does Airbnb pricing interact with rental markets in each city? Different cities have different STR regulations (NYC strict, Austin loose). This matters for JUE readers.
2. **Neighborhood-level variation discussion** — even if you can't run the analysis, discussing how within-city market structure varies is important for JUE.
3. **Longer data section** — JUE readers want to understand Inside Airbnb data deeply.

### Timeline
- Weeks 1-4: Revise full manuscript for JUE framing (reframe intro, expand city discussion, add housing market context)
- Week 5: Submit to JUE
- Months 3-5: Expect first decision

---

## Managing Overlap: What's Ethical

### This is fine
- Submitting a 2,200-word focused letter to EL and a 10,000-word full paper to JUE is standard practice. They are genuinely different papers — different length, scope, contribution claim, and audience.
- Many economists publish a "letter" version and a "full" version of the same project.

### What you MUST do
- **Disclose in the cover letter to JUE** (if EL is still under review): "A shorter version focusing solely on the price-level finding is under review at Economics Letters."
- **If EL accepts first**: Cite it in the JUE paper and explain how the JUE version extends it (variance, heterogeneity, policy, bounding argument).
- **If EL rejects**: No disclosure needed at JUE.

### What you must NOT do
- Submit the same paper to two journals simultaneously (but these are genuinely different papers)
- Submit the full version to JUE AND JIE at the same time — pick one

---

## Week-by-Week Action Plan

| Week | Track 1 (EL) | Track 2 (JUE) |
|---|---|---|
| **1** | Review EL draft, fix any issues | Start reframing intro for JUE audience |
| **2** | Format + cover letter + SUBMIT | Add city housing market context |
| **3** | (Waiting for EL) | Expand city heterogeneity discussion |
| **4** | (Waiting) | Rewrite conclusion for JUE framing |
| **5** | (Waiting) | Format + cover letter + SUBMIT JUE |
| **6-10** | EL decision expected | (Waiting for JUE) |
| **11+** | If rejected: revise for JEBO or JIE | JUE decision expected months 3-5 |

---

## If You Need Help From Me

I can help with any of these in future sessions:
- Format the EL draft as LaTeX/PDF for submission
- Write the cover letters for both journals
- Reframe the full manuscript for JUE (add housing market context, city discussion)
- Convert citations to proper citeproc for auto-bibliography
- Create a presentation (reveal.js slides) for seminar talks
