## 1. Reference Data

- [x] 1.1 Add `references/shortcut-patterns.yaml` with common poor-practice patterns by stage.
- [x] 1.2 Link shortcut patterns to stage IDs, risk descriptions, required evidence, and remediation guidance.
- [x] 1.3 Extend stage packages with stage-gate wording where needed.

## 2. Skill Workflow

- [x] 2.1 Update `SKILL.md` to classify evidence strength separately from confidence.
- [x] 2.2 Add checked vs. unverified required-check reporting after stage package loading.
- [x] 2.3 Add stage-gate risk evaluation before next-step recommendations.
- [x] 2.4 Add shortcut-pattern comparison before findings are finalized.
- [x] 2.5 Add concrete next-shot guidance for missing evidence.
- [x] 2.6 Add rectification workflow guidance for findings.

## 3. Output Contract

- [x] 3.1 Extend `output-schema.json` with `evidence_strength`.
- [x] 3.2 Add stage-gate risk fields and inspection completeness fields.
- [x] 3.3 Add next-shot guidance and rectification workflow fields.
- [x] 3.4 Preserve existing stage, severity, confidence, and evidence reference fields.

## 4. Validation

- [x] 4.1 Update validation checklist for evidence strength, stage-gate risk, missing checks, next-shot guidance, and rectification workflow.
- [x] 4.2 Add fixture expectations for window gap, rough-in missing pressure test, waterproof missing water test, and shortcut-pattern detection.
- [x] 4.3 Validate JSON schema syntax.
- [x] 4.4 Run OpenSpec validation for the change.

## 5. Publishing

- [ ] 5.1 Commit implementation changes.
- [ ] 5.2 Push main branch update.
