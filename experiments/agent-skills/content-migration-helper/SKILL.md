---
name: content-migration-helper
description: >
  Audits SCORM, xAPI, cmi5, and AICC content before migrating it between
  LMS platforms. Use when the user asks to check content readiness for
  migration, validate SCORM manifests, audit tracking data, compare content
  against a target LMS, or plan a content migration. Do not use when the
  task is to create new content or configure the target LMS.
allowed-tools: file_read, manifest_parse, content_inventory, lms_capability_check
---

# Content Migration Helper

Audit learning content before migrating it between LMS platforms. The goal
is to identify what will break, what will lose tracking data, and what
needs re-authoring.

## Use When

- User asks: "Will this SCORM package work in the new LMS?"
- User needs a pre-migration content audit.
- User wants to check whether tracking data will survive migration.
- User asks to compare content standards against target LMS capabilities.
- User needs to identify content that must be re-authored or retired.

## Inputs

The request must include:

- `content_source` — path or catalogue reference to the content.
- `target_lms` — the platform the content is moving to.
- `migration_scope` — `full` (all content) or `sample` (specific packages).

If `target_lms` is missing, ask for it before proceeding.

## Procedure

1. **Inventory the content.**
   Call `content_inventory(source=<content_source>)`. Group by standard:
   SCORM 1.2, SCORM 2004, xAPI, cmi5, AICC, native. Read `imsmanifest.xml`
   for each package and record `identifier`, `title`, `version`, `schema`.

2. **Check manifest integrity.**
   Call `manifest_parse(package=<content_source>)`. Verify:
   - Resource paths are relative and complete.
   - Item identifiers are unique within the package.
   - Launch URL is present and resolves.
   - `imsmanifest.xml` is well-formed XML.

3. **Check target LMS compatibility.**
   Call `lms_capability_check(lms=<target_lms>)`. Read supported standards
   and versions. Compare against the inventory from step 1.

4. **Assess tracking data risk.**
   For each package, classify tracking risk:
   - `low` — xAPI or cmi5; statements are portable via LRS.
   - `medium` — SCORM 2004; completion and score are portable, interaction
     data may be lost.
   - `high` — SCORM 1.2 or AICC; completion may survive, but fine-grained
     tracking is often lost. Re-authoring may be required.

5. **Emit a report.**
   For each content item, return: `status` (`ready`, `needs_review`,
   `re-author`), `standard`, `tracking_risk`, `target_support`, and
   `rationale`.

## Output Format

Return exactly one JSON object, no prose:

```json
{
  "summary": {
    "total_items": <number>,
    "ready": <number>,
    "needs_review": <number>,
    "re_author": <number>
  },
  "items": [
    {
      "content_id": "<identifier from manifest>",
      "title": "<title>",
      "standard": "SCORM_1.2" | "SCORM_2004" | "xAPI" | "cmi5" | "AICC",
      "status": "ready" | "needs_review" | "re_author",
      "tracking_risk": "low" | "medium" | "high",
      "target_support": "native" | "via_conversion" | "unsupported",
      "rationale": "one sentence citing the deciding factor"
    }
  ],
  "target_lms": "<lms name>",
  "notes": ["<optional caveats>"]
}
