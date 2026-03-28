## Deep Search Report: Algorithmic Pricing, Tacit Collusion, and Platform Markets
**Date**: 2026-03-22
**Scope**: Semantic Scholar (Economics filter, 80+ papers screened), NBER working papers, SSRN, Google Scholar, arXiv. Focused on IO theory of algorithmic collusion, empirical evidence on pricing algorithms, platform market regulation, and antitrust/algorithms.

---

### Literature landscape summary

The algorithmic pricing and collusion literature has exploded since 2020, driven by Calvano et al.'s (2020, AER) seminal Q-learning experiments showing that RL agents learn supracompetitive pricing strategies. As of early 2026, this paper has ~452 citations. The field divides into three distinct streams: (1) theoretical/simulation work on whether algorithms *can* collude, (2) empirical work on whether they *do* collude in real markets, and (3) regulatory/legal responses.

**The theoretical consensus** is nuanced: Q-learning agents reliably produce supra-competitive prices in stylized oligopoly (Calvano et al. 2020; Werner 2026; Bhole & Surana 2025), but more sophisticated DRL algorithms (PPO, DQN) and bandit algorithms generally converge closer to Nash equilibrium (Bichler, Durmann & Oberlechner 2024; Deng, Schiffer & Bichler 2024–2025). Algorithm heterogeneity across firms reduces collusion risk. LLM-based pricing agents represent a new frontier — Fish et al. (2024) show GPT-4 agents collude quickly even without explicit instructions.

**The empirical evidence** is thin but growing. Assad, Clark, Ershov & Xu (2024, JPE) provide the strongest quasi-experimental evidence: algorithmic pricing adoption in German gas stations increased margins by ~28% in duopoly/triopoly markets, but only when all stations adopted. Musolff (2022, EC) shows e-commerce repricing algorithms facilitate Edgeworth-cycle-style tacit coordination. On Airbnb specifically, Piao (2023) uses RDD+PSM to study Smart Pricing effects, and Foroughifar & Mehta (2024) study deployment challenges of Airbnb's pricing tool.

**Regulatory/legal** work is voluminous but mostly qualitative. Key contributions include Hartline, Long & Zhang (2024) proposing auditable algorithmic non-collusion definitions, and Brown & MacKay's "algorithmic coercion" framework (NBER W34070, 2025) showing a fast-pricing algorithm can enforce supra-competitive outcomes even against non-collusive rivals.

**Journals dominating**: AER, JPE, RAND, Science (for the Calvano et al. 2020 policy piece), plus many working papers on arXiv and SSRN. The EC (ACM Conference on Economics and Computation) is a key venue.

---

### Papers by role

#### Foundational works

| # | Authors | Year | Title | Venue | Citations | Role |
|---|---------|------|-------|-------|-----------|------|
| 1 | Calvano, Calzolari, Denicolò & Pastorello | 2020 | Artificial Intelligence, Algorithmic Pricing, and Collusion | AER | 452 | Seminal Q-learning collusion experiment |
| 2 | Calvano, Calzolari, Denicolò, Harrington & Pastorello | 2020 | Protecting Consumers from Collusive Prices Due to AI | Science | 89 | Policy companion to the AER paper |
| 3 | Asker, Fershtman & Pakes | 2022 | Artificial Intelligence, Algorithm Design, and Pricing | NBER/AER P&P | 54 | Framework for AI algorithm design in pricing |
| 4 | Harrington | 2018 | Developing Competition Law for Collusion by Autonomous Agents | — | — | Legal framework for algorithmic collusion |
| 5 | Ezrachi & Stucke | 2016 | Virtual Competition | Book | — | Popularized algorithmic collusion concerns |

#### Best identification designs (empirical)

| # | Authors | Year | Title | Venue | Citations | Design |
|---|---------|------|-------|-------|-----------|--------|
| 1 | Assad, Clark, Ershov & Xu | 2024 | Algorithmic Pricing and Competition: Empirical Evidence from the German Retail Gasoline Market | JPE | 148 | Structural break detection + HQ adoption IV |
| 2 | Musolff | 2022 | Algorithmic Pricing Facilitates Tacit Collusion: Evidence from E-Commerce | EC (ACM) | 34 | RDD on automatic repricing + exogenous repricing strategy variation |
| 3 | Werner | 2026 | Algorithmic and Human Collusion | SSRN | 17 | Lab experiments comparing human vs. algorithm pricing with treatment variation |
| 4 | Piao | 2023 | The New Age of Collusion? An Empirical Study into Airbnb's Pricing Dynamics | Working paper | 0 | RDD + PSM on Airbnb pricing tool rollout |
| 5 | Foroughifar & Mehta | 2024 | The Challenges of Deploying an Algorithmic Pricing Tool: Evidence from Airbnb | SSRN | — | Causal analysis of Airbnb pricing tool deployment |

#### Best simulation/theory designs

| # | Authors | Year | Title | Venue | Citations | Key finding |
|---|---------|------|-------|-------|-----------|------------|
| 1 | Brown & MacKay | 2025 | Algorithmic Coercion with Faster Pricing | NBER W34070 | — | Fast-pricing algorithm + commitment → supra-competitive "coercive equilibrium" |
| 2 | Bichler, Durmann & Oberlechner | 2024 | Online Optimization Algorithms in Repeated Price Competition | arXiv | 6 | Bandit algorithms mostly converge to Nash; collusion overstated |
| 3 | Deng, Schiffer & Bichler | 2024–25 | Algorithmic Collusion in Dynamic Pricing with DRL | Multiple | 7 | DRL less collusive than TQL; PPO least collusive |
| 4 | Cartea, Chang & Penalva | 2025 | Algorithmic Collusion and a Folk Theorem from Learning with Bounded Rationality | Games Econ. Behav. | 2 | Folk theorem result for learning algorithms |
| 5 | Fish et al. | 2024 | Algorithmic Collusion by Large Language Models | arXiv/AEA | — | GPT-4 pricing agents collude without explicit instruction |

#### Key critiques and debates

| # | Authors | Year | Title | Venue | Key argument |
|---|---------|------|-------|-------|-------------|
| 1 | Bichler et al. | 2024 | Online Optimization Algorithms... | arXiv | Collusion risk overstated — most practical algorithms converge to NE |
| 2 | Hartline, Long & Zhang | 2024 | Regulation of Algorithmic Collusion | Symp. CS & Law | Proposes auditable non-collusion definition; statistical test framework |
| 3 | Zhang | 2025 | Too Noisy to Collude? | arXiv | Information quality as policy lever — noise injection disrupts collusion |
| 4 | Sternberg & Normann | 2021 | Hybrid Collusion: Algorithmic Pricing in Human-Computer Lab Markets | SSRN | Human-algorithm interaction: 3-firm markets more collusive with algorithm |

#### Recent working papers (2024–2026)

| # | Authors | Year | Title | Venue |
|---|---------|------|-------|-------|
| 1 | Spann et al. | 2024 | Algorithmic Pricing: Implications for Marketing Strategy and Regulation | NBER W32540 |
| 2 | Brown & MacKay | 2025 | Algorithmic Coercion with Faster Pricing | NBER W34070 |
| 3 | Clark | 2026 | Innis Lecture: Algorithmic Pricing and Competition | Canadian J. Econ. |
| 4 | Calvano, Possnig & Toikka | 2026 | The Algorithmic Advantage: How RL Generates Rich Communication | Working paper |
| 5 | Cao & Hu | 2026 | LLM Collusion | arXiv |
| 6 | Abada & Lambin | 2026 | Unleashing the Predators: Autonomous Predation and Manipulation | J. Retailing |
| 7 | Zhao & Berman | 2025 | Algorithmic Collusion of Pricing and Advertising on E-commerce Platforms | arXiv |

#### Survey articles and handbook chapters

| # | Authors | Year | Title | Venue | Notes |
|---|---------|------|-------|-------|-------|
| 1 | Bichler, Deng, Schiffer | 2025 | Algorithmic Pricing and Algorithmic Collusion | Bus. Inf. Syst. Eng. | **Comprehensive survey** — covers theory, simulation, empirical, regulation |
| 2 | Assad et al. | 2021 | Autonomous Algorithmic Collusion: Economic Research and Policy Implications | Brookings | Multi-author survey of the state of knowledge |
| 3 | Spann et al. | 2024 | Algorithmic Pricing: Implications for Marketing Strategy and Regulation | NBER W32540 | Multi-author review of marketing + regulatory dimensions |

---

### Coverage assessment

- **Well-covered**: Q-learning simulation results; theoretical possibility of algorithmic collusion; German gasoline market empirics; legal/regulatory frameworks; DRL vs. TQL comparison
- **Sparse**: Empirical evidence from *platform* markets (only Musolff 2022 on Amazon, Piao 2023 and Foroughifar & Mehta 2024 on Airbnb); price *variance* / discrimination effects (your paper fills this gap); multicity quasi-experimental designs
- **Missing**: No published study combines fuzzy RDD/IV with ML heterogeneity analysis on a platform pricing algorithm — **this is your paper's unique contribution space**

---

### Recommended reading plan

**Week 1 (surveys + foundational)**:
1. Bichler, Deng & Schiffer (2025) survey — comprehensive landscape
2. Calvano et al. (2020, AER) — re-read with fresh eyes for citation
3. Assad et al. (2024, JPE) — closest empirical precedent

**Week 2 (best design papers)**:
4. Brown & MacKay (2025, NBER W34070) — "coercive equilibrium" framework
5. Musolff (2022) — e-commerce RDD precedent
6. Foroughifar & Mehta (2024) — direct Airbnb evidence

**Week 3 (critiques + new frontier)**:
7. Bichler, Durmann & Oberlechner (2024) — algorithms converge to NE critique
8. Fish et al. (2024) — LLM collusion frontier
9. Hartline, Long & Zhang (2024) — audit/regulation framework

**Week 4 (recent + niche)**:
10. Werner (2026) — human vs. algorithm lab experiments
11. Piao (2023) — closest direct competitor (Airbnb RDD)
12. Zhao & Berman (2025) — pricing + advertising dimensions

---

### Database-specific search strings for follow-up

**Scopus**: `TITLE-ABS-KEY("algorithmic pricing" OR "algorithmic collusion") AND SUBJAREA(ECON) AND PUBYEAR > 2021`

**Web of Science**: `TS=("algorithmic pricing" OR "algorithmic collusion" OR "pricing algorithm") AND WC=(Economics) AND PY=(2022-2026)`

**EconLit**: `SU L13 OR L41 AND KW "algorithmic pricing" OR "algorithmic collusion"`

**SSRN**: `"algorithmic pricing" "collusion" economics 2023-2026`

**Google Scholar**: `"algorithmic pricing" ("tacit collusion" OR "market power" OR "supra-competitive") -"machine learning" survey 2023..2026`
