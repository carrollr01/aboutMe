# Fraud / KYC / AML / Compliance-Tech Classification — Run 2 (375 targets)

Source: `deals2.txt` (375 unique names from the second uploaded `Book3.xlsx`; 383 rows, 8 dupes removed). Same method as run 1: 19 reasoning subagents (batches of ~20), domain-knowledge-first with web search on ambiguous names. Per-name output in **`classified2.csv`**; raw slices in `results2/`. Scope rule identical to run 1 (YES = primary business is anti-financial-crime / KYC / AML / fraud / IDV / fincrime RegTech; MAYBE = adjacent; NO = payments/lending/wealth/insurance/trading/data/proptech/etc.).

## Result: 11 YES · 14 MAYBE · 350 NO

### YES — in-scope (11)

| Company | Subsector | Conf. | What it does |
|---|---|---|---|
| Sis ID | Fraud | High | Wire-transfer/payment fraud prevention & bank-detail verification |
| Clearspeed | Fraud | High | AI voice-based risk assessment for fraud detection |
| Intix | Transaction Monitoring | High | Transaction track-and-trace; detects laundering, fraud, illicit flows |
| Greenlite AI | AML | High | AI agents automating AML/KYC/sanctions/transaction-monitoring reviews |
| Duna | KYC/KYB | High | AI-native business-identity KYB/KYC/AML onboarding & screening |
| Persona | Identity Verification | High | Identity verification & KYC/KYB/AML onboarding infrastructure |
| Demyst | KYC/KYB | High | External-data platform for KYB & onboarding automation |
| Hawk | Transaction Monitoring | High | AML transaction monitoring, payment screening, fraud detection |
| Actico | AML | High | AML transaction monitoring, sanctions, PEP/risk classification, fraud |
| Worth AI | KYC/KYB | High | AI SMB onboarding doing KYB/KYC & fraud detection |
| Quantexa | Financial Crime Analytics | High | Decision intelligence / entity resolution for AML/KYC/fraud |

### MAYBE — adjacent / review (14)

| Company | Leaning | Conf. | Why it's borderline |
|---|---|---|---|
| Dun & Bradstreet | KYC/KYB | Medium | Big KYC/KYB/AML/sanctions line, but core business is commercial data |
| Plaid | Identity/Fraud | Medium | Mainly bank-data connectivity; has IDV & anti-fraud (Signal/Beacon) |
| Taktile | Fraud | Medium | Risk-decisioning across credit + fraud + transaction monitoring |
| Mantl | KYC/KYB | Medium | Account opening/origination; includes onboarding/KYC but core is deposits |
| SteelEye | RegTech (conduct) | Medium | Trade/comms surveillance; market-conduct not AML |
| Global Trading Analytics | RegTech (conduct) | Medium | TCA / best-execution; trade-conduct adjacent |
| Heywood Business Analysts | RegTech (prudential) | Medium | Basel/BA regulatory reporting; prudential not fincrime |
| Norm AI | RegTech | Medium | AI regulatory-compliance agents; broad legal compliance |
| Acin | GRC (op-risk) | High | Operational / non-financial risk RegTech |
| Compyl | GRC (security) | Medium | SOC2/ISO/HIPAA GRC; not fincrime |
| TrustCloud | GRC (security) | Medium | Security GRC (SOC2/ISO27001) |
| Cerby | GRC (identity sec.) | Medium | Enterprise identity security & access governance |
| Nok Nok | Identity (auth) | Medium | FIDO passwordless/biometric authentication; not fincrime-specific |
| SpecterOps | GRC (cyber) | Medium | Cyber attack-path/adversary simulation (BloodHound) |

## Notes
- **Quantexa** appears here and is a clear YES — it's also one of your growth-equity precedents.
- Same boundary calls as run 1: dedicated AML/transaction-monitoring (Hawk, Intix, Actico, Greenlite) and IDV/KYB (Persona, Duna, Demyst, Worth AI) are YES; market-conduct surveillance (SteelEye, GTA) and security/IT GRC (Compyl, TrustCloud, Cerby, Nok Nok, SpecterOps) are MAYBE.
- Lowest-confidence rows to eyeball: **Dun & Bradstreet, Plaid, Mantl, Taktile** — each has a real fincrime/identity component bolted onto a larger non-fincrime core; whether they "count" depends on your definition.
