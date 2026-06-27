# Fraud / KYC / AML / Compliance-Tech Classification — 314 deal targets

Source: `deals.txt` (314 unique names, extracted from the uploaded `Book3.xlsx`). Each name was classified by a reasoning subagent (16 batches of ~20), leading with domain knowledge and using web search on ambiguous names. Full per-name output with subsector, confidence and rationale is in **`classified.csv`**; raw per-batch slices are in `results/`.

**Scope rule:** YES = the company's *primary* business is anti-financial-crime — AML, KYC/KYB, sanctions/PEP screening, transaction monitoring, fraud detection, identity verification (IDV), financial-crime risk intelligence, or RegTech compliance built for financial crime. NO = payments, lending, wealth, insurance, trading/capital-markets, market data, proptech, accounting/tax, banking, fund admin, etc. MAYBE = genuinely adjacent (broad GRC, generic "compliance," market-conduct surveillance, fraud-adjacent identity/credit data) — flagged for human review.

## Result: 12 YES · 18 MAYBE · 284 NO

### YES — in-scope financial-crime / KYC / AML / fraud / IDV (12)

| Company | Subsector | Conf. | What it does |
|---|---|---|---|
| RiskFront AI | Financial Crime Analytics | High | Agentic AI for financial-crime compliance; AML & fraud due diligence |
| Cable | RegTech/Compliance | High | Automated financial-crime control testing for banks/fintechs |
| OrboGraph | Fraud | High | AI check-fraud detection & prevention for banks |
| TradingHub | Transaction Monitoring | High | Trade surveillance & market-abuse detection |
| Eventus | Transaction Monitoring | Medium | Trade surveillance spanning AML & transaction monitoring |
| AtData | Fraud | High | Email-identity intelligence for fraud / synthetic-ID detection |
| Passthrough | KYC/KYB | High | Investor onboarding with KYC/AML & sanctions/PEP screening for funds |
| WorkFusion | AML | High | AI agents for AML, sanctions screening, KYC, transaction monitoring |
| Journey Technology Solutions | Identity Verification | High | Biometric identity verification & authentication; anti-fraud |
| Kompliant | KYC/KYB | High | KYB/KYC onboarding, underwriting & transaction monitoring for payments |
| KYC360 | KYC/KYB | High | KYC/AML perpetual-KYC & screening platform |
| Credas Technologies | Identity Verification | High | Digital ID verification w/ eKYC; AML, PEP & sanctions screening |

### MAYBE — adjacent / review these (18)

| Company | Leaning | Conf. | Why it's borderline |
|---|---|---|---|
| SteelEye | RegTech (market-conduct) | Medium | Trade & comms surveillance + reg reporting — conduct, not AML |
| Droit | RegTech (capital markets) | Medium | Pre/post-trade regulatory compliance & reporting; not fincrime-specific |
| Trailight | GRC (conduct/SMCR) | Medium | Conduct-risk & individual-accountability compliance |
| StandardFusion | GRC | Medium | Broad GRC/compliance SaaS; not fincrime-specific |
| AuditComply | GRC | Medium | Enterprise GRC / audit management |
| FairNow | GRC (AI governance) | Medium | AI-governance & compliance; not fincrime |
| TrustArc | GRC (privacy) | Medium | Privacy/data-governance compliance |
| CyberCube | GRC (cyber-risk) | Medium | Cyber-risk analytics for insurance |
| Wirespeed | GRC (cyber) | Medium | Cybersecurity MDR; not fincrime |
| Precept | RegTech | Medium | AI compliance automation across industries; broad |
| Konfir | Identity/Income Verification | Medium | Employment/income verification; fraud-adjacent |
| DataTools | Identity/Data Verification | Medium | Address/data verification (GBG); data quality vs. fincrime IDV |
| Floid | Open finance / verification | Low | Open-finance infra with user verification/risk |
| Planky | Open banking analytics | Low | Behavioural scoring on open-banking data |
| Beam | AML (name collision) | Low | "Beam Solutions" is AML/KYC, but other Beams aren't — verify which |
| RED | Unknown | Low | Non-descriptive; no evidence found |
| Surge | Unknown | Low | Non-descriptive; couldn't confirm focus |
| Asymmetric Information | InsurTech? | Low | Ambiguous; likely insurance/risk data |

## Caveats
- **284 NO** are dominated by payments, lending, wealth/asset management, insurance, trading/market-data, and proptech — the bulk of this M&A universe.
- **Name collisions** (Beam, RED, Surge, Asymmetric Information) are the least reliable rows — confirm the specific entity in the deal before relying on them.
- IDV (identity verification) is counted as YES, consistent with how the M&A comp set treated Onfido/Acuant/Veriff.
- Market-conduct/trade surveillance (SteelEye, Droit, Eventus, TradingHub) is a judgment call: pure trade-surveillance leans "market abuse / conduct" rather than AML. I put dedicated surveillance platforms (TradingHub, Eventus) in YES and the broader RegTech-reporting players (SteelEye, Droit) in MAYBE — adjust to your definition.
