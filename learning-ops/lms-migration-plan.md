# LMS/LXP Migration Plan

> **Disclaimer**
>
> This document is based on my own professional experience, accumulated notes, and research about learning platforms and HRTech ecosystems. It is not a vendor-specific guide or an official methodology. Frameworks, numbers, and examples are illustrative and should be adapted to the specific context, scale, and regulatory environment of your organization.
>
> Comments, corrections, and alternative approaches are welcome.
> 
## Why migrations fail

Most LMS migrations fail not because of technology, but because of:

- **Underestimating data complexity** — SCORM packages, xAPI statements, completion records, and assessment history are rarely clean. Data migration is consistently cited as the single most common root cause of implementation overruns. Legacy packages with authoring-tool dependencies, incomplete manifests, and mismatched identifiers are the usual culprits.
- **Treaing it as an IT project, not a change management project** — Research on organizational change consistently points to employee resistance and insufficient leadership support as the dominant reasons change programs fail. Users who don't understand why the transition is happening disengage, and once they stop using a platform, they rarely come back.
- **Ignoring compliance until the end** — In regulated industries, learning records are legal evidence. Lost or corrupted completion records constitute a compliance failure, and audit trails that don't map cleanly to the new system create exposure. A gap in reporting continuity during a compliance period can become a measurable breach.
- **No rollback plan** — When integrations break (and they will), there must be a way back. Running legacy and new systems in parallel through unstable integrations causes data latency and creates a "Day 2 crisis" before the first login.
- **Sunk costs in content and customizations** — Organizations often underestimate what it costs to re-author or retire legacy content that cannot be migrated cleanly. Pre-migration audits typically reduce scope significantly — but only if they are done before the vendor is involved.

This plan addresses each of these.

## Technical standards: what we're actually moving

Before planning a migration, it's worth being precise about what is being migrated. Learning content and tracking data come in several formats, each with its own migration risk.

| Standard | What it is | Migration risk |
|----------|-----------|----------------|
| **SCORM 1.2 / 2004** | Legacy content packaging and tracking | High — most older content uses this; interaction data often incomplete |
| **xAPI (Tin Can)** | Statement-based tracking, more granular | Medium — newer content may use this; requires an LRS |
| **cmi5** | Hybrid of SCORM and xAPI | Low — rare but growing; cleaner data model |
| **LTI 1.3** | Tool integration (external apps, tools) | High — breaks if not re-configured or re-registered |
| **AICC** | Very old standard, pre-SCORM | High — often requires re-authoring or retirement |

**What this means in practice:**
- Content that cannot be migrated cleanly must be re-authored or retired. 
- Tracking data (completion, scores, time spent) is only as good as the standard it was recorded in. SCORM data is often partial; xAPI data is richer but may be incomplete if the LRS wasn't configured properly.
- LTI integrations are the most fragile part of any migration. Every external tool must be re-registered, re-tested, and re-approved.

**Action:** Audit all content by standard before selecting a vendor. This is the step that most organizations skip, and it is the one that determines the real scope of the migration.

## Data architecture

Before migrating, it helps to map the core entities and how they relate. Most LMS/LXP platforms share a similar data model, but the details matter — especially when linking learning to HR data.

### Core entities

```
User
├── id (UUID)
├── email
├── employee_id (HRIS link)
├── department
├── role
├── grade
├── manager_id
├── hire_date
└── status (active / terminated)

LearningRecord
├── id
├── user_id
├── content_id
├── content_type (course / assessment / simulation)
├── status (not_started / in_progress / completed / failed)
├── score
├── time_spent_seconds
├── started_at
├── completed_at
└── xapi_statement_id (if applicable)

Assessment
├── id
├── content_id
├── questions[]
├── passing_score
├── attempts_allowed
└── ai_generated (boolean)
```

### Why this matters

- **User is the anchor.** Every learning record must resolve to a real user. If the HRIS link breaks, reporting breaks with it.
- **LearningRecord is the audit trail.** In regulated industries, this is the evidence that someone completed required training. It must be immutable and timestamped.
- **Assessment carries risk.** If an assessment is AI-generated, it needs its own review trail. If it's tied to compliance, it needs a version history.

### Data flow

```
HRIS (1C:ZUP / SAP SuccessFactors)
    │
    ▼
[ETL Layer] ── daily sync ──► LXP User Store

Legacy LMS
    │
    ▼
[Content Migration Tool] ── SCORM/xAPI parser ──► LXP Content Store

LXP (all events)
    │
    ▼
[Analytics Pipeline] ──► Amplitude / Tableau
```

**Key principle:** the HRIS is the source of truth for people. The LXP is the source of truth for learning. When they disagree, the HRIS wins — but the conflict must be logged, not silently resolved.

## API specification (target)

The goal is not to design the final API, but to show what a clean integration contract looks like. These are illustrative examples based on common patterns in learning platforms.

### User sync

```
POST /api/v1/users/sync
Authorization: Bearer <token>
Content-Type: application/json

{
  "users": [
    {
      "employee_id": "12345",
      "email": "user@company.com",
      "department": "Engineering",
      "role": "Backend Developer",
      "grade": "L3",
      "manager_id": "67890",
      "status": "active"
    }
  ]
}
```

**Why it matters:** the HRIS pushes updates daily. If a user is terminated, the LXP must deactivate access — not delete the record. Learning history stays for audit; access goes away.

### Completion webhook

```
POST /webhooks/completion
X-Signature: sha256=<hmac>

{
  "user_id": "uuid",
  "content_id": "uuid",
  "status": "completed",
  "score": 85,
  "time_spent_seconds": 720,
  "completed_at": "2026-09-16T10:30:00Z"
}
```

**Why it matters:** completion events are the audit trail. They must be signed, timestamped, and stored immutably. If a compliance audit asks "did this person complete the training?", this webhook is the answer.

### Assessment submission

```
POST /api/v1/assessments/{id}/submit
{
  "user_id": "uuid",
  "answers": [
    {"question_id": "q1", "answer": "B"},
    {"question_id": "q2", "answer": "A"}
  ]
}
```

**Why it matters:** if the assessment is AI-generated, the submission must record which version of the assessment was served. Otherwise, a score is not defensible in an audit.

## Migration phases (selected)

| Phase | Typical duration | Factors affecting duration | Rollback |
|-------|------------------|----------------------------|----------|
| **Audit** | 4–8 weeks | Data volume, content complexity, number of integrations, stakeholder availability | N/A |
| **Pilot** | 4–6 weeks | Pilot group size, test scenario complexity, feedback cycles | Revert DNS, restore legacy LMS |
| **Parallel run** | 6–12 weeks | Compliance requirements, reporting cycle length, integration stability | Legacy LMS remains primary |
| **Cutover** | 1 week + 2–4 weeks support | Blackout window tolerance, QA resource availability | Switch DNS back |
| **Decommission** | 4–6 weeks | Data retention policy, legal review, archiving process | Restore from backup |

**Key rules:**

- **Never delete legacy data until 90 days after cutover:** If something breaks in month two, you need the old records.
- **Run parallel for at least one full reporting cycle:** If monthly compliance reports exist, you need at least one month of parallel data to validate.
- **Define the rollback trigger before the pilot starts:** "If adoption drops below X% in the first two weeks, we roll back, not "we'll decide if it feels wrong." The threshold is defined by the business, not by the project team.
- **Log every sync conflict:** When HRIS and LXP disagree, the HRIS wins, but the conflict must be visible, not silently resolved. Log who resolved it, when, and on what basis.

### Why this matters in a regulated environment

The rollback plan is what makes the migration defensible to legal, audit, and compliance teams. Without it, you are asking them to trust the process. 

## Compliance for fintech

| Requirement | What it means for migration | How to handle it |
|-------------|----------------------------|------------------|
| **GDPR** | EU personal data must stay in EU, right to erasure, consent tracking | Data residency in EU; erasure API; consent log migration |
| **152-FZ** | RU personal data stored in RU; local DPO sign-off | Data residency in RU; coordinate with legal before any cross-border sync |
| **Audit trail** | Every learning record must be traceable and immutable | Migrate with original timestamps; never overwrite history |
| **Access control** | Role-based access, SSO with MFA, session timeout | Map legacy roles to new RBAC; test SSO before pilot |
| **Data retention** | Compliance records kept for the required period; learning records for a shorter period | Define retention policy per record type before migration |

### What this changes in the migration plan

- **Audit phase** must include a compliance review, not just a data inventory.
- **Pilot** must run with the same access controls as production. A pilot without compliance controls proves nothing.
- **Parallel run** must produce identical reports from both systems. If they differ, you cannot cut over.
- **Decommission** must include legal sign-off that legacy data can be archived or deleted.

### Practical notes

- **Do not migrate data you are not allowed to keep.** If a record has expired under the retention policy, it should not be migrated at all.
- **Log every access to learning records.** In an audit, "who saw this record and when" matters as much as the record itself.
- **Involve legal and the DPO early.** They are not a final approval step — they are a design partner. If they see the plan for the first time at cutover, the project is already at risk.
- **Assume the auditor will ask for everything.** Design the migration so that any record can be traced from the new system back to its source.

## What the budget actually covers

The platform license is the number everyone sees. In my experience, the license is somewhere between a third and half of the real cost (the rest sits in everything around it).

**The platform**

- **License:** per user, per year. The definition of "active user" matters: is it someone who logs in once, or someone who completes a course? This single definition can change the annual cost by 30–40%.
- **Add-ons:** AI recommendations, advanced analytics, mobile access. Ask what is included in the base license and what is a separate module.
- **Tiered pricing:** volume discounts are common, but the thresholds vary. Ask what scale actually costs: at 10,000 users, at 50,000, at 90,000.

**The migration itself**

- **Data extraction and transformation:** pulling user records, completion history, and assessment results from the legacy system, cleaning them, and mapping them to the new data model. The cost depends entirely on how messy the source data is.
- **Content re-authoring or retirement:** not all SCORM content migrates cleanly. Some courses need to be rebuilt; others should be retired. This is a content project, not an IT task, and it is almost always underestimated.
- **Integration development:** every HRIS, SSO provider, analytics tool, and external content source is a separate integration. Each one needs to be built, tested, and maintained.
- **Parallel run:** running the legacy LMS and the new LXP side by side for at least one full reporting cycle. This means paying for two systems, supporting two systems, and reconciling data between them.

**The compliance layer**

- **Data residency:** this affects hosting, vendor selection, and integration design.
- **Audit trails:** every learning record must be traceable and immutable. Migration must preserve original timestamps and never overwrite history.
- **Retention policies:** different record types have different retention periods. Migrating data you are not allowed to keep is a compliance risk, not a cost saving.
- **Legal and DPO review:** treat them as design partners, not a final approval step. If they see the plan for the first time at cutover, the project is already at risk.

**The people**

- **Internal PM and L&D time:** migration is a project, and someone has to run it. If it is added on top of existing responsibilities, something else will slip.
- **IT time:** integrations, data work, and infrastructure changes require engineering effort, even if the vendor "handles it."
- **Change management:** training, comms, champions, and support during rollout. This is what determines whether people actually use the new system.
- **Support during and after cutover:** a period of heightened support is not optional. It is part of the cost.

**The cost of staying**

Staying on the legacy system is not free either. It means continued license spend, manual workarounds, fragmented data, and the opportunity cost of not having modern learning infrastructure. In some cases, the migration pays for itself — but only if the legacy cost is honestly counted.

**The point:** the vendor quote covers the platform. The budget that gets approved should cover everything else.

## Vendor evaluation matrix

The topic is important enough to deserve its own document, where I go into detail:

→ **[Vendor Evaluation Matrix](vendor-evaluation-matrix.md)**

## Conclusions

**A migration is a data project, not a platform project:** The platform is the wrapper. Everything that determines success or failure sits inside it: clean records, intact audit trails, complete learning history. If the data is messy, no platform will save it.
**Content is an iceberg:** The visible part is the license and the interface. The submerged part is re-authoring SCORM courses that don't migrate cleanly. That is what eats the budget and the timeline, and it is almost never planned for.
**Compliance cannot be bolted on at the end:** Data residency, audit trails, and retention are architectural decisions, not settings. If legal and the DPO see the plan for the first time at cutover, the project is already at risk.
**Parallel run is insurance, and it costs double:** Two systems, two licenses, one team. But the parallel run is what shows whether the reports reconcile before the old system is switched off. One full reporting cycle is the minimum, not a luxury.
**The vendor quote is not the budget:** The license is roughly a third of the real cost. The rest is migration, integrations, compliance, and people. If the budget covers only the platform, it does not cover the project.
**Staying put is also a decision, and it also has a price:** Remaining on a legacy system means continued license spend, manual workarounds, and fragmented data. Sometimes the migration pays for itself, but only if the cost of doing nothing is counted honestly.
**If you cannot describe how to undo the migration, you are not ready to start it:** A rollback plan is not paranoia, it is what makes the project defensible to legal, audit, and compliance.

