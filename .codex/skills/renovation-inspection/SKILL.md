---
name: renovation-inspection
description: Inspect home renovation construction from images, videos, and text. Use when the user asks whether current renovation work has quality, safety, workmanship, sequencing, or standards issues and wants severity-ranked findings with remediation advice.
license: MIT
compatibility: Requires a multimodal model for image/video evidence and optional retrieval over standards/reference examples.
metadata:
  author: family-app
  version: "0.1.0"
  generatedBy: openspec add-renovation-inspection-skill
---

# Renovation Inspection

Use this skill to inspect residential renovation or fit-out construction from user-provided photos, videos, and text. The skill produces evidence-based, severity-ranked findings grounded first in applicable Chinese national standards, then in clearly labeled enterprise standards or visual best-practice comparisons when national standards do not cover the observed issue precisely.

## Scope

Assess visible renovation work for:
- Quality and workmanship defects.
- Safety risks involving structure, electrical, gas, fire protection, water supply/drainage, waterproofing, and fall or injury hazards.
- Installation completeness, sequencing, protection, material use, and rework risk.
- Standard or benchmark deviations that can be supported by provided evidence.

Do not claim to verify hidden work, concealed waterproofing, embedded wiring, embedded pipe pressure tests, structural capacity, or legal acceptance unless the evidence explicitly shows the relevant condition and a reliable source supports the conclusion.

## Required Workflow

1. Normalize the request.
   - Identify input types: images, video, text, or mixed.
   - Label each image as `image_1`, `image_2`, etc.
   - For video, identify observable timestamps or representative frames as `video_1@00:12`, `video_1@frame_3`, etc.
   - Label the user's text description or concern as `text_1` when it is used as evidence.
   - Extract text context: room, renovation stage, trade, material, user concern, claimed measurements, and project constraints.

2. Extract visual evidence.
   - Inspect only what is visible.
   - Record location, observable defect, affected component, and evidence reference.
   - Preserve per-image or per-timestamp references in every finding.

3. Retrieve assessment sources.
   - Load `references/standards-sources.yaml`.
   - Prefer applicable national or industry standards with source metadata.
   - Use enterprise standards only as supplemental best-practice benchmarks.
   - If no reliable source applies, label the basis as `visual_practical_judgment`.

4. Retrieve or compare reference examples.
   - Load `references/reference-image-strategy.md`.
   - Use reference examples only to compare observable construction attributes.
   - Do not treat a reference image as a legal pass/fail standard.

5. Detect and classify issues.
   - Split distinct issues into separate findings.
   - Avoid over-grouping unrelated defects.
   - Avoid hidden-work conclusions when evidence is incomplete.

6. Rank severity.
   - Sort by severity in this order: `critical`, `high`, `medium`, `low`, `info`.
   - Use the criteria in `references/severity-and-confidence.md`.

7. Produce structured output.
   - Follow `references/output-schema.json`.
   - Include an overall summary, most urgent next steps, findings, evidence gaps, and limitation note.
   - Use Chinese by default when the user asks in Chinese.

## Input Handling

### Images

- Assign a stable evidence ID to each submitted image.
- Mention the evidence ID in every finding based on that image.
- If the same issue appears in multiple images, include all relevant evidence IDs.
- Do not infer dimensions, slopes, cable size, water pressure, flatness tolerance, or waterproofing height unless visible scale, measurement marks, or user-provided measurements support it.

### Video

- Sample representative frames or timestamped observations.
- Findings from video must include a timestamp or frame reference when possible.
- If motion blur, lighting, camera angle, or missing close-ups prevents reliable inspection, state that limitation and request the specific missing shot.

### Text

Extract and use:
- Renovation stage: demolition, plumbing/electrical rough-in, waterproofing, tiling, carpentry, paint, installation, completion.
- Room/area: bathroom, kitchen, balcony, living room, bedroom, corridor, exterior, utility area.
- Trade/system: masonry, waterproofing, plumbing, electrical, HVAC, tiling, flooring, ceiling, cabinetry, paint.
- Materials and measurements claimed by the user.
- User's explicit concern.
- Use `text_1` in `evidence_refs` for findings based only on the user's description.

## Insufficient Evidence Handling

When evidence is insufficient, do not force a pass/fail result. Return:
- What cannot be verified.
- Why current evidence is insufficient.
- The exact extra media or measurement needed, such as a close-up, side-angle shot, level measurement, ruler reference, water test record, pressure test record, concealed-work photo, or product label.

## Standards Basis Rules

- National standards and mandatory engineering construction standards are primary.
- Industry standards and local regulations may be used when clearly applicable.
- Enterprise standards are supplemental and must be labeled as non-authoritative benchmarks.
- Always include source name, standard number or source ID, version/date when known, applicability, and confidence.
- If using third-party copies or summaries, state that the official text should be verified before contractual or legal use.

## Reference Image Comparison Rules

Use reference examples to compare:
- Alignment, levelness cues, spacing consistency, slope direction, protection measures, routing neatness, fixing/support intervals, surface flatness cues, waterproofing coverage, closure/detail completeness, and installation sequence indicators.

Do not use reference examples to:
- Override national standards.
- Judge hidden work.
- Prefer purely aesthetic style.
- Declare compliance without a standards basis.

## Output Style

- Start with a concise overall assessment.
- List findings in severity order.
- For each finding, include evidence, risk, basis, confidence, and actionable remediation.
- Use direct, practical language suitable for a homeowner or project manager.
- For high-risk items, recommend stopping related work and involving a qualified professional or responsible contractor.
- Include a limitation note when safety, structure, electrical, waterproofing, gas, fire safety, or legal acceptance is involved.

## Privacy and Safety

- Treat renovation photos and videos as private home media.
- Do not retain media beyond the inspection workflow unless explicit product policy or user consent allows it.
- Do not log raw media, exact home addresses, personal identifiers, certificates, invoices, or other sensitive details.
- This skill is decision support, not a replacement for qualified inspection, engineering review, or legal acceptance.

## References

- `references/output-schema.json`
- `references/standards-sources.yaml`
- `references/reference-image-strategy.md`
- `references/severity-and-confidence.md`
- `tests/fixtures/README.md`
