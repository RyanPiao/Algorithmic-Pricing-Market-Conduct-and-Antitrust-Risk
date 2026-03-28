# Deep research verification for Inside Airbnb, methodological citations, and software status

## Data source governance and current activity

**Who runs Inside Airbnb (and who “Inside Airbnb” is today).** The project’s “About” page identifies **Murray Cox** as the founder and coordinator of Inside Airbnb. citeturn33view0 The same page describes a governance transition: Inside Airbnb began as a personal project (explicitly dated to **February 2015**) and, in **2023**, stewardship was formalized under a not‑for‑profit called entity["organization","Housing Justice Data Lab","hjdl not-for-profit 2023"], which “continue[s] to steward the Inside Airbnb project.” citeturn33view0

**Is it still active as of 2026?** Two independent signals on the official site support that it is active during 2026:

- The “Get the Data” page lists at least one region with a dataset date in **2026** (e.g., Buenos Aires “25 January, 2026”), which implies data production continued into 2026. citeturn35view0  
- The “About” page states that a major report was “expected late‑March 2026,” which is contemporaneous evidence of ongoing work and publishing plans. citeturn33view0

## Data collection cadence and archive coverage

**What Inside Airbnb publicly commits to (as of March 2026).** The “Get the Data” page states: “**Quarterly data for the last year for each region is available for free download on this page**.” citeturn34view0turn35view0 It also repeatedly labels archived downloads as “generally quarterly data for the last 12 months,” and instructs users to make an archived data request for additional coverage. citeturn34view0turn35view0

This implies that, for the **standard open downloads**, you should treat the publication cadence as **quarterly snapshots**, at least for the “free” window of coverage (last 12 months). citeturn34view0turn24view0

**Does cadence vary by city/region?** Yes, in at least two practical senses:

- **Snapshot dates differ across regions** (each region has its own “as of” date on the download page), so updates are not synchronized globally. citeturn35view0turn34view0  
- Academic work describing the released data notes imperfect temporal regularity: the 2024 open‑access paper in entity["organization","PLOS ONE","journal | plos"] describes InsideAirbnb releases as “snapshots … not continuous streams,” and states that “calendar updates are made available **monthly (or even less frequently in some cities)**,” characterizing coverage as “patchy both temporally and spatially.” citeturn28view0turn29view3

**How to reconcile “quarterly” vs “monthly.”** The most defensible wording (for a paper) is:

- **Public, free downloads (current site policy): quarterly for the last year**. citeturn34view0turn24view0  
- **Observed release/coverage regularity in the research ecosystem:** sometimes treated as “monthly or less,” and not uniformly regular across cities, reflecting capacity constraints. citeturn28view0turn29view3

If your empirical strategy depends on monthly granularity, you should explicitly document whether you are using (a) quarterly snapshots from the download page, or (b) additional archived releases requested separately. citeturn24view0turn34view0turn22view0

## Calendar file contents and the time direction of “prices”

**Does `calendar.csv` contain forward-looking prices or historical realized prices?** Inside Airbnb’s own documentation is explicit that the compiled data includes “the availability calendar for **365 days in the future**.” citeturn25view0 In other words, `calendar.csv` is best interpreted as a **snapshot of the listing’s future-facing booking calendar as displayed at scrape time**, not a ledger of realized transactions.

This interpretation is aligned with academic descriptions of Airbnb calendars: the 2024 entity["organization","PLOS ONE","journal | plos"] article explains that, at time of scraping, each listing’s booking calendar shows planned availability “for the next 365 days,” and that “unavailable” includes both booked days and host-blocked days. citeturn28view3turn29view3

**What is “in” `calendar.csv` in practice?** While Inside Airbnb’s full data dictionary is hosted externally, multiple reproducible users of the Inside Airbnb calendar file document a stable core schema consistent with the semantic definition above:

- A common set of columns includes: `listing_id`, `date`, `available`, `price`, `adjusted_price`, and `minimum_nights` (with other fields sometimes present depending on vintage). citeturn36search15turn36search2  
- At least some instructional material working directly with Inside Airbnb `calendar.csv.gz` also references a `maximum_nights` field among price/calendar variables. citeturn36search5

**Implication for your paper’s language.** It is accurate to describe `calendar.csv` as containing **date‑stamped, forward‑looking nightly prices and availability statuses** (for dates up to ~365 days ahead of the scrape), not historical realized “paid prices.” citeturn25view0turn28view3 If you want historical price dynamics, you generally need **multiple scrape vintages** (panel of snapshots) and then model changes over time; even then, you are observing **posted calendar states**, not confirmed bookings or final paid amounts. citeturn28view3turn22view0

## Methodology evolution and versioning from 2015 to 2026

A single authoritative, year‑by‑year changelog (2015–2026) is not published in one place on the site, but several **documented structural and operational changes** are verifiable:

**Organizational and infrastructure evolution.** The official “About” page documents that the project began in 2015, later formed an advisory board, and in 2023 transitioned stewardship to entity["organization","Housing Justice Data Lab","hjdl not-for-profit 2023"]. citeturn33view0 The same page credits collaborators with “automating the scraping” and “moving the project to the cloud,” which are concrete methodological/infrastructure changes relative to an earlier personal-project phase. citeturn33view0

**Public release policy and archive approach changed (or at least is now explicitly formalized).** Inside Airbnb now draws a clear boundary between “free” and “archived” data: policy language states that the project offers “a reasonable amount of free data (the last 12 months)” and that “all other data will be archived and must be requested.” citeturn24view0 This is tightly consistent with the “Get the Data” page’s emphasis on last‑year quarterly downloads plus archived requests and newer “regional archive files.” citeturn34view0turn24view0

**Methodological sensitivity to platform change.** External evaluation in entity["organization","Decision Support Systems","journal | elsevier"] documents that Inside Airbnb is widely used but historically “not thoroughly verified for accuracy,” and reports data quality issues attributed to “systemic errors in the data collection process,” including issues arising from a “new feature implemented by Airbnb,” with reproducibility problems when comparing different dataset releases. citeturn22view0 This is evidence that both the platform being scraped and the scraping/processing pipeline can introduce discontinuities over time—important for any 2015–2026 longitudinal research design. citeturn22view0turn28view0

**Bottom line for your methods section.** A defensible statement is that the Inside Airbnb project has (a) changed governance and infrastructure between its 2015 origin and 2026 status, and (b) changed/clarified data distribution policy toward quarterly “last‑year” public releases plus archived access, while (c) the underlying scraped platform and collection pipeline changes can affect comparability across vintages. citeturn33view0turn24view0turn22view0turn34view0

## Known limitations and biases documented by Inside Airbnb and the research literature

**Limitations explicitly acknowledged by Inside Airbnb.** The Data Assumptions page provides several important caveats that map directly to common empirical pitfalls:

- **Independence and scope:** the site is not associated with or endorsed by entity["company","Airbnb","short-term rental platform"] (or competitors), and uses publicly displayed information, including the forward 365‑day calendar and reviews. citeturn25view0  
- **Snapshot nature:** listings can be deleted and the dataset is “a snapshot … at a particular time.” citeturn25view0  
- **Calendar ambiguity:** the Airbnb calendar “does not differentiate between a booked night vs an unavailable night,” so unavailability is not a clean occupancy measure. citeturn25view0turn28view3  
- **Geographic masking:** listing locations are anonymized by Airbnb by up to ~150 meters, and listings in the same building may appear scattered. citeturn25view0  
- **Neighbourhood assignment:** neighbourhoods are derived by matching (masked) coordinates to official neighbourhood boundary definitions; Airbnb’s own neighbourhood labels are avoided due to inaccuracy. citeturn25view0

These disclaimers imply systematic measurement error risks in **spatial econometrics** (masked coordinates), **occupancy inference** (booked vs blocked), and **panel comparability** (deleted listings/snapshot structure). citeturn25view0turn28view3

**Bias/uncertainty highlighted in peer‑reviewed work.** The 2024 open‑access study in entity["organization","PLOS ONE","journal | plos"] contrasts InsideAirbnb with other sources and flags: lack of fully shared scraping/development processes in general, InsideAirbnb’s constrained resources leading to “patchy” temporal/spatial coverage, and the fact that “snapshots” can miss bookings/cancellations between collection points—making occupancy estimation assumption‑heavy and potentially biased. citeturn28view0turn28view3turn29view3

The 2021 research note in entity["organization","Decision Support Systems","journal | elsevier"] specifically documents data quality problems (incorrect review linkage) and warns about reproducibility issues when researchers do not specify which Inside Airbnb release/vintage they used. citeturn22view0

**Practical guidance for bias statements in your paper.** Based on the sources above, the most “standard” limitations paragraph for Inside Airbnb usage (2015–2026) typically includes: (a) snapshot and deletion/entry dynamics, (b) masked geolocation, (c) inability to directly observe realized bookings or paid transaction prices, (d) ambiguity in calendar unavailability, and (e) release‑to‑release comparability and potential scraping errors. citeturn25view0turn28view0turn22view0

## Verification of key methodological references

Below are verified bibliographic details (journal, volume/issue, pages, DOI) corresponding to the items you listed.

**Robust RD inference (CCT).**  
Calonico, Sebastian; Cattaneo, Matias D.; Titiunik, Rocio. 2014. “Robust Nonparametric Confidence Intervals for Regression‑Discontinuity Designs.” *Econometrica* **82**(6) (November): 2295–2326. DOI: 10.3982/ECTA11757. citeturn15view0

**RD density / manipulation test reference.**  
Cattaneo, Matias D.; Jansson, Michael; Ma, Xinwei. 2020. “Simple Local Polynomial Density Estimators.” *Journal of the American Statistical Association* **115**(531): 1449–1455. DOI: 10.1080/01621459.2019.1635480. citeturn14view0turn13view0  
(Using the above local polynomial density estimator, the paper develops a discontinuity‑in‑density testing approach as a methodological application, building on McCrary’s manipulation test idea.) citeturn13view0

**Staggered adoption DiD / multiple time periods.**  
Callaway, Brantly; Sant’Anna, Pedro H. C. 2021. “Difference‑in‑Differences with multiple time periods.” *Journal of Econometrics* **225**(2) (December): 200–230. DOI: 10.1016/j.jeconom.2020.12.001. citeturn16view0

**Double/debiased ML.**  
Chernozhukov, Victor; Chetverikov, Denis; Demirer, Mert; Duflo, Esther; Hansen, Christian; Newey, Whitney; Robins, James. 2018. “Double/debiased machine learning for treatment and structural parameters.” *The Econometrics Journal* **21**(1) (1 February): C1–C68. DOI: 10.1111/ectj.12097. citeturn17view0turn10search27

**Algorithmic pricing and collusion.**  
Calvano, Emilio; Calzolari, Giacomo; Denicolò, Vincenzo; Pastorello, Sergio. 2020. “Artificial Intelligence, Algorithmic Pricing, and Collusion.” *American Economic Review* **110**(10) (October): 3267–97. DOI: 10.1257/aer.20190623. citeturn12view0turn11search3

## Software implementations and maintenance status

**CCT/rdrobust‑style RDD bandwidth selection in Python.** The entity["organization","RD Packages","rdpackages.github.io"] project documents that `rdrobust` provides **Python, R, and Stata** implementations for RD estimation and inference, including bandwidth selectors. citeturn18search0turn18search18 The Python codebase includes an `rdbwselect` implementation with documentation stating it implements bandwidth selectors developed in Calonico, Cattaneo, Titiunik and related follow‑on work. citeturn18search5

As of 2026‑03‑22, the entity["organization","PyPI","python package index"] listing for `rdrobust` shows version **1.3.0**, latest release date **Sep 14, 2024**. citeturn18search1turn18search3  
Interpretation: `rdrobust` is the most direct Python package answer to “CCT optimal bandwidth selection for RDD,” with explicit support for bandwidth selection routines consistent with the CCT/RD packages ecosystem. citeturn18search0turn18search5turn15view0

**Python implementation of Callaway & Sant’Anna vs R‑only.** The canonical and most cited implementation remains the R package `did` (official docs reference the 2021 *Journal of Econometrics* paper as the background article). citeturn19search6turn16view0

However, there are now **Python implementations** and ports in the ecosystem:

- A dedicated Python implementation exists as **csa‑py**, explicitly described as “an implementation of the Callaway and Sant’Anna (2021) estimator in Python.” citeturn19search0  
- The `differences` Python project reports an `ATTgt` class that implements procedures “suggested by Callaway and Sant’Anna (2021)” (and related work), and it is distributed via PyPI. citeturn19search9turn19search25  
- A curated resource page by Sant’Anna lists multiple languages and includes a “Python package” link under the Callaway–Sant’Anna framework resources. citeturn19search4

**Status of the `ruptures` Python package.** As of 2026‑03‑22, `ruptures` is clearly active/maintained in the sense of recent releases: PyPI shows `ruptures` **1.1.10** released **Sep 10, 2025**. citeturn21view0 The GitHub releases page corroborates the existence of versioned releases including v1.1.10 dated Sep 10 (2025). citeturn20search1turn20search2

## Source URLs

```text
Inside Airbnb (official)

About Inside Airbnb
- https://insideairbnb.com/about/

Get the Data
- https://insideairbnb.com/get-the-data/

Data Assumptions
- https://insideairbnb.com/data-assumptions/

Data Policies
- https://insideairbnb.com/data-policies/

Academic / peer-reviewed discussions of Inside Airbnb limitations & data quality

Wang et al. (2024), PLOS ONE (open-access via PMC)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10849255/

Alsudais (2021), Decision Support Systems (ScienceDirect landing page)
- https://www.sciencedirect.com/science/article/abs/pii/S0167923620302086
DOI
- https://doi.org/10.1016/j.dss.2020.113453

Methodological references (verified bibliographic details)

Calonico, Cattaneo & Titiunik (2014), Econometrica PDF
- https://rdpackages.github.io/references/Calonico-Cattaneo-Titiunik_2014_ECMA.pdf
DOI
- https://doi.org/10.3982/ECTA11757

Cattaneo, Jansson & Ma (2020), JASA PDF
- https://rdpackages.github.io/references/Cattaneo-Jansson-Ma_2020_JASA.pdf
DOI
- https://doi.org/10.1080/01621459.2019.1635480

Callaway & Sant’Anna (2021), Journal of Econometrics (ScienceDirect landing page)
- https://www.sciencedirect.com/science/article/abs/pii/S0304407620303948
DOI
- https://doi.org/10.1016/j.jeconom.2020.12.001

Chernozhukov et al. (2018), The Econometrics Journal (Oxford Academic landing page)
- https://academic.oup.com/ectj/article-abstract/21/1/C1/5056401
PDF copy used for bibliographic verification
- https://www.math.mcgill.ca/dstephens/SISCER2024/Module15-PropensityScores/Articles/Chernozhukov2018.pdf
DOI
- https://doi.org/10.1111/ectj.12097

Calvano et al. (2020), American Economic Review (AEA landing page)
- https://www.aeaweb.org/articles?id=10.1257%2Faer.20190623
DOI
- https://doi.org/10.1257/aer.20190623

Software

RDROBUST (RD Packages site)
- https://rdpackages.github.io/rdrobust/

rdrobust on PyPI (Python package)
- https://pypi.org/project/rdrobust/

rdrobust bandwidth selection code reference (GitHub)
- https://github.com/rdpackages/rdrobust/blob/master/Python/rdrobust/src/rdrobust/rdbwselect.py

R did package documentation site
- https://bcallaway11.github.io/did/

csa-py (Callaway–Sant’Anna estimator in Python)
- https://github.com/jsr-p/csa-py

differences (Python DiD implementations) – GitHub and PyPI
- https://github.com/bernardodionisi/differences
- https://pypi.org/project/differences/

ruptures – PyPI and GitHub releases
- https://pypi.org/project/ruptures/
- https://github.com/deepcharles/ruptures/releases

Supplementary (calendar.csv columns used in practice)

Example showing common calendar columns (tibble/head output)
- https://chia-kaiyang.github.io/post/test/

Instructional material referencing pricing/calendar columns (incl. maximum_nights)
- https://matteocourthoud.github.io/course/data-science/03_data_wrangling/

Example noting calendar is for upcoming 365 days (Oslo repo summary)
- https://github.com/trulsmoller/airbnb-oslo
```