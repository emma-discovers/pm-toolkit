# AI PRD for L&D

> **Disclaimer**
>
> This document is based on my experience with AI pilots in corporate learning, synthesised with best practices from AI product management frameworks (Karpathy's "Software 2.0", Anthropic's Responsible Scaling Policy, OpenAI Model Spec, EU AI Act risk tiers), and L&D domain expertise.
>
> It is not an official methodology. Adapt it to your context, scale, and regulatory environment.

## What makes an AI PRD different

A traditional PRD describes what to build. An AI PRD also defines **how the system behaves when it's wrong**, **what data it needs**, **how you'll know it's working**, and **what happens when it fails**. Without these, an AI feature is a demo that never ships.

An AI PRD is not a longer PRD. It is a different document. The core shift: the eval **is** the spec. A requirement like "the assistant should be helpful" is not a requirement — it's a wish. A real requirement says: "the assistant achieves ≥90% acceptance on a 200-item golden set, with hallucination rate ≤2% by faithfulness rubric, p95 latency under 1.8s, and cost-per-interaction under $0.05."[reference:0]

## Structure

### 1. Problem and context
- **What learning problem are we solving?** The user pain point, not the model.
- **Why is AI justified over a simpler alternative?** If a rule-based algorithm or a regular expression solves it, don't use an LLM. Generative AI introduces real latency, compute cost, and unpredictability. The PRD has to justify why the model is uniquely required.[reference:1]
- **What is the cost of being wrong?** This determines how much guardrailing and human review you need downstream.
- **Out of scope:** what this feature will not do.

### 2. Data requirements
- **Input data:** what the model needs (user role, grade, history, performance, feedback).
- **Data sources:** HRIS, LMS, surveys, external content.
- **Data quality:** what happens if data is missing or stale?
- **Privacy and compliance:** GDPR, 152-FZ, retention, consent.
- **Data inventory:** for each dataset, record source, fields, PII classification, rights/basis, retention period, residency, and access controls.[reference:2]
- **Data minimisation:** what data is explicitly off-limits.

### 3. Model behaviour
- **What the model does:** recommendation, generation, scoring, summarisation.
- **What the model does not do:** clearly defined boundaries.
- **Confidence and uncertainty:** how does the system handle low-confidence outputs?
- **Human-in-the-loop:** who reviews, when, and what they can override. Never write AI-generated data straight to a production system of record without review. Specify UX flows that let the user edit, regenerate, or reject the output before it's committed.[reference:3]
- **Explainability:** UI components that show why the model produced an answer — for example, citing the specific source document in a RAG system.[reference:4]
- **Refusal policy:** what should the model never do, what should it refuse, what should it redirect, and what should it answer plainly. "Don't be harmful" is not a refusal policy. A real policy lists concrete categories with examples.[reference:5]

### 4. Evaluation plan (required before rollout)
Define what "good" means before building.

**Offline evaluation:**
- **Golden set:** 200+ items covering 70% common / 20% edge / 10% adversarial cases for your domain.
- **Quality metrics:** acceptance rate (target ≥90%), hallucination rate (target ≤2% by faithfulness rubric), refusal rate on benign queries (target ≤4%), refusal rate on harmful queries (target ≥98%).[reference:6]
- **Human evaluation:** rubric (1–5) with definitions, reviewer sampling and calibration plan, inter-rater agreement target.[reference:7]
- **Performance metrics:** p95 latency, cost per interaction.

**Online evaluation:**
- **A/B test design:** pilot group, duration, success criteria.
- **Guardrail metrics:** what must NOT get worse (compliance, fairness, learner NPS).

**Bias and fairness:** what could go wrong, and how you monitor it.

**Drift:** how often you re-evaluate, and what triggers a retrain.

### 5. Fallback and failure modes
- **What happens if the model is unavailable?** Fallback model, degraded experience, or clear error message.
- **What happens if the model produces a harmful or incorrect output?** Escalation path, not just an error message. Human-in-the-loop design, not error handling.[reference:8]
- **What happens if the model is slow?** Stream the output. Token-by-token streaming dramatically improves perceived latency even when total generation time is unchanged.[reference:9]
- **How do we roll back?** Rollback trigger, owner, procedure, time-to-rollback.

### 6. Success metrics
- **Primary:** the one metric that defines success. In L&D: transformation rate (TR), time-to-first-value, retention.
- **Secondary:** supporting metrics (engagement, completion, NPS).
- **Guardrails:** what must not get worse (compliance, fairness, cost).
- **Cost per interaction:** estimated monthly cost at scale, based on token pricing. Output tokens typically cost 5–6x input tokens.[reference:10]

### 7. Rollout plan
- **Pilot group:** size, duration, success criteria.
- **Scale-up criteria:** what must be true to expand.
- **Kill criteria:** what would force a stop.
- **Rollout ramp:** shadow → internal → canary → percentage → GA, with gates at each stage.[reference:11]

### 8. Risk tier (EU AI Act)
Declare the risk tier upfront. In education and employment, the EU AI Act classifies certain applications as **high risk**, requiring conformity assessment, technical documentation, human oversight, and accuracy/robustness specifications.[reference:12]
- **Unacceptable risk:** banned.
- **High risk:** regulated heavily (education scoring, employment).
- **Limited risk:** transparency obligations (chatbots, AI-generated content disclosure).
- **Minimal risk:** unregulated.

## Worked example (anonymised)

**Feature:** AI-powered learning recommendations for IT specialists.

**Problem:** 14,000+ IT specialists, low engagement with generic catalogue. Goal: personalised learning paths based on role, grade, and past learning.

**Why AI:** Rule-based recommendation would only match on role and grade. LLM-based recommendation can reason over messy input: past projects, manager feedback, career goals.

**Data:** HRIS (role, grade, manager), LMS (completed courses, scores), feedback (NPS, open text). Missing data falls back to role-based defaults. PII classification: employee ID, email. Retention: 3 years for learning records, 7 years for compliance records.

**Model:** LLM-based recommender. Does not make compliance decisions. All recommendations reviewed by L&D before being shown to learners in the pilot.

**Evaluation:**
- Offline: 200 historical cases, relevance scored by 3 L&D experts (target: 80% agreement). Hallucination rate target ≤2%.
- Online: A/B test, 2,000 users, 6 weeks. Primary metric: time-to-first-value. Guardrail: NPS must not drop.

**Fallback:** if model unavailable, show existing catalogue with a banner. If confidence low, show top 3 role-based courses instead of personalised.

**Success metrics:** time-to-first-value ↓30%, NPS stable or up, no compliance issues. Cost per interaction: <$0.02.

**Rollout:** pilot 500 users, then scale to 2,000, then full.

## Red flags to avoid

1. **Hallucination-tolerance hand-waving.** "We will work hard to minimise hallucinations" is not a requirement. Name a number.[reference:13]
2. **No eval criteria before model selection.** Picking a model before defining what you're evaluating means you have no defensible reason for the choice.[reference:14]
3. **No fallback model.** Frontier-model outages happen. Vendor pricing changes happen. A single-vendor PRD bakes in operational risk that nobody named.[reference:15]
4. **"Accurate" without definition.** Accuracy is statistical, not categorical. Define the unit, evaluator, population, and consequence of error.[reference:16]
5. **Guardrails as an afterthought.** Guardrails are the result of having failed to encode requirements earlier in the system design. Runtime guardrails are almost always evidence that requirements weren't encoded upstream.[reference:17]

---

*Working draft. Comments and corrections welcome.*
