# Vendor Evaluation Matrix

> **Disclaimer**
>
> This document is based on my own professional experience, accumulated notes, and research about learning platforms and HRTech ecosystems. It is not a vendor-specific guide or an official methodology. Criteria, weights, and examples are illustrative and should be adapted to the specific context, scale, and regulatory environment of your organization.
>
> Comments, corrections, and alternative approaches are welcome.

## Why a matrix, and why not a checklist

Most vendor comparisons fail because they use a flat feature checklist where "AI capabilities" and "mobile app" carry the same weight. The result: three vendors score within two points of each other, and nobody can explain why one should win.

A weighted matrix forces the real questions into the open:

- Can the vendor meet your data residency requirements without a custom build?
- What happens to your data if you leave?
- Who is on the hook when the HRIS sync breaks at 2 AM?
- How long does it take to re-author content the platform can't ingest?

The matrix doesn't pick the vendor. It makes the trade-offs visible — and defensible.

## The three-axis evaluation framework

Research on LMS selection identifies three dimensions that determine whether a platform succeeds in a regulated environment:

1. **Weight** — how much each criterion matters for your organization.
2. **Readiness** — whether the vendor can actually deliver, not just demo.
3. **Migration** — what it costs to get from where you are to where you need to be.

Most evaluations stop at "Weight." That is why they fail.

## Evaluation criteria

| # | Criterion | Weight | What it actually means |
|---|-----------|--------|------------------------|
| 1 | **Compliance & data residency** | 20% | GDPR, 152-FZ, SOC 2, ISO 27001, audit trails, data residency options, breach SLAs. |
| 2 | **Technical standards & migration readiness** | 15% | SCORM 1.2, xAPI, cmi5, LTI 1.3. Can the platform ingest what you already have — and what does it cost to rebuild what it can't? |
| 3 | **Integrations** | 15% | HRIS (1C:ZUP, SAP SF), SSO, analytics, external content. How many are included vs. custom? Who maintains them? |
| 4 | **AI & personalization** | 10% | Recommendations, adaptive paths, LLM-based features. Is it live in production or a demo layer? |
| 5 | **Cost & pricing model** | 15% | Per-user pricing, active-user definition, add-ons, renewal terms, 3-year TCO. |
| 6 | **Implementation & partnership** | 10% | Implementation services, named lead, phased onboarding, post-launch support, references for first 6 months. |
| 7 | **UX & adoption** | 10% | Time to first value, mobile experience, accessibility (WCAG 2.2 AA), admin usability. |
| 8 | **Vendor viability & exit** | 5% | Roadmap transparency, release cadence, financial health, export format, data portability, exit clauses. |

**Total: 100%**

Weights are not fixed. In a regulated fintech, compliance (20%) and integrations (15%) usually dominate. In a fast-moving startup, UX and time-to-value might weigh more.

## What each criterion actually looks like

### 1. Compliance & data residency

- **Questions to ask:** Where is data stored? Can we choose the region? How are audit trails preserved? What happens under GDPR erasure requests? Can you provide SOC 2 Type II or ISO 27001 audit reports?
- **Red flags:** "We're GDPR compliant" without specifics. No EU or RU hosting option. Audit logs that can't be exported. Self-attested checklists only.
- **Non-negotiable for fintech:** data residency in the required jurisdiction, immutable audit trail, retention policy support, documented breach SLAs.

### 2. Technical standards & migration readiness

- **Questions to ask:** Which SCORM versions are supported? Is there a native LRS for xAPI? How is LTI 1.3 handled? What about AICC legacy content? What percentage of our content can migrate without re-authoring?
- **Red flags:** "We support SCORM" but no version detail. No xAPI/LRS. LTI integrations that require custom development. No migration cost estimate.
- **Practical test:** ask the vendor to ingest one of your real legacy courses during the pilot. If they can't, that's the answer.

### 3. Integrations

- **Questions to ask:** How many integrations are included in the base license? What's the cost per custom integration? Who maintains the HRIS sync — vendor or us? What's the integration effort in weeks?
- **Red flags:** "Unlimited integrations" without an SLA. Custom integrations billed by the hour with no cap. No existing customer reference with the same HRIS stack.
- **Practical test:** ask for an existing customer reference with your exact HRIS and SSO configuration.

### 4. AI & personalization

- **Questions to ask:** What's actually AI, and what's a rules engine with a marketing label? How are recommendations trained? Is the model vendor-owned or third-party? Can recommendations be audited or explained?
- **Red flags:** "AI-powered" everywhere, with no detail on model, data, or evaluation. No way to audit or explain recommendations. AI demonstrated only on curated content, not in production.
- **Practical test:** ask how the system handles a recommendation that turns out to be wrong.

### 5. Cost & pricing model

- **Questions to ask:** What counts as an active user? How do add-ons price? What are renewal terms? Are there overage fees? What's the 3-year TCO?
- **Red flags:** Pricing that scales faster than headcount. Add-ons that turn out to be core features. Auto-renewal clauses with no exit. Hidden costs for data exports or premium analytics
- **Practical test:** ask for a 3-year cost projection at your scale, in writing, with all line items.

### 6. Implementation & partnership

This is the most underweighted criterion in most evaluations. Research shows that more than half of LMS buyers lack a dedicated training and development team to absorb migration complexity. The vendor's services team is part of the product.

- **Questions to ask:** Who is the named implementation lead? What does a phased onboarding model look like? What happens after launch? Can we talk to two references about their first six months?
- **Red flags:** No named support contact. Implementation handed off to a generic team. References who won't take the call. No post-launch support commitment.
- **Practical test:** ask for the last two post-incident reports and the implementation timeline for a customer your size.

### 7. UX & adoption

- **Questions to ask:** What's the median time to first completed course? Can a new learner find and launch assigned training in under two minutes? Does the admin dashboard allow bulk actions without IT support?
- **Red flags:** A great demo that requires a 30-page admin guide. Mobile as a second-class experience. No accessibility compliance (WCAG 2.2 AA)

### 8. Vendor viability & exit

- **Questions to ask:** What's the release cadence? Can we see roadmap artifacts? Can we export all data? In what format? At what cost? How long after termination is data retained?
- **Red flags:** Roadmap that doesn't align with your strategy. Export only via PDF. Export fees. Data deleted 30 days after termination with no grace period.
- **Practical test:** ask for a sample export before signing.

## Scoring template

Use a 1–5 scale. Weighted score = sum of (score × weight). Document evidence for each score — screenshots, contract excerpts, PoC results

| Criterion | Weight | Vendor A | Vendor B | Vendor C |
|-----------|--------|----------|----------|----------|
| Compliance & data residency | 20% | | | |
| Technical standards & migration readiness | 15% | | | |
| Integrations | 15% | | | |
| AI & personalization | 10% | | | |
| Cost & pricing model | 15% | | | |
| Implementation & partnership | 10% | | | |
| UX & adoption | 10% | | | |
| Vendor viability & exit | 5% | | | |
| **Weighted total** | **100%** | | | |

**A note on scoring:** a 5 is not "great" — it's "no material risk in this area." A 3 is "acceptable, with caveats." A 1 is "this will block the project." Score the risk, not the enthusiasm.

Any score of 1–2 on a deal-breaker criterion eliminates the vendor regardless of total

## The decision rule

The highest weighted score is not automatically the answer. Before committing:

- **Any 1 on compliance is a dealbreaker.** No score elsewhere compensates.
- **Any 1 on integrations means a pilot is mandatory** before signing.
- **A high total score with a weak exit clause is a trap.** You will leave this vendor eventually. Plan for it.
- **Weighted scores produce a shortlist; your non-negotiables break the tie**

## What I'd do differently next time

- **Run the compliance review before the demo.** It filters out 80% of vendors in the first week.
- **Ask for the export format on day one.** If a vendor hesitates, that's the answer.
- **Score the risk, not the feature list.** A vendor that does less but is honest about its limits is worth more than one that promises everything.
- **Weight implementation services as part of the product.** The platform you buy is not the platform you get, the services team determines what actually works in month three.
