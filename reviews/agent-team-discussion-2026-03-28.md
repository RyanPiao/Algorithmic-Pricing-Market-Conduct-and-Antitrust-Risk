# Agent Team Discussion: Findings Assessment & Publication Strategy

**Date**: 2026-03-28
**Author**: Richeng Piao (first paper)
**Participants**: Senior Faculty Advisor, Methods Detective, Journal Editor Simulator

---

## CONSENSUS: What All Three Agents Agree On

1. **The null is real but for the wrong reason.** The positive point estimates (0.5-1.9%) are probably not zero — the sign test (7/8 cities positive, p ≈ 0.035) and city-level t-test (p ≈ 0.04) both suggest a small positive effect. But the wild bootstrap (p = 0.15-0.20) cannot confirm this because 8 clusters sharing a common cutoff is fundamentally underpowered.

2. **The paper's contribution is real.** Providing the first large-scale quasi-experimental evidence from a many-seller differentiated-product market is valuable, especially given the DOJ v. RealPage litigation and FTC surveillance pricing investigation. The question earns a seat at the table.

3. **The RDD vs DiD disagreement is the biggest threat.** Opposite signs on both levels and variance means neither design alone is reliable. The true effect is likely bounded between -1.6% and +1.9%, with zero comfortably inside.

4. **The design limitation is structural, not fixable with more analysis.** 8 cities sharing one cutoff date is the fundamental constraint. The triple-difference, sign test, and city-level t-test help, but only staggered rollout across more markets would truly resolve the power problem.

5. **The paper's honesty is a genuine asset.** All three agents noted the unusually transparent reporting of limitations — pre-trends, sign disagreement, bundled treatment, bootstrap p-values. This intellectual honesty earned Major Revisions from referees instead of Rejections.

---

## KEY DEBATE: Is "We Can't Reject Zero" a Contribution?

**Advisor says:** Yes, IF reframed as a bounding argument — "the effect lies between -1.6% and +1.9%, zero is inside, and this is an order of magnitude below oligopoly effects even after ITT/TOT adjustment." That's a contribution. But "we have too few clusters to tell" is a limitation, not a finding.

**Methods Detective says:** The sign test (p ≈ 0.035) and city-level t-test (p ≈ 0.04) actually suggest the effect IS positive. The "null" is an artifact of the conservative bootstrap inference, not of the economics. The paper should present BOTH: the bootstrap says we can't reject zero, but nonparametric tests suggest the effect is probably positive and small.

**Editor Sim says:** Journals care about clean stories. "We can't tell" is hard to publish. "Small but positive, consistent with market structure mediating algorithmic pricing effects" is publishable — at the right journal.

---

## THE METHODS DETECTIVE'S KEY INSIGHT: SIGN TEST

This is the most actionable finding from the discussion:

- 7 of 8 cities show positive effects at ±60d
- Under the null (50/50 chance of positive), P(7+ out of 8 positive) = 9/256 ≈ **3.5%**
- This is a valid nonparametric test that does NOT depend on the number of clusters
- It suggests the effect is probably not zero, even though the parametric bootstrap can't confirm it

**The paper should present this alongside the bootstrap.** It's honest and informative: "The bootstrap cannot reject zero (p = 0.15), but the sign test rejects at 5% (p = 0.035), suggesting a small positive effect that our common-cutoff design lacks the precision to quantify."

---

## PUBLICATION STRATEGY FOR A FIRST PAPER

### Journal Rankings (consensus)

| Journal | Desk-reject risk | Acceptance odds | Reframing needed |
|---|---|---|---|
| **Economics Letters** | Low (25%) | **40-50%** | Radical compression to 8-10 pages |
| **Journal of Urban Economics** | Low-Medium (35%) | **30-40%** | Reframe as city/housing impact |
| **JIE / IJIO** | Medium (40%) | **25-35%** | Keep IO framing, lean into Assad contrast |
| **JEBO** | Medium (40%) | **30-40%** | Elevate tech-skill complementarity |
| **Marketing Science** | High (50%) | 15-25% | Major restructure around host behavior |
| **AEJ: Micro** | Very High (80%) | 10-15% | Would need staggered rollout |
| **RAND** | Very High (90%) | 5-10% | Would need staggered rollout |

### Recommended Two-Track Strategy

**Track 1 (immediate): Submit to Economics Letters**
- Compress to 8-10 pages: one bootstrap table, one event study figure
- Core message: "Algorithm availability → positive but insignificant effects in many-seller market; sign test suggests small positive effect; contrasts with 38% in gasoline duopolies"
- Drop: variance analysis (not robust), heterogeneity analysis (descriptive), policy discussion (too long)
- Timeline: 2-3 weeks to prepare, 2-3 months to decision
- **This gets you published.** A published EL is worth infinitely more than a RAND desk reject.

**Track 2 (parallel): Prepare fuller version for JUE or JIE**
- Add the sign test and city-level t-test as primary nonparametric results
- Add the bounding argument (RDD upper bound, DiD lower bound, zero inside)
- Reframe Assad comparison honestly (ITT vs TOT, gap narrows to 4-5x)
- Keep heterogeneity analysis as descriptive section
- Temper policy language
- Timeline: 2-3 months preparation, submit after EL decision

**Do NOT:**
- Submit to RAND or AEJ:Micro (expected return is negative for a first paper)
- Hold the paper waiting for better data (the policy window is NOW)
- Spend 6+ months on revision purgatory at a top journal

---

## CONCRETE NEXT STEPS (Priority Order)

### Analytical (1-2 weeks)
1. **Add sign test** — compute the exact binomial test on city-level signs. Report alongside bootstrap.
2. **Add city-level t-test** — mean of 8 city estimates, t-test on 8 observations.
3. **Present the bounding argument formally** — RDD upper bound, DiD lower bound, true effect ∈ [-1.6%, +1.9%].
4. **Fix the Assad comparison** — compute Wald-scaled TOT, show gap narrows from "order of magnitude" to ~4-5x.

### Writing (1-2 weeks)
5. **Draft Economics Letters version** — 8-10 pages, stripped to core finding.
6. **Revise full paper** with sign test, bounding argument, tempered framing.

### Submission (immediately after)
7. **Submit EL version** while revising full paper for JUE/JIE.

---

## THE COFFEE TALK (Advisor's Direct Advice)

> "Richeng, you have a paper on a question that matters, at a moment when policymakers are desperate for evidence. The design has a power limitation that is structural — it's not your fault, it's the nature of platform-wide rollouts. Your intellectual honesty is a real asset. The goal right now is not the definitive paper on algorithmic pricing — it's a credible, published paper in a respectable journal before your tenure clock pressure builds. A solid single gets you tenure. Do the sign test, write the EL version, and get it out the door."
