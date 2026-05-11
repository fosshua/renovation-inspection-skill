## Context

The renovation inspection skill now identifies construction stages and loads stage-specific reference packages. That improves what the skill checks, but professional inspection practice also emphasizes issue closure: what is confirmed, what is suspected, what remains unchecked, whether work can proceed, and what evidence proves rectification.

This change adds problem-discovery SOP behavior on top of the existing stage flow. The intent is not to manage the whole renovation project; it is to make each inspection result more actionable and less likely to miss stage-critical checks.

## Goals / Non-Goals

**Goals:**

- Make every finding clearer about evidence strength: confirmed, suspected, or not verifiable.
- Identify whether an issue blocks the next construction stage.
- Report stage-required checks that were verified and checks that remain unverified.
- Give users a specific next-shot script for follow-up photos, videos, measurements, or records.
- Add rectification workflow guidance that users can send to contractors.
- Add shortcut/poor-practice pattern references to catch common现场糊弄做法.
- Keep outputs concise enough for consumer use while preserving report-like structure.

**Non-Goals:**

- Manage schedules, payments, contracts, or contractor assignments as a full project management system.
- Make legal determinations or replace licensed inspection.
- Auto-generate formal legal claims.
- Enforce contractor-specific standards unless explicitly provided by the user or source references.

## Decisions

1. **Use evidence strength separate from confidence.**

   `confidence` describes how confident the skill is in its interpretation. `evidence_strength` describes the evidence state: `confirmed`, `suspected`, or `not_verifiable`. This avoids treating "must check but not visible" as a low-confidence defect.

2. **Add stage-gate risk to findings and summaries.**

   Each relevant finding can say whether it blocks the next stage. The overall response can include a concise proceed / do not proceed recommendation for the current stage.

3. **Use checked vs. unverified stage checks.**

   Stage packages already list required checks. The skill should report which checks are supported by evidence and which are missing. Missing checks should not become defects unless evidence supports a defect.

4. **Add next-shot guidance as a first-class output.**

   Follow-up prompts should be stage-specific and concrete: distance, angle, duration, tool, and record type. This makes multi-turn diagnosis more effective.

5. **Add shortcut-pattern references.**

   A new reference file will list common poor practices such as hiding large gaps with thick sealant, closing chases before pressure testing, or covering waterproofing before node photos. These are comparison patterns and require evidence before becoming findings.

6. **Add rectification workflow without contract enforcement.**

   The skill can suggest action, likely responsible party, reinspection evidence, and whether next-stage work should pause. It should not advise withholding payment as legal advice; it may say not to confirm the node as complete before reinspection.

## Risks / Trade-offs

- **Outputs may become too long** -> Keep the user-facing summary short and put details inside findings, missing checks, and next-shot guidance.
- **Stage-gate language can sound overly authoritative** -> Use "建议暂停/不建议进入下一步" and tie it to missing evidence or visible risk.
- **Shortcut patterns can over-bias the model** -> Require visible or textual evidence before converting a pattern into a finding.
- **Responsible-party suggestions can be wrong** -> Phrase as likely responsible party and include uncertainty when trade boundaries are unclear.

## Migration Plan

Additive update:

- Extend schema with evidence strength, stage-gate risk, checked/unverified checks, next-shot guidance, and rectification workflow.
- Add shortcut-pattern reference data.
- Update `SKILL.md` workflow and output rules.
- Update fixtures and validation checklist.

Rollback is to remove the new fields and shortcut reference while keeping the stage-based flow.
