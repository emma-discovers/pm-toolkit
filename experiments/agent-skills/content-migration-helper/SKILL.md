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
```

## Rules

- `status` is `ready` only when the target LMS natively supports the
  standard and manifest integrity passes.
- `status` is `needs_review` when the standard is supported via conversion
  or the manifest has minor warnings.
- `status` is `re_author` when the standard is unsupported or the manifest
  is broken beyond repair.
- If a package uses a standard not in the target LMS's supported list,
  `status` is `re_author` regardless of manifest integrity.
- Never recommend migration of AICC content without a re-authoring plan.
- Do not modify content. Only audit and report.

## Edge Cases

- **Mixed-standard packages.** Some packages declare SCORM 2004 but contain
  xAPI calls. Report both, and flag as `needs_review`.
- **Missing manifest.** If `imsmanifest.xml` is absent or unparseable,
  status is `re_author` with rationale "manifest missing or malformed."
- **Absolute paths in manifest.** If resource paths are absolute URLs,
  flag as `needs_review` — they may break behind a CDN.
- **Duplicate item identifiers.** If two items share an identifier,
  flag as `needs_review` — tracking may collide.
- **Target LMS unknown.** If `lms_capability_check` returns no data,
  return `needs_review` for all items with rationale "target LMS
  capabilities could not be verified."
- **Content behind authentication.** If the package references external
  assets behind auth, flag as `needs_review`.

## Example

**Input:**
- `content_source`: `/catalogue/engineering/`
- `target_lms`: `docebo`
- `migration_scope`: `full`

**Inventory:**
- 3 SCORM 1.2 packages
- 1 SCORM 2004 package
- 1 xAPI package

**Target LMS check:**
- SCORM 1.2: supported
- SCORM 2004: supported
- xAPI: supported via LRS integration
- cmi5: supported

**Output:**
```json
{
  "summary": {
    "total_items": 5,
    "ready": 4,
    "needs_review": 1,
    "re_author": 0
  },
  "items": [
    {
      "content_id": "ENG-101",
      "title": "Engineering Fundamentals",
      "standard": "SCORM_1.2",
      "status": "ready",
      "tracking_risk": "medium",
      "target_support": "native",
      "rationale": "SCORM 1.2 is natively supported; completion and score will survive."
    },
    {
      "content_id": "ENG-205",
      "title": "Advanced Systems Design",
      "standard": "xAPI",
      "status": "needs_review",
      "tracking_risk": "low",
      "target_support": "via_conversion",
      "rationale": "xAPI requires LRS integration; verify LRS endpoint before migration."
    }
  ],
  "target_lms": "docebo",
  "notes": ["SCORM 1.2 packages will lose interaction-level data during migration."]
}
```

**Counter-example (re_author):**

**Input:**
- `content_source`: `/legacy/safety/`
- `target_lms`: `docebo`
- `migration_scope`: `full`

**Inventory:**
- 2 AICC packages

**Target LMS check:**
- AICC: unsupported

**Output:**
```json
{
  "summary": {
    "total_items": 2,
    "ready": 0,
    "needs_review": 0,
    "re_author": 2
  },
  "items": [
    {
      "content_id": "SAF-001",
      "title": "Workplace Safety Basics",
      "standard": "AICC",
      "status": "re_author",
      "tracking_risk": "high",
      "target_support": "unsupported",
      "rationale": "AICC is not supported by the target LMS; re-authoring in SCORM 2004 or xAPI is required."
    }
  ],
  "target_lms": "docebo",
  "notes": ["AICC content should be re-authored or retired, not migrated."]
}
```

## Platform Compatibility

| Platform | Supported |
|----------|-----------|
| Cursor | ✅ |
| Claude Code | ✅ |
| Codex | ✅ |
| Gemini CLI | ✅ |

## Related Skills

- [training-request-eligibility](../training-request-eligibility/SKILL.md) — for checking eligibility before booking training.
- [training-report](../training-report/SKILL.md) — for reporting on completed trainings.

## Limitations

- Assumes `content_inventory`, `manifest_parse`, and `lms_capability_check`
  tools are available.
- Does not validate runtime behaviour of packages — only structural integrity.
- Does not handle DRM-protected content.
- Tracking risk assessment is based on the standard, not on the actual
  content implementation. A SCORM 1.2 package with no interaction data
  may have lower risk than a poorly implemented SCORM 2004 package.
