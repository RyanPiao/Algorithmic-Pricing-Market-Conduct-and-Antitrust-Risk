# Debate Map: How Do Pricing Algorithms Affect Market Outcomes?

**Project**: Algorithmic Pricing and Market Conduct — Evidence from Airbnb Smart Pricing
**Date**: 2026-03-24

---

## Core Question

When firms adopt algorithmic pricing tools, do market prices rise (collusion/coordination), fall (efficiency), or change in structure (discrimination)?

---

## Position A: Algorithms Facilitate Tacit Collusion

**Proponents**: Calvano et al. (2020, AER); Assad et al. (2024, JPE); Werner (2026); Harrington (2026, JIE); Fish et al. (2024)

**Claim**: Autonomous pricing algorithms learn to sustain supra-competitive prices through implicit reward-punishment strategies, even without explicit communication. This constitutes "tacit collusion by machines."

**Key evidence**:
- Q-learning agents converge to prices 10-30% above Nash in simulation, with punishment strategies lasting 4-8 periods (Calvano et al. 2020)
- German gasoline duopolies: +38% margins when both stations adopt AP; undercutting probability drops to zero; effects emerge after 12 months (Assad et al. 2024)
- Lab experiments: algorithms are more collusive than human subjects in 2-3 player markets (Werner 2026)
- LLM-based pricing agents collude without explicit instruction (Fish et al. 2024)

**Conditions required**: (1) Few sellers, (2) homogeneous products, (3) real-time price transparency, (4) identifiable bilateral rivals, (5) repeated interaction at high frequency.

**Strongest version**: Even with many small firms, a shared algorithm provider creates a hub-and-spoke structure enabling coordination (Harrington 2026).

---

## Position B: Algorithms Enable Price Discrimination, Not Collusion

**Proponents**: Huang (2025); Foroughifar & Mehta (2024); **This paper**; Garcia et al. (2024)

**Claim**: In differentiated-product, many-seller markets, pricing algorithms act as demand-prediction and revenue-management tools. They increase price *variance* (finer time/segment-based discrimination) without raising price *levels*. The primary effect is relaxing cognitive constraints on sophisticated sellers.

**Key evidence**:
- 85% of Airbnb hosts set near-uniform prices; algorithm's welfare-optimal role is setting price *variation* while hosts set *levels* (Huang 2025)
- Only 22% of hosts adopt Smart Pricing; adoption is a skill-complementary choice, not universal (Foroughifar & Mehta 2024)
- Our ITT estimates: pooled tau = 0.0018 (0.18%) on price levels; variance RDD tau = 0.007-0.009 (highly significant) on price dispersion
- Hotel pricing frictions: tool benefit depends on pre-existing strategy quality (Garcia et al. 2024)

**Conditions**: (1) Many sellers, (2) differentiated products, (3) algorithm designed for demand prediction (not competitive reaction), (4) hosts retain price-setting discretion.

**Mechanism**: Technology-skill complementarity (Autor et al. 2003) --- the algorithm complements nonroutine pricing knowledge while substituting for routine demand monitoring.

---

## Position C: Algorithms Coerce Through Speed and Commitment

**Proponents**: Brown & MacKay (2025)

**Claim**: A single firm with a fast, committed pricing algorithm can unilaterally sustain supra-competitive prices by reshaping a rival's within-period payoffs --- without any collusion or communication. Prices can exceed even the fully collusive benchmark.

**Key evidence**:
- Theoretical model: algorithmic firm earns 1.21x collusion profits at maximal speed + commitment; rival earns 0.76x (Brown & MacKay 2025)
- With 10 non-algorithmic rivals, share-weighted average price remains ~18% above Bertrand
- Naive rivals converge to the coercive outcome via simple gradient learning in <15 periods

**Conditions required**: (1) Asymmetric speed advantage (one firm reacts faster), (2) monitoring of a specific identifiable rival, (3) commitment to a persistent pricing rule, (4) oligopoly.

**Distinction from Position A**: Coercion is *unilateral* --- only one firm needs an algorithm. No agreement, communication, or mutual learning required.

---

## Position D: Algorithms Mostly Converge to Nash Equilibrium

**Proponents**: Bichler, Durmann & Oberlechner (2024); Lambin (2024); Deng, Schiffer & Bichler (2024-25)

**Claim**: The collusion result is an artifact of tabular Q-learning's specific learning dynamics. More sophisticated and practically deployed algorithms (bandits, PPO, DQN) generally converge to Nash equilibrium. Supra-competitive prices in Q-learning reflect "learning inertia" (failure to fully exploit deviations), not genuine strategic collusion.

**Key evidence**:
- Bandit algorithms converge closer to Nash than Q-learning (Bichler et al. 2024)
- DRL algorithms (PPO) are least collusive; TQL most collusive (Deng et al. 2024-25)
- Memoryless agents also produce supra-competitive prices, ruling out punishment-based collusion as the mechanism (Lambin 2024)
- Algorithm heterogeneity across firms reduces collusion risk

**Implication**: The "algorithmic collusion" concern may be overstated for real-world pricing software, which typically uses bandits, contextual optimization, or ML prediction --- not tabular Q-learning.

---

## Sources of Disagreement

### 1. Market structure assumptions

| Feature | Positions A & C (prices rise) | Positions B & D (prices flat/Nash) |
|---------|------------------------------|-----------------------------------|
| Number of sellers | 2-3 (oligopoly) | Many (competitive/monopolistic competition) |
| Product type | Homogeneous or near-homogeneous | Highly differentiated |
| Price transparency | Perfect, real-time | Moderate, imperfect comparison |
| Rivalry structure | Identifiable bilateral rivals | Diffuse competition |

The single most important moderator is **market structure**. Positions A and C derive their results in duopoly/tight oligopoly; Position B studies many-seller markets. This is not a genuine disagreement about economic theory --- it is a question of which setting one studies.

### 2. Algorithm design

Positions A and C study algorithms designed for *competitive reaction* (respond to rival price changes). Position B studies algorithms designed for *demand prediction* (forecast demand and set prices accordingly). These are fundamentally different technologies with different equilibrium implications:

- **Competitive-reaction algorithms** (gasoline, e-commerce repricing): detect rival actions and adjust --- creates the speed/monitoring conditions for collusion or coercion
- **Demand-prediction algorithms** (Airbnb Smart Pricing, hotel RM): forecast demand and optimize price schedules --- creates the variance/discrimination effects we observe

### 3. Baseline for comparison

- Position A compares algorithmic outcomes to Nash equilibrium (finding prices above Nash)
- Position D compares different algorithms to each other (finding Q-learning above others)
- Position B compares algorithmic outcomes to the cognitively-constrained status quo (finding discrimination, not price increases)

The choice of baseline determines whether one frames the algorithm's effect as "harmful" (above Nash) or "beneficial" (closer to first-best from a welfare perspective).

### 4. Whether the null on levels is "informative"

- Positions A and C might argue our null simply reflects low adoption (22%) diluting the ITT
- Position B argues the null is structurally predicted: algorithms that set variance but not levels should produce exactly this result
- Resolution: our variance finding distinguishes these --- if the null were pure attenuation, variance should also be null

---

## Resolution and Our Paper's Contribution

Our paper resolves the debate along the market-structure dimension: **algorithmic pricing effects are mediated by market structure**. In tight oligopolies with homogeneous products (Assad et al. 2024), algorithms facilitate coordination. In many-seller differentiated markets (our paper), algorithms enable discrimination. The two findings are not contradictory --- they map the frontier of when and where algorithmic pricing raises concerns.

The variance finding is the key discriminant. If our null on levels were merely an attenuated version of Assad et al.'s positive finding (due to low adoption or market structure), we would also expect null effects on variance. Instead, we find a strong positive effect on variance, indicating that the algorithm *does* change pricing behavior --- but through the discrimination channel, not the coordination channel.

The technology-skill complementarity framework (Position B) unifies the cross-study pattern: algorithms complement the dominant task in each setting. In gasoline (routine competitive monitoring), the algorithm substitutes for human reaction speed, enabling faster punishment. In Airbnb (nonroutine demand assessment), the algorithm complements existing pricing knowledge, enabling finer discrimination.

---

## Visual Summary

```
                        Market Structure
                   Few sellers ◄──────► Many sellers
                   Homogeneous          Differentiated
                        │                     │
                        ▼                     ▼
              ┌─────────────────┐   ┌─────────────────┐
              │  COORDINATION   │   │  DISCRIMINATION  │
              │  Price levels ↑ │   │  Price levels →  │
              │  Variance → / ↓ │   │  Variance ↑      │
              │                 │   │                   │
              │  Assad (2024)   │   │  This paper       │
              │  Brown & MacKay │   │  Huang (2025)     │
              │  Calvano (2020) │   │  Foroughifar &    │
              │  Werner (2026)  │   │  Mehta (2024)     │
              └─────────────────┘   └─────────────────┘
                        │                     │
                        └────────┬────────────┘
                                 │
                        Technology-Skill
                        Complementarity
                        (Autor et al. 2003)
                                 │
                    ┌────────────┴────────────┐
                    │ Routine monitoring:     │
                    │ Algorithm substitutes   │
                    │ → faster punishment     │
                    │ → coordination          │
                    ├─────────────────────────┤
                    │ Nonroutine assessment:  │
                    │ Algorithm complements   │
                    │ → finer discrimination  │
                    │ → variance, not levels  │
                    └─────────────────────────┘
```
