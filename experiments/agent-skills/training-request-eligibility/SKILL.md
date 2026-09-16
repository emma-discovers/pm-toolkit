---
name: training-request-eligibility
description: >
  Decides whether an employee is eligible for a requested training course
  and matches the request to an L&D catalogue entry. Use when the user
  asks to check training eligibility, approve a training request, match
  a requested course to the catalogue, or validate a learning request
  against employee grade, tenure, and history. Do not use when the task
  is to create or modify the catalogue itself.
allowed-tools: employee_get, employee_history, catalogue_match
---

# Training Request Eligibility

Check whether an employee can take a requested training course, and if so,
which catalogue course matches the request.

## Use When

- User asks: "Can this employee take this training?"
- User provides a training request and wants a verdict.
- User needs to match a free-text course title to a catalogue entry.
- User wants to validate a learning request against grade, tenure, and history.
- User asks "is this duplicate?" or "did they already take this?"

## Inputs

The request must include:

- `employee_id` — the employee requesting training.
- `requested_course` — the course title as written by the requester.
- `estimated_cost` — optional, in the local currency.
- `target_start_date` — optional, YYYY-MM-DD.

If any required input is missing, ask for it before proceeding.

## Procedure

1. **Pull employee data.**
   Call `employee_get(employee_id=<employee_id>)`. Read `grade`,
   `cost_centre`, `tenure_months`, and `home_market`.

2. **Check for duplicates.**
   Call `employee_history(employee_id=<employee_id>)`. Search for the same
   topic within the last 12 months. A duplicate is a hard ineligibility ground.

3. **Apply eligibility gates.**
   - Minimum grade: the employee's grade must meet the topic's minimum.
   - Prerequisites: any required prior course must appear in `employee_history`.
   - Tenure: if the topic requires a minimum tenure, check `tenure_months`.

4. **Match against the catalogue.**
   Call `catalogue_match(topic=<topic>, requested_title=<requested_course>,
   target_start_date=<target_start_date>)`. The tool returns `course_id`,
   `vendor`, `confirmed_cost`, `course_start_date`, and `match_quality`
   ∈ {exact, closest, none}.

5. **Emit a verdict.**
   - `eligible` — all gates pass and `match_quality` is `exact` or `closest`.
   - `ineligible` — any gate fails. The rationale must name the failing rule.
   - `needs_review` — gates pass but `match_quality` is `none` or the
     catalogue returned multiple close matches.

## Output Format

Return exactly one JSON object, no prose:

```json
{
  "verdict": "eligible" | "ineligible" | "needs_review",
  "course_id": "<catalogue id or closest alternative id>",
  "vendor": "<vendor name>",
  "confirmed_cost": <number>,
  "course_start_date": "<YYYY-MM-DD>",
  "match_quality": "exact" | "closest" | "none",
  "rationale": "one sentence citing the deciding rule"
}
