# Paper Snapshot: Brown and MacKay (2025) — Algorithmic Coercion with Faster Pricing

## Citation

Brown, Zach Y. and Alexander MacKay. 2025. "Algorithmic Coercion with Faster Pricing." NBER Working Paper No. 34070. July 2025, revised January 2026. National Bureau of Economic Research.

- Brown: University of Michigan, Department of Economics
- MacKay: University of Virginia, Department of Economics (note: MacKay moved from Harvard Business School)
- PDF: https://www.nber.org/papers/w34070

---

## Research Question

Can a single firm, by delegating pricing to a fast algorithm with multi-period commitment, unilaterally sustain supracompetitive prices -- even when its rival is myopic, cannot collude, and simply maximizes current-period profits? The paper asks how the *interaction* of pricing speed and rule persistence creates a new channel for higher prices that is distinct from both tacit collusion and standard sequential-move (Stackelberg) leadership.

---

## Theoretical Framework

### Setup
- Duopoly with differentiated products (price competition, strategic complements).
- Firm *a* (the "algorithmic firm") commits to an algorithm that (i) sets an initial price at the start of each period and (ii) can update its price *within* the period after observing firm *b*'s price.
- Firm *b* (the "rival") has no algorithm; it simply maximizes static (current-period) profits each period.

### Two Key Parameters
1. **Speed advantage** (alpha in [0,1]): fraction of the period during which firm *a*'s algorithm can react to firm *b*'s price after observing it. Higher alpha = faster within-period response.
2. **Commitment** (gamma in [0,1]): probability the algorithm persists unchanged into the next period. Combined with the discount factor beta, the "effective commitment" is beta*gamma.

### The "Coercive Equilibrium"
- The algorithmic firm chooses a *target price pair* (p_a, p_b) and programs the algorithm to: (a) play p_a if firm *b* sets the target p_b; (b) *punish* by switching to its static best response R_a(p_b) if firm *b* deviates from the target.
- Because the algorithm reacts *within* the period, any deviation by firm *b* triggers an immediate price cut by firm *a*, making the deviation unprofitable for firm *b* in the *current* period -- not via future punishment.
- Firm *b*'s incentive compatibility constraint (ICC) binds: the profit firm *b* earns at the target must be at least as large as the profit it could earn by deviating and facing the algorithm's within-period punishment.
- The algorithmic firm then picks the most profitable target pair subject to this ICC. Under regularity conditions, this coercive equilibrium exists and is unique (Proposition 1).

### Nesting Benchmarks
- alpha=0, gamma=0: collapses to simultaneous Bertrand-Nash.
- alpha=0, beta*gamma -> 1: Stackelberg leader (firm *a* leads).
- alpha -> 1, gamma=0: Stackelberg follower (firm *a* follows).
- alpha -> 1, beta*gamma -> 1: **Maximal coercion** -- qualitatively different from all benchmarks.

### Speed + Commitment Interaction
The two features are *complementary* (supermodular in equilibrium prices). Speed alone makes firm *a* a follower; commitment alone makes it a leader. Together, the algorithmic firm can both *discipline* its rival through rapid within-period punishment and *discipline itself* through commitment, expanding the feasible payoff set far beyond either benchmark.

---

## Key Results

1. **Prices can exceed collusive levels.** Under maximal coercion (alpha=1, beta*gamma=1) in their linear-demand example (d=1), equilibrium prices are (p_a, p_b) = (1.93, 2.15), with a quantity-weighted average of 2.01 -- above the symmetric collusive price of 2.0. The algorithmic firm prices *below* its rival, capturing a disproportionate demand share. Both prices are 93-115% above the Bertrand level of 1.0.

2. **The algorithmic firm can earn more than full collusion profits.** At maximal coercion, firm *a* earns 1.21 vs. 1.00 under symmetric collusion. Firm *a*'s profits are monotonically increasing in both speed (Prop. 3) and commitment (Prop. 4). Firm *b* earns only 0.76, strictly less than its collusion profit of 1.00 but equal to its Stackelberg-leader profit. Consumer surplus can fall *below* the collusive benchmark (Remark 3, Figure 6).

3. **Even moderate speed/commitment yields substantial price increases.** With alpha = 0.5 and full commitment, the algorithmic firm already earns more than its collusion profit (Figure 3b). Prices are monotonically increasing in both alpha and beta*gamma under linear demand (Prop. 6). The complementarity means the marginal effect of speed is larger when commitment is higher, and vice versa.

4. **Coercion is robust.** The mechanism survives: (a) a forward-looking rival (coercive equilibrium remains an equilibrium), (b) alternative punishment rules including price matching (which yields the fully collusive outcome under maximal speed), (c) alternative timing assumptions at reprogramming dates, and (d) N-firm oligopoly -- even with 10 non-algorithmic rivals, the share-weighted average price remains roughly 18% above Bertrand.

5. **Naive rivals converge to the coercive outcome via simple gradient learning.** When firm *b* uses gradient-based price experimentation (no knowledge of the algorithm), a linear pricing rule by firm *a* rotates firm *b*'s perceived residual demand to appear more inelastic, shifting firm *b*'s perceived profit peak upward. Convergence to the coercive target is rapid (typically <15 periods) and robust to demand shocks (Section 5, Prop. 8).

---

## Relevance to Our Paper

### How does coercion relate to our null finding on Airbnb price levels?

Brown and MacKay provide an alternative mechanism -- *coercion*, not collusion -- by which algorithms can raise prices. This is important for our paper because it expands the theoretical landscape: the absence of tacit collusion does not exhaust the channels through which algorithms could affect prices.

### Does Airbnb satisfy the conditions for coercion?

Several conditions are likely *violated* in the Airbnb setting, which may help explain our null finding:

1. **Asymmetric speed advantage over rivals.** The coercion mechanism requires one firm to react *faster* than its rivals within a pricing period. On Airbnb, hosts who adopt algorithmic pricing tools (e.g., PriceLabs, Wheelhouse, Beyond) gain speed relative to manual hosts, but (a) many competing hosts in the same market also use algorithms, creating *symmetric* speed rather than asymmetric advantage, and (b) Airbnb's platform architecture may limit within-period re-pricing (listings are not repriced in real-time in response to a specific rival's move the way Amazon or gasoline pricing works).

2. **Observability and monitoring of a specific rival.** The model requires firm *a*'s algorithm to observe and respond to a specific rival's price. Airbnb listings compete with a diffuse set of substitutes; there is no clear bilateral rivalry amenable to targeted punishment.

3. **Commitment to a persistent rule.** Airbnb pricing tools are easily reconfigured; hosts can override or turn off algorithmic suggestions at any time, weakening the commitment parameter gamma.

4. **Product differentiation and market structure.** Airbnb is a highly differentiated, many-seller market. The N-firm extension shows coercion weakens (though does not vanish) with more rivals. In a market with dozens of competing listings, the coercion channel is substantially diluted.

5. **Platform design.** Brown and MacKay show that a welfare-maximizing platform would set alpha = gamma = 0 (Prop. 9). Airbnb does not grant any seller a proprietary speed advantage; third-party tools are available to all. This is closer to the neutral-platform benchmark.

**Bottom line:** The coercion mechanism requires asymmetric speed, monitoring of a specific rival, and commitment -- conditions that are largely absent on Airbnb's many-seller, differentiated-product marketplace. This is consistent with our null result on price levels and suggests that the Airbnb setting may be precisely the type of environment where algorithmic pricing does *not* generate supracompetitive outcomes, even though the theoretical possibility exists.

---

## Policy Implications

- **Restricting speed can mitigate coercion.** Limiting how quickly sellers can react to rivals' prices (e.g., through API latency, minimum time-between-change rules, or batched price updates) directly reduces alpha and weakens the coercive mechanism.
- **Restricting commitment also helps.** Preventing persistent pricing rules (e.g., requiring periodic re-optimization) reduces effective commitment.
- **Platform neutrality matters.** A platform that weights consumer surplus sufficiently prefers to set (alpha, gamma) = (0, 0). Platforms that disproportionately internalize seller profits (e.g., via vertical integration or higher take rates from algorithmic sellers) have an incentive to enable coercive technologies (Props. 10-11). Policy ensuring equal access to pricing tools and constraining speed/commitment features can increase welfare.
- **Coercion is distinct from collusion for antitrust.** Standard antitrust frameworks focus on coordination/agreement. Coercion requires only *one* firm with a fast, committed algorithm; the rival need not even be aware it faces an algorithm. This raises new challenges for antitrust enforcement -- the harmful outcome arises from unilateral technological choice, not from any agreement.
- **Arms race concern.** If firms invest in ever-faster algorithms to gain a speed advantage, the result may be a socially wasteful "arms race" analogous to high-frequency trading (Budish et al. 2015).

---

## How to Cite in Our Paper

### In Related Work / Literature Review:
"A distinct theoretical channel through which algorithms can raise prices is *coercion* rather than collusion. Brown and MacKay (2025) show that a single firm with a fast pricing algorithm and multi-period commitment can unilaterally sustain supracompetitive prices by reshaping a rival's within-period payoffs, even when the rival is myopic and cannot collude. In their model, prices can exceed fully collusive levels, with the algorithmic firm earning more than symmetric collusion profits. Crucially, this mechanism requires asymmetric speed -- one firm must react substantially faster than a specific identifiable rival -- combined with persistent commitment to a pricing rule."

### In Discussion / Interpretation of Null Results:
"Our null finding on price levels is also consistent with the theoretical predictions of Brown and MacKay (2025), who identify coercion -- not collusion -- as a channel through which algorithms can raise prices. Their mechanism requires a single firm with a decisive speed advantage over identifiable rivals and commitment to a persistent pricing rule. These conditions are unlikely to hold on Airbnb, where many hosts simultaneously access similar third-party pricing tools, competition is diffuse across dozens of differentiated listings, and hosts can freely reconfigure or override algorithmic recommendations. The absence of asymmetric speed, bilateral monitoring, and binding commitment in our setting helps explain why algorithmic pricing adoption does not translate into higher prices."

---

*Snapshot created: 2026-03-22*
*Source: NBER Working Paper 34070, retrieved from https://www.nber.org/papers/w34070*
