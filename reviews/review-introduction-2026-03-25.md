## Self-Review Report: introduction.md
**Date**: 2026-03-25
**Overall score**: 56/70

### Scores by lens
| Lens | Score | Key issues |
|------|-------|------------|
| Argument structure | 9/10 | Excellent Head formula execution; one repetition issue |
| Pedagogical clarity | N/A | Journal paper — not applicable |
| Math accuracy | 8/10 | No equations (appropriate for intro); numbers accurate per tables |
| Prose quality | 8/10 | Strong active voice; a few long sentences; minor repetition |
| Citation integrity | 7/10 | Two citations lack `[@citekey]` format; one claim needs source |
| Cross-references | 6/10 | No `@fig-`, `@tbl-` refs (appropriate for intro); section refs are plain text not Quarto cross-refs |
| Voice consistency | 9/10 | Consistent semi-formal academic register throughout |

### Critical issues (must fix)

1. **Repetition of "maximally conducive to coordination" phrase.** Used in paragraph 2 ("settings maximally conducive to coordination") and again almost identically in the first contribution paragraph ("features maximally conducive to coordination"). Same phrase appearing twice in ~1,200 words is noticeable. **Fix**: Vary the second instance — e.g., "settings where coordination conditions are strongest" or "markets structurally prone to coordination."

2. **Assad et al. cited 3 times in findings + contribution.** The paper is mentioned in paragraph 2 (findings preview), paragraph 7 (first contribution strand), and paragraph 9 (closest comparison). The third mention is necessary, but the first two overlap substantially. **Fix**: Trim the Assad reference in paragraph 2 to one clause; let the contribution section carry the detailed comparison.

3. **"0.18 percentage points" vs "0.18%".** Paragraph 4 says "an increase of 0.18 percentage points." But tau = 0.0018 on log prices is a 0.18% increase (semi-elasticity), not 0.18 percentage points. These are the same thing for log outcomes, but the language should be precise: "a 0.18 percent increase" or "0.18 log points." **Fix**: Use "0.18 percent" consistently.

### Important issues (should fix)

1. **No abstract.** The research plan specifies an abstract lead ("We study the rollout of Airbnb's Smart Pricing algorithm..."). The introduction currently starts with the hook. An abstract should precede it or be drafted separately.

2. **Paragraph 5 (variance finding) has a long parenthetical.** "hosts (or the algorithm on their behalf) adjusting prices more responsively to demand fluctuations without systematically raising the average rent" — 19 words in a parenthetical. **Fix**: Make it a separate clause or sentence.

3. **Missing Quarto citekeys.** All citations use author-date text format (e.g., "Calvano et al. (2020)") rather than `[@calvano2020artificial]` format. If compiling via Quarto/pandoc with citeproc, these won't resolve to the bibliography. **Fix**: Convert to `[@citekey]` format or add a note that citekeys will be added at compile time.

4. **"The remainder of the paper proceeds as follows" — throat-clearing.** Cochrane advises against this phrasing. **Fix**: "The paper proceeds as follows." or simply start listing sections.

### Minor issues (nice to fix)

1. Paragraph 1, sentence 3: "In Europe, the Digital Markets Act imposed new obligations..." — the DMA is effective since 2023 and compliance since 2024, but the sentence reads as if it just happened. Consider a time marker.

2. Paragraph 6 (third finding): "Using an unsupervised machine learning proxy for latent adoption propensity constructed from strictly pre-treatment pricing behavior" — 17-word noun phrase before the main verb. Consider splitting.

3. The roadmap (final paragraph) lists Section 5 as "where pricing changes concentrate" but the research plan calls this "Where Do Effects Concentrate?" — minor naming consistency.

### Strengths

1. **Head formula perfectly executed.** Hook (policy context) → Question (does Smart Pricing affect prices?) → Method (sharp ITT, 8 cities, 24.2M obs) → Findings (three numbered results) → Contribution (three strands) → Roadmap. Textbook execution.

2. **Contribution paragraphs are well-structured.** Funnel from broad (algorithmic collusion lit) to narrow (platform pricing) to closest paper (Assad et al.). Each paragraph ends with the gap this paper fills. Generous framing throughout.

3. **Concrete numbers throughout.** "0.0018", "0.23%", "38%", "24.2 million", "22%" — no vague claims. Every empirical statement has a specific magnitude.

4. **Active voice dominates.** Passive voice count: ~3 out of ~35 sentences (~9%), well below the 20% threshold.

5. **The three-finding structure** provides a clear organizing framework that the rest of the paper can follow.

### Quality gate
- [x] Score >= 50/70: Commit-safe (okay to save and continue)
- [ ] Score >= 60/70: Review-ready (okay to share with readers)
- [ ] Score >= 65/70: Near-final (minor polish only)

### Recommended next action
Fix the three critical issues (repetition, Assad overlap, percentage point language), convert citations to `[@citekey]` format, and trim the roadmap throat-clearing. This would bring the score to ~62/70 (review-ready).
