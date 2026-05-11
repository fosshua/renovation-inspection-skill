## 1. Reference Data

- [ ] 1.1 Add `references/shortcut-patterns.yaml` with common poor-practice patterns by stage.
- [ ] 1.2 Link shortcut patterns to stage IDs, risk descriptions, required evidence, and remediation guidance.
- [ ] 1.3 Extend stage packages with stage-gate wording where needed.

## 2. Skill Workflow

- [ ] 2.1 Update `SKILL.md` to classify evidence strength separately from confidence.
- [ ] 2.2 Add checked vs. unverified required-check reporting after stage package loading.
- [ ] 2.3 Add stage-gate risk evaluation before next-step recommendations.
- [ ] 2.4 Add shortcut-pattern comparison before findings are finalized.
- [ ] 2.5 Add concrete next-shot guidance for missing evidence.
- [ ] 2.6 Add rectification workflow guidance for findings.

## 3. Output Contract

- [ ] 3.1 Extend `output-schema.json` with `evidence_strength`.
- [ ] 3.2 Add stage-gate risk fields and inspection completeness fields.
- [ ] 3.3 Add next-shot guidance and rectification workflow fields.
- [ ] 3.4 Preserve existing stage, severity, confidence, and evidence reference fields.

## 4. Validation

- [ ] 4.1 Update validation checklist for evidence strength, stage-gate risk, missing checks, next-shot guidance, and rectification workflow.
- [ ] 4.2 Add fixture expectations for window gap, rough-in missing pressure test, waterproof missing water test, and shortcut-pattern detection.
- [ ] 4.3 Validate JSON schema syntax.
- [ ] 4.4 Run OpenSpec validation for the change.

## 5. Publishing

- [ ] 5.1 Commit implementation changes.
- [ ] 5.2 Push main branch update.
