# AI Assessment Framework

> **Disclaimer**
>
> This document is based on my own professional experience, accumulated notes, and research about learning platforms and AI in L&D. It is not an official methodology or a vendor-specific guide. Criteria, weights, and examples are illustrative and should be adapted to the specific context, scale, and regulatory environment of your organization.
>
> Comments, corrections, and alternative approaches are welcome.

## Why this framework exists

AI can generate assessment questions, feedback, and learning content faster than any team can review it manually. The question is whether the output is good enough to put in front of learners, and whether you can prove it if someone asks.

This framework is a practical rubric for evaluating AI-generated learning content and assessments before they reach users. It is built for the reality of L&D teams: limited review capacity and high volume.

## The four dimensions

Research on AI-generated educational resources consistently identifies four areas that matter most: content quality, process, human oversight, and AI-resilience. This framework is organized around those four dimensions.

### 1. Content quality

AI-generated content must be accurate, relevant, and aligned with learning objectives before anything else is evaluated.

| Criterion | What to check | Red flag |
|-----------|--------------|----------|
| **Accuracy & groundedness** | Facts, figures, and terminology are correct and verifiable against approved source material. Claims are traceable to internal knowledge or reputable sources. | Content that sounds confident but cannot be traced to a source. Convincing fake citations. |
| **Relevance & context** | Content matches the learning objective and reflects the learner's real environment. | Generic content that could apply to any role or topic. "Synthetic Content Syndrome" — polished but disconnected from the learner's reality. |
| **Completeness** | The content covers the necessary depth without gaps. | Missing steps, skipped context, or partial explanations. |
| **Tone & clarity** | Language is appropriate for the audience and easy to follow. | Overly complex, condescending, or inconsistent tone. Formulaic AI language patterns. |
| **Alignment** | The assessment actually tests the skill or knowledge it claims to test. | Questions that test recall when the objective is application. |

**Practical test:** take one AI-generated question or lesson. Ask: "Would a subject-matter expert approve this without changes?" If the answer is "probably not," it needs review.

### 2. Process documentation

Process documentation makes the use of AI transparent and auditable, which is essential in a regulated environment.

| Criterion | What to check | Red flag |
|-----------|--------------|----------|
| **Prompt traceability** | The exact prompt text used to generate the content is recorded with a version identifier. | No record of how the content was generated. |
| **Model version** | The AI model and version are documented, including the date of generation. | "We used ChatGPT" with no version or date. |
| **Review trail** | Who reviewed the content, when, and what they changed. | Content published with no human sign-off. |
| **Iteration history** | Revisions and corrections are logged. | Only the final version is kept. |

**Why this matters:** in an audit, "the AI generated it" is not an answer. "The AI generated it, a human reviewed it, and here is the record" is. Versioned rubrics and prompt hashes enable post-hoc auditing, any output can be traced back to the exact prompt and model configuration that produced it.

### 3. Human oversight (human-in-the-loop)

AI can generate, but humans must validate. Research on human-in-the-loop frameworks consistently shows that quality improves when human judgment is part of the process, not an afterthought.

| Level | What happens | When to use |
|-------|-------------|-------------|
| **Human-in-the-loop** | Every AI output is reviewed before use. | Compliance-critical content, assessments, certifications. |
| **Human-on-the-loop** | AI output is used directly, but a human monitors for issues. | Low-stakes content, practice questions, optional learning. |
| **Human-out-of-the-loop** | AI output is used without review. | Not recommended for any learner-facing content in a regulated environment. |

**Practical rule:** if the content can affect a compliance decision, a career path, or a performance review, it must be human-in-the-loop.

**Note on scaling:** human review is not a bottleneck if it is designed well. A structured HITL pipeline — with pre-grading configuration, preliminary AI scoring, human validation on the riskiest steps, and dual-logged audit trails — can reduce review time while maintaining quality.

### 4. AI-resilience

AI-resilience is about designing assessments that measure real capability, not the ability to prompt a model.

The PROTECT framework provides seven principles for designing AI-resilient assessments: **P**ersonalization, **R**ealism, **O**riginality, **T**axonomy-guided progression, **E**valuation diversity, **C**onstraints, and **T**ransparency.

| Criterion | What to check | Red flag |
|-----------|--------------|----------|
| **Higher-order thinking** | Questions require analysis, evaluation, or creation — not just recall. | Multiple-choice questions that can be answered by a search. |
| **Process evidence** | Learners document their reasoning, not just their answer. Checkpoints such as draft submissions, peer reviews, or progress updates. | Only final answers are submitted. |
| **Authentic context** | Tasks are grounded in real scenarios from your organization, with incomplete data and conflicting stakeholder interests. | Generic case studies that any AI can solve. |
| **Oral or performance component** | A live defense or demonstration is required for high-stakes assessments. | Assessment is entirely written and asynchronous. |
| **Transparency** | Learners document their AI use — prompts, tools, and validation steps. | AI use is hidden or unacknowledged. |

**Important note:** Detection tools are unreliable, and AI capabilities improve faster than detection methods. The better approach is to design assessments that require process, reasoning, and real-world context, things AI can assist with but cannot substitute.

## The scoring rubric

Use a 1–5 scale. Score the risk, not the enthusiasm. A 5 is "no material risk." A 3 is "acceptable, with caveats." A 1 is "this will block the project."

| Dimension | Weight | Score (1–5) | Evidence |
|-----------|--------|-------------|----------|
| Content quality | 35% | | Accuracy check, SME review notes |
| Process documentation | 25% | | Prompt log, review trail, version history |
| Human oversight | 20% | | Review records, sign-off log |
| AI-resilience | 20% | | Assessment design, process evidence |
| **Weighted total** | **100%** | | |

**Decision rule:**
- **4.0–5.0:** Ready for use. Monitor.
- **3.0–3.9:** Ready with conditions. Fix the weak dimension before scaling.
- **2.0–2.9:** Not ready. Requires redesign.
- **Below 2.0:** Do not use. Compliance risk.

## Worked example

**Scenario:** an AI-generated multiple-choice question for a compliance training module.

| Dimension | Score | Reasoning |
|-----------|-------|-----------|
| Content quality | 4 | Accurate, relevant, but slightly ambiguous wording. |
| Process documentation | 2 | No prompt record, no model version, no review trail. |
| Human oversight | 1 | Published without review. |
| AI-resilience | 2 | Recall-based question, easily answered by AI. |
| **Weighted total** | **2.4** | **Not ready.** Requires redesign and review. |

**What to fix:** add a human review step, document the prompt and model, and redesign the question to test application rather than recall.

## How I use this in practice

- **At the start of an AI pilot:** define which dimension is the risk. If it's compliance, human oversight is non-negotiable.
- **During content generation:** log prompts and model versions. It takes 30 seconds and saves hours in an audit.
- **Before publishing:** run the rubric. If the total is below 3.0, it doesn't go out.
- **After launch:** review a sample of AI-generated content monthly. Drift happens.

## Open questions

- How do we scale human review without becoming a bottleneck?
- What does "AI-resilient" mean for roles where AI will be part of the job?
- How do we measure whether AI-generated content improved learning outcomes, not just speed of production?
