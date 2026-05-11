# Validation Checklist

Use this checklist before marking the skill ready.

## Structured Output

- Every response includes `overall_assessment`.
- Every response includes `stage_assessment` with `primary_stage` and confidence.
- Every response includes `urgent_next_steps`.
- Every finding includes `id`, `severity`, `category`, `evidence_refs`, `observed_evidence`, `risk`, `reference_basis`, `recommendation`, and `confidence`.
- Findings include `stage_id` and `stage_name` when the construction stage is known.
- Findings include `evidence_strength` as `confirmed`, `suspected`, or `not_verifiable` when applicable.
- Findings include `common_issue_match` when the finding is based on a stage common issue pattern.
- Findings include stage-gate risk and rectification workflow when they affect next-stage work.
- Findings are sorted `critical`, `high`, `medium`, `low`, `info`.
- Each finding preserves image, video timestamp, or frame references.

## Stage Recognition

- The skill identifies the construction stage before selecting standards or producing findings.
- Mixed-stage inputs identify primary and secondary stages instead of forcing one stage.
- Ambiguous-stage inputs list likely candidate stages and request wider photos/video or stage context.
- Stage package materials are loaded before findings for high-priority stages.

## Standards Priority

- Applicable mandatory engineering codes and national standards appear before industry standards.
- Industry standards appear before enterprise benchmarks unless the user explicitly asks for an enterprise-standard comparison.
- Enterprise standards are labeled as supplemental and non-authoritative.
- Manufacturer instructions, design nodes, good examples, and bad examples are labeled as supplemental unless contractually binding.
- Detected stage source IDs are prioritized before generic source matching.
- Reference images are labeled as comparison evidence, not compliance basis.
- Visual judgment without a reliable standard is labeled `visual_practical_judgment` and confidence is qualified.

## Common Issue Comparison

- Common stage issues are converted to findings only when supported by evidence.
- Relevant but unobserved common stage issues are listed as evidence gaps or checklist items.
- High-priority stage package checks cover rough-in, waterproofing, window/door edge finishing, tiling/flooring, and completion acceptance.
- Shortcut or poor-practice patterns are converted to findings only when visible cues or user text support them.
- Missing required checks are reported as unverified, not as confirmed defects.

## Problem Discovery SOP

- Responses include checked and unverified stage-required checks when the stage is known.
- Responses include next-shot guidance that names capture distance, angle, duration, tool, or record type where applicable.
- Findings that block the next stage say so explicitly.
- Rectification workflow includes action, likely responsible party, reinspection evidence, and blocks-next-stage status.
- Evidence strength remains separate from confidence.

## Insufficient Evidence

- Blurry, cropped, distant, or missing-context inputs do not produce definitive pass/fail claims.
- Hidden plumbing, wiring, waterproofing, and structure are not judged unless directly visible or supported by records.
- The response asks for specific missing evidence, such as close-up photos, side views, level/ruler measurements, pressure-test records, water-retention records, or concealed-work photos.
- Text-only or low-confidence responses explicitly tell the user they can supplement photos, videos, measurements, or construction records for a follow-up assessment.

## High-Risk Escalation

- Structural, electrical, gas, waterproofing failure, fire safety, and similar findings recommend qualified professional or responsible-contractor review.
- High-risk findings include stop-work or pre-closure checks when delay would increase risk or rework cost.

## Privacy

- Test prompts and outputs do not require retaining raw private media.
- Logs or examples avoid addresses, faces, certificates, invoices, phone numbers, or other personal identifiers.
