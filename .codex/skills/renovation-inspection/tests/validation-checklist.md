# Validation Checklist

Use this checklist before marking the skill ready.

## Structured Output

- Every response includes `overall_assessment`.
- Every response includes `urgent_next_steps`.
- Every finding includes `id`, `severity`, `category`, `evidence_refs`, `observed_evidence`, `risk`, `reference_basis`, `recommendation`, and `confidence`.
- Findings are sorted `critical`, `high`, `medium`, `low`, `info`.
- Each finding preserves image, video timestamp, or frame references.

## Standards Priority

- Applicable mandatory engineering codes and national standards appear before industry standards.
- Industry standards appear before enterprise benchmarks unless the user explicitly asks for an enterprise-standard comparison.
- Enterprise standards are labeled as supplemental and non-authoritative.
- Reference images are labeled as comparison evidence, not compliance basis.
- Visual judgment without a reliable standard is labeled `visual_practical_judgment` and confidence is qualified.

## Insufficient Evidence

- Blurry, cropped, distant, or missing-context inputs do not produce definitive pass/fail claims.
- Hidden plumbing, wiring, waterproofing, and structure are not judged unless directly visible or supported by records.
- The response asks for specific missing evidence, such as close-up photos, side views, level/ruler measurements, pressure-test records, water-retention records, or concealed-work photos.

## High-Risk Escalation

- Structural, electrical, gas, waterproofing failure, fire safety, and similar findings recommend qualified professional or responsible-contractor review.
- High-risk findings include stop-work or pre-closure checks when delay would increase risk or rework cost.

## Privacy

- Test prompts and outputs do not require retaining raw private media.
- Logs or examples avoid addresses, faces, certificates, invoices, phone numbers, or other personal identifiers.
