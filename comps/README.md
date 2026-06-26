# RegTech / Identity & Financial-Crime Comps — M&A and Growth Equity Precedents

Compiled June 2026. Every figure below is mapped to a verifiable primary or reputable secondary source (company press release / RNS, SEC filing, or tier-1 trade press). **The headline finding: of the 8 M&A deals, only 2 have publicly traceable valuations (Acuant/GBG and Ekata/Mastercard), and only 1 (Acuant/GBG) supports defensible EV/Revenue and EV/EBITDA multiples.** The rest were private-to-private or strategic tuck-ins with undisclosed terms. Nothing in the "EV / Revenue" or "EV / EBITDA" columns has been fabricated — cells read "Not disclosed" where no verified figure exists, and any estimate is explicitly labeled.

Files:
- `MA_transactions.csv` — the 8 M&A rows
- `growth_equity_precedents.csv` — the 4 growth-equity rows

---

## 1. M&A Transactions

| Subsector | Month | Deal Type (Buyer) | Acquirer / Investor | Target | Target Country | EV ($M) | EV / Revenue | EV / EBITDA |
|---|---|---|---|---|---|---|---|---|
| Fraud prevention / financial crime (AML) | Sep-2024 | Strategic | Visa | Featurespace | United Kingdom | **Not disclosed** (est. ~$935m / £700m) | Not disclosed (est. ~11–14x) | Not disclosed |
| AML / financial crime compliance | Feb-2025 | Financial sponsor (PE) | Marlin Equity Partners | Napier AI | United Kingdom | **Not disclosed** | Not disclosed | Not disclosed |
| GRC / integrated risk mgmt software | Apr-2023 | Financial sponsor (PE) | Cinven | Archer (Integrated Risk Mgmt) | United States | **Not disclosed** | Not disclosed | Not disclosed |
| Identity verification (IDV) / KYC-AML | Nov-2021 | Strategic | GBG (GB Group plc) | Acuant | United States | **$736m** | **~12.7x LTM** | **~62x LTM** (derived) |
| Identity verification / digital identity | Apr-2021 | Strategic | Mastercard | Ekata | United States | **$850m** (EV; $861m cash at close) | Not disclosed | Not disclosed |
| KYC / AML / perpetual KYC | Oct-2025 | Strategic | Experian | KYC360 (KYC Global Technologies) | Jersey (Channel Islands) | **Not disclosed** | Not disclosed | Not disclosed |
| Identity verification (IDV) / biometrics | Feb-2024 | Strategic | Entrust | Onfido | United Kingdom | **Not disclosed** (est. ~$400–650m) | Not disclosed (est. ~4.6–5.0x) | Not disclosed |
| Financial crime compliance / intelligent automation | Feb-2026 | Strategic | UiPath | WorkFusion | United States | **Not disclosed** | Not disclosed | Not disclosed |

### Per-deal notes & sources

**1. Featurespace / Visa** — Real-time AI fraud prevention (ARIC Risk Hub). Announced **26 Sep 2024**, completed Dec 2024; Featurespace folded into Visa's Risk & Identity Solutions unit. HQ Cambridge, UK. Terms **officially undisclosed**; Sky News reported ~£700m (≈$935m), a transaction-database record shows ~$950m. Featurespace FY2023 revenue £50.4m (filed accounts via IP Group), ~£63.4m for CY2024 — implies a rough ~11–14x on the estimated price, but this is *derived from an unofficial EV* and should be footnoted, not treated as disclosed. No public EBITDA → EV/EBITDA not calculable.
  - Visa IR: https://investor.visa.com/news/news-details/2024/Visa-to-Acquire-Featurespace/default.aspx
  - Completion: https://investor.visa.com/news/news-details/2024/Visa-Completes-Acquisition-of-Featurespace/default.aspx
  - Price estimate (Sky/Finextra): https://www.finextra.com/newsarticle/44633/visa-in-talks-over-700m-featurespace-acquisition---sky-news
  - Revenue (IP Group): https://www.ipgroupplc.com/our-portfolio/case-studies/featurespace-our-largest-exit-to-date

**2. Napier AI / Marlin Equity Partners** — AI financial-crime compliance (AML/CTF, "Continuum" platform). **Majority growth investment** (not a 100% buyout) announced **3 Feb 2025**. HQ London. Terms **not disclosed** by either party or any trade press; no EV/Revenue/EBITDA exists. (Aggregator-cited FY2023 revenue ~£18.9m is unverified background and pairs with no disclosed EV — do not derive a multiple.)
  - Marlin PR: https://www.marlinequity.com/news/marlin-makes-majority-growth-investment-in-napier-ai/
  - Napier PR: https://www.napier.ai/post/napier-investment-marlin
  - Finextra: https://www.finextra.com/newsarticle/45433/marlin-makes-majority-stake-investment-in-napier-ai

**3. Archer / Cinven** — Governance, Risk & Compliance (GRC) / Integrated Risk Management software (formerly RSA Archer). HQ Overland Park, Kansas. Cinven (PE) acquired Archer from Clearlake Capital + Symphony Technology Group; announced **13 Apr 2023**, closed **10 Jul 2023**. "Financial terms of the transaction were not disclosed" — no credible EV/revenue/EBITDA estimate in the public record.
  - Cinven PR: https://www.cinven.com/news-insights/cinven-agrees-to-acquire-archer/
  - Close (Clearlake): https://clearlake.com/news/clearlake-and-stg-complete-sale-of-archer-to-cinven/

**4. Acuant / GBG** — Identity verification / KYC-AML & identity-fraud prevention. **This is the one fully-traceable deal with multiples**, because acquirer GBG is LSE-AIM-listed and disclosed the deal in an RNS. Announced **18 Nov 2021**, completed ~7 Dec 2021. HQ Los Angeles, US; seller was Audax Private Equity.
  - **EV = $736m** (disclosed, cash-free / debt-free).
  - **EV/Revenue ≈ 12.7x LTM** (Edison Group analysis; implies LTM revenue ≈ $58m). GBG framed it informally as "~12x forward sales."
  - **EV/EBITDA ≈ 62x LTM** — *derived* from RNS-disclosed Acuant Adj. EBITDA (2019 $5.7m → 2020 $10.9m → LTM Jul-2021 **$11.8m**) against the $736m EV. GBG did not headline this multiple; treat as calculated, not company-stated.
  - GBG PR: https://www.gbg.com/en/news/gbg-announces-it-has-agreed-to-acquire-acuant/
  - GBG RNS (Proposed Acquisition & Placing): https://www.investegate.co.uk/announcement/rns/gb-group--gbg/proposed-acquisition-and-placing/6792183
  - Edison (12.7x LTM EV/sales): https://www.edisongroup.com/research/accelerating-growth-with-acuant-acquisition/30236/
  - SecurityWeek ($736m): https://www.securityweek.com/gbg-acquire-acuant-736-million-deal/

**5. Ekata / Mastercard** — Digital identity verification / fraud (spun out of Whitepages). Announced **19 Apr 2021**, closed Jun 2021; integrated into Mastercard's Cyber & Intelligence unit. HQ Seattle, US.
  - **EV = $850m** (disclosed headline enterprise value); **$861m** cash consideration at close per Mastercard's FY2021 10-K (EV adjusted for cash + net working capital). Do not conflate the two.
  - **EV/Revenue: Not disclosed** — Ekata never published an absolute revenue figure (only +33% YoY growth for 2020). Third-party estimate sites (Growjo/Owler/ZoomInfo) are not verifiable and were deliberately excluded, so no multiple is shown.
  - Mastercard newsroom: https://newsroom.mastercard.com/news/press/2021/april/mastercard-to-acquire-ekata-to-advance-digital-identity-efforts/
  - $850m (TechCrunch): https://techcrunch.com/2021/04/19/mastercard-is-acquiring-identity-verification-company-ekata-for-850m/
  - $861m at close (Mastercard FY2021 10-K, EDGAR CIK 0001141391, accession 000114139122000023)

**6. KYC360 / Experian** — KYC/KYB/AML & perpetual-KYC (Customer Lifecycle Management; brand formerly RiskScreen). Announced **27 Oct 2025**. Legal entity **KYC Global Technologies Limited**, registered in **Jersey** (Channel Islands), London office. To be integrated into Experian's Ascend platform. Terms **not disclosed** (typical for an Experian tuck-in) — no EV/multiples available. *Note: the deal is 2025, not 2024, and HQ is Jersey, not the Isle of Man.*
  - Experian PR: https://www.experianplc.com/newsroom/press-releases/2025/experian-acquires-kyc360-to-boost-fraud-and-financial-crime-solu
  - FinTech Futures: https://www.fintechfutures.com/m-a/experian-buys-kyc360

**7. Onfido / Entrust** — AI/ML identity verification (biometrics + document verification). Exclusive discussions announced **7 Feb 2024** (reported 6 Feb), completed **9 Apr 2024**. HQ London. **"Terms of the acquisition were not disclosed."** Press estimated ~$400–650m (TechCrunch/SiliconANGLE cite ~$650m, unnamed sources). Reported revenue: ~$130m ARR (Sifted, FY to Jan-2023) / "over $140m annual revenue" (Entrust completion release) → implied ~4.6–5.0x *only against the unofficial price* — estimate, not disclosed. No EBITDA (growth-stage, reportedly unprofitable).
  - Entrust completion (BusinessWire, terms not disclosed): https://www.businesswire.com/news/home/20240409800662/en/Entrust-Completes-Acquisition-of-Onfido-Creating-A-New-Era-of-Identity-Centric-Security
  - Price estimate (TechCrunch): https://techcrunch.com/2024/02/06/confirmed-entrust-is-buying-ai-based-id-verification-startup-onfido-sources-say-for-more-than-400m/

**8. WorkFusion / UiPath** — Financial-crime compliance (AML/KYC/sanctions/transaction monitoring) via AI "digital workers." **Full corporate acquisition** (WorkFusion now "a UiPath company"), announced **6 Feb 2026**, closing in UiPath's fiscal Q1 2027. HQ New York. *Important: this is a 2026 acquisition, not a 2021 deal or a partnership.* **"Terms of the acquisition were not disclosed."** Do not use WorkFusion's Sep-2025 $45m funding round as a deal value — that was investor funding, not the purchase price.
  - UiPath newsroom: https://www.uipath.com/newsroom/uipath-acquires-workfusion-strengthening-agentic-solutions-for-financial-services
  - UiPath IR: https://ir.uipath.com/news/detail/425/uipath-acquires-workfusion-strengthening-agentic-solutions-for-financial-services

---

## 2. Growth Equity Precedents

For private growth rounds, "EV ($M)" is reported as **post-money valuation** where disclosed (a standard EV proxy for venture/growth comps — no debt/cash adjustment is public). Amount raised is noted separately.

| Source | Month | Buyer Type | Industry Type | Transaction Type | Acquirer / Investor | Target | Target Country | EV ($M) | EV / Revenue | EV / EBITDA |
|---|---|---|---|---|---|---|---|---|---|---|
| Company PR / GlobeNewswire | Mar-2025 | Growth equity (pension growth fund) | Decision intelligence / financial crime analytics | Series F growth equity | Teachers' Venture Growth | Quantexa | United Kingdom | **$2,600m** (post-money) | ~26x ARR (est.) | Not disclosed |
| Company PR / BusinessWire | Jul-2020 / May-2021 | Growth equity | AML / financial crime data & analytics | Series C growth equity (incl. GS extension) | Ontario Teachers' (TIP) + Goldman Sachs Growth | ComplyAdvantage | United Kingdom | **Not disclosed** ($70m raised) | Not disclosed | Not disclosed |
| Company PR / PR Newswire | Jun-2026 | Growth equity | Financial crime risk intelligence / AML analytics | Growth equity investment | Summit Partners | Quantifind | United States | **Not disclosed** ($200m raised) | Not disclosed | Not disclosed |
| Company PR / PR Newswire | Jan-2022 | Crossover / growth equity | Identity verification (IDV) | Series C growth equity | Tiger Global & Alkeon | Veriff | Estonia | **$1,500m** (post-money) | Not disclosed | Not disclosed |

### Per-company notes & sources

**Quantexa** — Decision intelligence for financial crime (AML/KYC/fraud). HQ London. Row uses the most recent priced round: **Series F, announced 4–5 Mar 2025, $175m raised at a $2,600m post-money valuation**, led by Teachers' Venture Growth. The ~26x is an *estimate* against the company's disclosed $100m+ ARR milestone (Oct 2024) — Quantexa did not pair the round with an official revenue figure, so footnote it. **Alternative rows if a different vintage is preferred:** Series E (Apr 2023, $129m at **$1.8bn**, led by GIC) or Series D (Jul 2021, $153m, led by Warburg Pincus — the cleanest pure growth-equity lead).
  - Series F (GlobeNewswire): https://www.globenewswire.com/news-release/2025/03/05/3037089/0/en/Quantexa-Completes-USD-175-million-Series-F-Investment-Round-led-by-Teachers-Venture-Growth.html
  - Series E (TechCrunch, $1.8bn): https://techcrunch.com/2023/04/03/quantexa-raises-129m-at-a-1-8b-valuation-to-help-navigate-online-fraud-and-customer-data-management/
  - $100m ARR: https://www.quantexa.com/press/quantexa-reaches-centaur-status-surpassing-100-million-arr/

**ComplyAdvantage** — AI-driven AML / financial-crime risk data. HQ London (major NY hub). Largest growth event is the **Series C: $50m (Jul 2020, led by Ontario Teachers' TIP), extended to $70m total with Goldman Sachs Growth (May 2021)**. There is no Series D. **Valuation was never disclosed** — "terms of the transaction were not disclosed." No revenue figure at the time of the round → no defensible multiple.
  - $50m Series C (PR Newswire): https://www.prnewswire.com/news-releases/complyadvantage-closes-us50m-series-c-to-fuel-growth-and-expansion-in-fight-against-financial-crime-301100629.html
  - $70m Goldman extension (BusinessWire): https://www.businesswire.com/news/home/20210519005678/en/ComplyAdvantage-Extends-Series-C-Round-To-%2470-Million-With-New-Goldman-Sachs-Investment

**Quantifind** — AI-native financial-crime risk intelligence / AML analytics ("Graphyte"). HQ Palo Alto, US. Row uses the most recent and largest round: **$200m growth investment led by Summit Partners, announced 26 Jun 2026** (existing investors Citi Ventures, S&P Global, Deloitte, Stephens Group participating). **Post-money valuation not disclosed** — the $200m is investment size, not EV. (Earlier comp: $23m led by DNS Capital, Mar 2023 — also undisclosed valuation.)
  - Summit Partners / PR Newswire: https://www.prnewswire.com/news-releases/quantifind-announces-200-million-growth-investment-led-by-summit-partners-to-advance-ai-native-risk-intelligence-and-governed-agentic-middleware-for-modern-risk-operations-302811745.html
  - Summit news: https://www.summitpartners.com/news/quantifind-announces-200-million-growth-investment-to-advance-ai-native-risk-intelligence

**Veriff** — AI-powered identity verification (IDV). HQ Tallinn, Estonia (NYC office). Row uses the largest/most recent priced round: **Series C, announced 26 Jan 2022, $100m raised at a $1,500m post-money valuation**, co-led by Tiger Global and Alkeon (IVP and Accel participating). **No revenue/ARR disclosed** at the round → EV/Revenue not computable. No subsequent priced round has superseded it. (Prior: Series B, Apr 2021, $69m, led by IVP & Accel — valuation undisclosed.)
  - PR Newswire ($100m / $1.5bn): https://www.prnewswire.com/news-releases/veriff-raises-100m-series-c-at-1-5b-valuation-co-led-by-tiger-global-and-alkeon-301469002.html
  - TechCrunch: https://techcrunch.com/2022/01/26/identity-verification-provider-veriff-raises-100m-series-c-co-led-by-tiger-global-and-alkeon/

---

## Methodology & caveats

- **No fabricated multiples.** Where revenue/EBITDA was not disclosed by a verifiable source, the cell reads "Not disclosed." Estimates (Featurespace, Onfido, Quantexa ARR multiple) are explicitly labeled and derive from press-reported, sourced figures.
- **Disclosed multiples exist for only one M&A deal (Acuant/GBG)** because the acquirer was publicly listed and filed an RNS. Strategic acquirers (Visa, Mastercard, Entrust, Experian, UiPath) and PE buyers (Marlin, Cinven) generally did not disclose terms.
- **Date/HQ corrections vs. the original brief:** KYC360/Experian is **Oct-2025** (not 2024) and Jersey (not Isle of Man); WorkFusion/UiPath is a **Feb-2026 full acquisition** (not a 2021 deal/partnership); Quantifind's lead round is **Summit Partners, Jun-2026**.
- **"EV" for growth rounds = post-money valuation**, a venture-comps proxy, not a strict debt/cash-adjusted enterprise value.
- **Verification note:** the agent egress proxy returned HTTP 403 on direct page fetches for many publisher/PR domains, so figures were corroborated via server-side search across multiple independent renderings of the same primary sources (each cross-checked across ≥2–3 outlets). For audit-grade deck footnotes, open the cited primary URLs directly in a browser to confirm exact wording.
