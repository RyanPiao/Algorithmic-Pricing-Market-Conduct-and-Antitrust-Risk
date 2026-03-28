# Fact-Check Log: Algorithmic Pricing & Airbnb Smart Pricing Paper
**Date**: 2026-03-22
**Sources**: ChatGPT fact-check (rollout timing), ChatGPT data verification (Inside Airbnb), Gemini platform regulation report

---

## A. Institutional Claims — Smart Pricing

| Claim | Status | Evidence | Action needed |
|-------|--------|----------|---------------|
| Smart Pricing announced Nov 12, 2015 at Airbnb Open (Paris) | **VERIFIED** (secondary) | Time, TechCrunch, Newsweek all report Nov 12, 2015 launch | Use secondary citations; note no Airbnb primary press release found |
| Rollout was progressive/staggered, not simultaneous | **VERIFIED** (secondary) | TechCrunch: "rolled out progressively" — initially to host conference attendees | Cite TechCrunch 2015; frame as "limited rollout" |
| City-specific rollout dates for 8 study cities | **NOT CONFIRMED** | No primary or secondary source enumerates city-by-city dates | **CRITICAL**: Must acknowledge this. Frame rollout dates as estimated from structural breaks in data, not official schedules |
| Smart Pricing is opt-in (host toggles on/off, sets min/max) | **VERIFIED** (primary) | Airbnb Help Center article 1168; Newsweek 2015 interview | Cite Help Center + contemporaneous reporting |
| Smart Pricing adoption rate (% of hosts) | **NOT CONFIRMED** | No public disclosure found | Acknowledge as limitation; use proxy from data patterns |
| Whether opt-in/opt-out status changed over time | **NOT CONFIRMED** | No dated changelog found | Cannot claim it was always opt-in; describe current status |
| Precursor tool "Price Tips" launched June 2015 | **VERIFIED** (primary) | Airbnb Engineering blog post June 4, 2015 (Aerosolve) | Cite as precursor; note potential contamination of treatment timing |

## B. Algorithm Mechanics

| Claim | Status | Evidence | Action needed |
|-------|--------|----------|---------------|
| Signals: demand, seasonality, reviews, location, events, weather | **VERIFIED** (primary) | Engineering blog posts (2015, 2018); Help Center | Cite specific signals with primary sources |
| Model architecture: gradient boosting / wide additive models | **VERIFIED** (primary) | 2015 blog: "hundreds of thousands of interacting parameters"; 2018 blog: forecasting lead-time distributions | Describe in paper; note model may have evolved since |
| Patent evidence for demand prediction | **VERIFIED** (primary) | US20160148237, US10664855B2 | Cite patent for institutional credibility |
| Algorithm maximizes booking probability × price, not host profit | **VERIFIED** (primary) | 2015 engineering post describes optimization objective | Key for platform incentive misalignment discussion |

## C. Antitrust & Regulatory References

| Claim | Status | Evidence | Action needed |
|-------|--------|----------|---------------|
| DOJ v. RealPage filed Aug 23, 2024 (M.D.N.C.) | **VERIFIED** (primary) | DOJ case page, press release, complaint PDF, CourtListener docket | Cite DOJ primary sources |
| DOJ amended complaint Jan 7, 2025 (added landlord defendants) | **VERIFIED** (primary) | Amended complaint PDF | Update paper to reflect amendment |
| DOJ proposed settlement Nov 24, 2025 | **VERIFIED** (primary) | DOJ press release + Federal Register (91 FR 2592, Jan 21, 2026) | Use consent decree terms as regulatory context |
| Settlement terms: no runtime competitor data, 12-month aging, state-level geo limits | **VERIFIED** (primary) | Federal Register filing | Describe terms precisely; contrast with Airbnb's design |
| FTC surveillance pricing study (6(b) orders, July 2024) | **VERIFIED** (primary) | FTC press release July 23, 2024 | Cite for broader regulatory context |
| FTC interim findings Jan 2025 | **VERIFIED** (primary) | FTC press release Jan 17, 2025 | Include in policy discussion |
| FTC/DOJ withdrew 2000 Competitor Collaboration Guidelines (Dec 2024) | **VERIFIED** (primary) | FTC press release; new comment request Feb 2026 | Note regulatory flux |
| EU DMA entered force Nov 1, 2022; applicable May 2, 2023; compliance March 7, 2024 | **VERIFIED** (primary) | EUR-Lex, EC DMA explainer | Use exact dates |
| DMA contains specific "algorithmic pricing" provisions | **NOT CONFIRMED** | No specific DMA article found targeting algorithmic pricing | Do NOT claim DMA directly regulates algo pricing; describe as framework for platform conduct |
| EU Commission proceedings against Airbnb/Booking.com Jan 2026 | **VERIFIED** (primary per Gemini report) | EC enforcement action | Cite; note focus is data-sharing compliance, not pricing directly |
| Ezrachi & Stucke "Virtual Competition" bibliographic details | **NOT CONFIRMED** | Publisher page not retrieved | Verify via WorldCat/Harvard UP before citing |

## D. Data Source (Inside Airbnb)

| Claim | Status | Evidence | Action needed |
|-------|--------|----------|---------------|
| Founded by Murray Cox, Feb 2015 | **VERIFIED** (primary) | insideairbnb.com/about/ | Cite |
| Governance transferred to Housing Justice Data Lab, 2023 | **VERIFIED** (primary) | insideairbnb.com/about/ | Note in data section |
| Still active as of 2026 | **VERIFIED** (primary) | Buenos Aires dataset dated Jan 2026; report planned late March 2026 | Confirm |
| Data cadence: quarterly for last year (free); older via archive request | **VERIFIED** (primary) | insideairbnb.com/get-the-data/ | Describe precisely in methods |
| Calendar data is forward-looking (365 days), not realized transactions | **VERIFIED** (primary) | Data Assumptions page; PLOS ONE 2024 | **CRITICAL**: Must disclose this prominently. Prices are posted, not transacted. |
| Calendar `available` does not distinguish booked from host-blocked | **VERIFIED** (primary) | Data Assumptions page | **CRITICAL**: Affects interpretation of `available` as treatment proxy |
| Listing locations masked by ~150m | **VERIFIED** (primary) | Data Assumptions page | Disclose; affects spatial analysis |
| Known data quality issues (Alsudais 2021) | **VERIFIED** (peer-reviewed) | Decision Support Systems; DOI: 10.1016/j.dss.2020.113453 | Cite limitations |

## E. Key Software Packages

| Package | Status | Version as of March 2026 |
|---------|--------|--------------------------|
| `rdrobust` (Python) | Active | v1.3.0 (Sep 2024) |
| `csa-py` (Callaway-Sant'Anna in Python) | Available | GitHub: jsr-p/csa-py |
| `differences` (Python DiD) | Available | PyPI: differences |
| `ruptures` (structural breaks) | Active | v1.1.10 (Sep 2025) |

---

## Summary: Critical unverified claims that must be addressed

1. **City-specific rollout dates** — No official schedule exists. Must reframe as estimated from data.
2. **Smart Pricing adoption rate** — No public disclosure. Must use proxy identification.
3. **`available` as treatment proxy** — Calendar availability does not measure Smart Pricing adoption AND does not distinguish booked from blocked. This is the core identification concern flagged by Referee 2.
4. **Calendar prices are posted, not transacted** — Must disclose and argue results are robust.
5. **Price Tips launched 5 months before Smart Pricing** — Potential treatment contamination.
