## 1. Stage Reference Data

- [ ] 1.1 Add `references/stage-inspection-matrix.yaml` with stage IDs, aliases, visual cues, standards source IDs, common issues, required checks, and recommended evidence.
- [ ] 1.2 Cover initial stages: demolition, masonry/base work, plumbing/electrical rough-in, waterproofing, window/door installation, tiling/flooring, carpentry/ceiling, paint/finish, fixture installation, and completion.
- [ ] 1.3 Link each stage to existing standards source IDs where available and mark missing sources for future expansion.
- [ ] 1.4 Add dedicated stage reference packages for high-priority stages: plumbing/electrical rough-in, waterproofing, window/door installation and edge finishing, tiling/flooring, and completion acceptance.
- [ ] 1.5 For each stage package, separate authoritative standards, supplemental enterprise benchmarks, manufacturer/design guidance, good examples, bad example patterns, required checks, recommended evidence, and next-stage gate criteria.

## 2. Skill Workflow

- [ ] 2.1 Update `SKILL.md` to classify construction stage immediately after input normalization.
- [ ] 2.2 Update standards retrieval guidance to filter and prioritize sources by recognized stage.
- [ ] 2.3 Update issue detection guidance to load the detected stage's dedicated reference materials before producing findings.
- [ ] 2.4 Update issue detection guidance to compare evidence against stage-specific common issue patterns before producing findings.
- [ ] 2.5 Add mixed-stage and ambiguous-stage handling with confidence and targeted evidence requests.

## 3. Output Contract

- [ ] 3.1 Update `output-schema.json` to allow stage context in findings and summary metadata.
- [ ] 3.2 Ensure findings can include `stage_id`, `stage_name`, and `common_issue_match` when applicable.
- [ ] 3.3 Preserve existing evidence references and severity fields.

## 4. Validation

- [ ] 4.1 Update validation checklist to require stage recognition, stage-specific source priority, and common issue comparison.
- [ ] 4.2 Add fixture coverage for plumbing/electrical rough-in, waterproofing, and window/door gap/edge finishing.
- [ ] 4.3 Add validation cases proving that stage packages are loaded before findings and that supplemental references are labeled correctly.
- [ ] 4.4 Validate JSON schema syntax.
- [ ] 4.5 Run OpenSpec validation for the change.

## 5. GitHub Publishing

- [ ] 5.1 Commit the OpenSpec proposal artifacts.
- [ ] 5.2 Push the proposal branch or main branch update after review.
