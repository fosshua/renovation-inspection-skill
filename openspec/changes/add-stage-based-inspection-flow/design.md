## Context

The renovation inspection skill currently normalizes inputs, extracts evidence, retrieves standards, compares references, detects issues, and ranks severity. Recent image and video tests show that accuracy improves when the skill understands the construction stage first: waterproofing, plumbing/electrical rough-in, window/door installation, tiling, and completion each have different standards, evidence needs, and common defect patterns.

This change adds a stage-based inspection layer. The layer does not replace existing issue detection; it constrains and improves it by selecting each stage's dedicated reference package before findings are produced. A reference package includes authoritative standards, supplemental enterprise workmanship guidance, manufacturer or design-node guidance, good examples, bad examples, common problems, required checks, stage-gate criteria, and evidence requests.

## Goals / Non-Goals

**Goals:**

- Identify one or more likely construction stages from images, video, and text.
- Load stage-specific reference materials before issue detection.
- Distinguish authoritative standards from supplemental enterprise benchmarks, manufacturer guidance, design nodes, and visual examples.
- Compare observed evidence against the current stage's expected work products and frequent defect patterns.
- Use good and bad construction examples as comparison aids without treating them as compliance authority.
- Keep ambiguous or mixed-stage requests explicit instead of forcing a single stage.
- Make output more targeted: stage, basis, common issue match, and missing evidence should be clear.

**Non-Goals:**

- Build a complete construction project management system.
- Replace professional stage acceptance, hidden-work inspection, or legal acceptance.
- Guarantee exhaustive coverage of every local standard, material system, or contractor-specific process.
- Add live web search or an external standards database in this change.

## Decisions

1. **Add stage detection as a required step after input normalization.**

   Stage detection will classify evidence into known stages such as demolition, masonry/base work, plumbing/electrical rough-in, waterproofing, window/door installation, tiling/flooring, carpentry/ceiling, paint/finish, installation/fixtures, and completion. The output may contain multiple candidate stages with confidence.

   Alternative considered: keep stage as optional context. That keeps the workflow simpler but allows the model to apply generic standards too early.

2. **Use a structured stage matrix reference plus stage-specific reference packages.**

   Add `references/stage-inspection-matrix.yaml` with stage IDs, visual cues, reference package links, applicable standards/source IDs, required checks, common issues, and recommended supplemental evidence. Add stage packages under `references/stages/` when a stage needs richer detail.

   The stage matrix entries should support:
   - `stage_id`
   - `stage_name`
   - `aliases`
   - `visual_cues`
   - `authoritative_standard_ids`
   - `supplemental_benchmark_ids`
   - `manufacturer_or_design_guidance`
   - `good_example_requirements`
   - `bad_example_patterns`
   - `required_checks`
   - `common_issues`
   - `recommended_evidence`
   - `next_stage_gate`
   - `source_gaps`

   Alternative considered: put all stage rules directly into `SKILL.md`. That would be easier initially but harder to maintain as stages grow.

3. **Stage-specific sources filter standard retrieval.**

   The skill will still use `standards-sources.yaml`, but stage detection will decide which source IDs and issue categories to prioritize. National and mandatory standards remain higher authority than enterprise benchmarks.

   Alternative considered: separate standards per stage. That duplicates source metadata and increases update risk.

4. **Common issues are comparison prompts, not automatic findings.**

   A stage common issue becomes a finding only when there is visible evidence or user-provided text support. Otherwise it becomes an evidence gap or checklist item.

   Alternative considered: emit every common issue as a warning. That would produce noisy, low-confidence results.

5. **Mixed-stage handling stays explicit.**

   If the evidence shows multiple stages, the skill will inspect each stage separately or name the dominant stage and secondary stage. Findings should include `stage_id` where possible.

6. **Prioritize high-value initial stage packages.**

   The first implementation should deeply cover plumbing/electrical rough-in, waterproofing, window/door installation and edge finishing, tiling/flooring, and completion acceptance because recent tests show these are common user inputs and high-risk decision points. Other stages can start with lighter packages and explicit `source_gaps`.

## Risks / Trade-offs

- **Stage misclassification can lead to wrong standards** -> Include stage confidence and fallback to multiple candidate stages when cues are mixed.
- **The stage matrix can become stale or incomplete** -> Keep it as an initial reference and require source verification before legal or acceptance use.
- **Common issue lists may bias findings** -> Require evidence support before converting a common issue into a defect.
- **More structured output can make responses longer** -> Keep user-facing summaries concise and place detailed checks in findings/evidence gaps.
- **Some images show details without enough stage context** -> Ask for project stage, room, next planned process, and wider photos/video.

## Migration Plan

Implement as an additive skill update:

- Add the stage matrix reference file.
- Add dedicated stage reference data for the initial stages.
- Update `SKILL.md` workflow to classify stage before standards retrieval.
- Update output guidance to include stage context and stage-specific evidence gaps.
- Update validation fixtures to test stage recognition and stage-aware issue checks.

Rollback is to remove the stage matrix and restore the previous generic inspection workflow.
