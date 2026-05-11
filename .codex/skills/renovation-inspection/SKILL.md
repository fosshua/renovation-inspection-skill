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

Use this skill to inspect residential renovation or fit-out construction from user-provided photos, videos, and text. The skill first identifies the construction stage, then loads that stage's dedicated reference materials before producing evidence-based, severity-ranked findings grounded first in applicable Chinese national standards, then in clearly labeled enterprise standards or visual best-practice comparisons when national standards do not cover the observed issue precisely.

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

2. Identify the construction stage.
   - Load `references/stage-inspection-matrix.yaml`.
   - Classify one or more likely stages from visual cues and text context.
   - Include stage confidence: `high`, `medium`, or `low`.
   - If evidence spans multiple stages, name the dominant stage and secondary stages.
   - If the stage is ambiguous, list candidate stages and ask for wider photos/video or project context before making stage-specific claims.

3. Load stage reference materials.
   - Load the detected stage entry from `references/stage-inspection-matrix.yaml`.
   - If `reference_package` is present, load the corresponding file under `references/stages/`.
   - Use the stage's `authoritative_standard_ids` to prioritize sources in `references/standards-sources.yaml`.
   - Use `supplemental_benchmark_ids`, manufacturer/design guidance, good examples, and bad example patterns only as supplemental references.
   - Keep stage `source_gaps` visible in uncertainty and evidence-gap handling.

4. Extract visual evidence.
   - Inspect only what is visible.
   - Record location, observable defect, affected component, and evidence reference.
   - Preserve per-image or per-timestamp references in every finding.

5. Retrieve assessment sources.
   - Load `references/standards-sources.yaml`.
   - Prefer applicable national or industry standards with source metadata from the detected stage.
   - Use enterprise standards only as supplemental best-practice benchmarks.
   - If no reliable source applies, label the basis as `visual_practical_judgment`.

6. Retrieve or compare reference examples.
   - Load `references/reference-image-strategy.md`.
   - Use stage package `good_example_requirements` and `bad_example_patterns` as comparison prompts.
   - Use reference examples only to compare observable construction attributes.
   - Do not treat a reference image as a legal pass/fail standard.

7. Detect and classify issues.
   - Compare evidence against the detected stage's `required_checks`, `common_issues`, and `bad_example_patterns`.
   - Convert a common issue into a finding only when visible evidence or user text supports it.
   - If a common issue is relevant but not visible, list it as an evidence gap or checklist item.
   - Split distinct issues into separate findings.
   - Avoid over-grouping unrelated defects.
   - Avoid hidden-work conclusions when evidence is incomplete.

8. Rank severity.
   - Sort by severity in this order: `critical`, `high`, `medium`, `low`, `info`.
   - Use the criteria in `references/severity-and-confidence.md`.
   - Consider `next_stage_gate` when judging urgency before the next construction step.

9. Produce structured output.
   - Follow `references/output-schema.json`.
   - Include an overall summary, most urgent next steps, findings, evidence gaps, and limitation note.
   - Mention the identified stage and the most important stage-specific checks.
   - Include `stage_id`, `stage_name`, and `common_issue_match` in findings when applicable.
   - When the request lacks images, video, measurements, or records needed for confidence, explicitly invite the user to supplement those materials.
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
- A concise prompt telling the user they can upload additional photos, videos, measurements, or施工记录 for a more reliable follow-up assessment.

Prefer specific supplement prompts:
- "请补充远景 + 近景照片，并用胶带或笔标出问题位置。"
- "请补充 10-20 秒横向视频，包含整体位置、近距离细节和尺子/水平尺参照。"
- "如果是隐蔽工程，请补充封槽/回填前照片、闭水记录、打压记录或材料标签。"
- "如果涉及尺寸或坡度，请补充带尺子的照片或水平仪/坡度测量结果。"

## Standards Basis Rules

- National standards and mandatory engineering construction standards are primary.
- Industry standards and local regulations may be used when clearly applicable.
- Enterprise standards are supplemental and must be labeled as non-authoritative benchmarks.
- Stage-specific standard IDs from `stage-inspection-matrix.yaml` determine source priority before generic source matching.
- Manufacturer instructions, design nodes, good examples, and bad examples are supplemental references unless the contract makes them binding.
- Always include source name, standard number or source ID, version/date when known, applicability, and confidence.
- If using third-party copies or summaries, state that the official text should be verified before contractual or legal use.

## Stage-Based Inspection Rules

Use stage packages to sharpen the inspection:
- `plumbing_electrical_rough_in`: focus on pressure testing, drainage testing, conduit continuity, pipe/conduit fixing, crossings, route archive, and closure readiness.
- `waterproofing`: focus on base quality, corners, pipe roots, thresholds, wall upturn height, coating continuity, protection, and water tests.
- `window_door_installation`: focus on frame fixing, frame-to-wall/floor gaps, gap filling, interior/exterior sealing, sill drainage, and edge finishing.
- `tiling_flooring`: focus on base cleanliness, hollowing, joint consistency, wet-area slope, and edge/threshold closure.
- `completion_acceptance`: focus on room-by-room visual quality, function tests, documentation, environmental records, and punch-list closure.

When a stage package is missing or incomplete, keep the stage classification but qualify confidence and ask for the missing source or project context.

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
- `references/stage-inspection-matrix.yaml`
- `references/stages/*.yaml`
- `references/reference-image-strategy.md`
- `references/severity-and-confidence.md`
- `tests/fixtures/README.md`
