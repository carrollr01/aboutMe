# Durable weekly prompt — paste into a fresh session (repo: carrollr01/aboutMe)

```
Run the weekly FinTech deals scan for the MOST RECENTLY COMPLETED week using the
weekly-fintech-deals skill in this repo (.claude/skills/weekly-fintech-deals/ — read
SKILL.md and description-style.md first; the finalized precedent DB is
weekly-deals/Finalized_Deals_History.xlsx). Work autonomously; state assumptions instead
of asking.

0) WEEK: Sat→Fri, named by its ending Friday (most recent Friday passed). State the window.
   ANNOUNCEMENT date governs — verify every date; exclude prior-week deals even if this
   week's roundups carry them, and completions of earlier-announced deals.

1) SCOPE (locked rules — full detail in SKILL.md):
   - FinTech only (low bar but real: no traditional MGAs/carriers, RIA roll-ups, IT services).
   - Every deal needs a credible source or it's out.
   - Raises tab: equity >= $25M USD; combined simultaneous tranches = one round;
     minority/growth-equity investments go HERE, never in M&A.
   - M&A tab: control deals only, no size floor. Deal Type is STRICTLY "Strategic M&A" or
     "PE Buyout" (zero temperature); snap adjacent structures to the nearest and explain the
     nuance in the description. Exclude: minority stakes, team/book/asset deals, continuation
     vehicles, non-binding proposals.
   - Everything in USD (convert at announcement-date FX).

2) RESEARCH: anchor on the weekly roundups (FinTech Global, FinTech Futures ICYMI,
   InsurTech.ME, DealStreetAsia, Entrackr, Crunchbase, Axios Pro) then sweep all 8 sectors and
   all regions (US, Europe, India, MENA, Africa, SEA, East Asia, LatAm, Canada/ANZ). Crypto
   M&A via The Block/CoinDesk. Public take-privates via SEC/press. Prefer direct web searches;
   keep subagent fan-out modest (spend caps).

3) FINANCIALS: public targets — compute EV/Rev and EV/EBITDA on true EV (net of cash);
   private — compute when disclosed. Record Mults Source + Mults Basis for every computed
   number. Flow metrics (TPV/volume/AUM/GWP/deposits) are never revenue. Undisclosed = "-".
   Negative EBITDA = "n.m.".

4) OUTPUT: build with the skill's build_workbook.py (it enforces the schema):
   Tab "All M&A (PE & Strategic)" and tab "Growth Capital Raises", exact columns per SKILL.md
   (incl. Week auto-derived, and the meta columns Mults Source/Mults Basis/Public Deal/
   HL Deal/Seller — fill what's publicly knowable, "-" otherwise; leave x empty).
   Descriptions per description-style.md: short, product-first, no client-count padding;
   borderline names carry the fintech angle AND the traditional business.
   Name: Weekly_Fintech_Deals_YYYY-MM-DD.xlsx (ending-Friday date), saved to
   weekly-deals/outputs/ (deals JSON to weekly-deals/inputs/).

5) DELIVER: send the file; commit+push. Summary must include counts, headliners, computed
   multiples, borderline calls, AND a list of notable deals you EXCLUDED with the reason
   (out-of-window / non-fintech / not-control / below floor / no credible source).
```
