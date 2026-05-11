## ADDED Requirements

### Requirement: Evidence strength classification
The skill SHALL classify each finding or stage-required check by evidence strength.

#### Scenario: Confirmed issue
- **WHEN** a defect is directly visible in image or video evidence
- **THEN** the skill SHALL mark the evidence strength as `confirmed`

#### Scenario: Suspected issue
- **WHEN** evidence suggests a problem but lacks measurement, angle, clarity, or records
- **THEN** the skill SHALL mark the evidence strength as `suspected` and request specific follow-up evidence

#### Scenario: Not verifiable check
- **WHEN** a stage-required check is relevant but not visible or supported by records
- **THEN** the skill SHALL mark it as `not_verifiable` instead of reporting it as a confirmed defect

### Requirement: Stage-gate risk assessment
The skill SHALL assess whether findings or missing checks block the next construction stage.

#### Scenario: Blocking issue before closure
- **WHEN** a high-risk rough-in, waterproofing, or window-edge issue is visible before it will be covered
- **THEN** the skill SHALL state that next-stage work should not proceed until the issue is resolved or verified

#### Scenario: Missing required check before next stage
- **WHEN** a required stage check such as pressure testing, water testing, or slope verification is missing
- **THEN** the skill SHALL list the missing check and explain whether it blocks the next stage

### Requirement: Missing-check reporting
The skill SHALL report checked and unverified required checks for the recognized stage.

#### Scenario: Evidence supports required check
- **WHEN** submitted evidence proves a stage-required check was performed
- **THEN** the skill SHALL list the check as verified or checked

#### Scenario: Evidence does not support required check
- **WHEN** submitted evidence does not show a stage-required check
- **THEN** the skill SHALL list the check as unverified with the evidence needed to verify it

### Requirement: Next-shot guidance
The skill SHALL provide concrete follow-up capture instructions when more evidence is needed.

#### Scenario: Window gap needs measurement
- **WHEN** a window gap or edge finishing issue lacks scale
- **THEN** the skill SHALL request a ruler or feeler-gauge close-up, wide location photo, interior/exterior sealant views, and water-spray evidence when relevant

#### Scenario: Rough-in needs records
- **WHEN** plumbing or electrical rough-in evidence lacks required records
- **THEN** the skill SHALL request pressure gauge photos, drainage test video, conduit continuity evidence, full-route photos, and crossing close-ups as applicable

### Requirement: Rectification workflow
The skill SHALL provide actionable rectification workflow details for confirmed or suspected findings.

#### Scenario: Finding needs reinspection
- **WHEN** the skill reports a finding that requires correction
- **THEN** the finding SHALL include recommended action, likely responsible party, reinspection evidence, and whether it blocks next-stage work

#### Scenario: Professional escalation is required
- **WHEN** a finding involves structural, electrical, gas, fire, major waterproofing, or safety risk
- **THEN** the skill SHALL recommend qualified professional or responsible-contractor review before proceeding

### Requirement: Shortcut-pattern detection
The skill SHALL compare evidence against common poor-practice patterns without treating patterns as defects unless evidence supports them.

#### Scenario: Shortcut pattern is visible
- **WHEN** visible evidence matches a known poor-practice pattern
- **THEN** the skill SHALL include the matched pattern in the finding and explain the risk

#### Scenario: Shortcut pattern is relevant but not visible
- **WHEN** a common poor-practice pattern is relevant to the stage but not visible
- **THEN** the skill SHALL include it as a checklist item or evidence gap instead of a confirmed finding

### Requirement: Inspection completeness
The skill SHALL summarize inspection completeness for the recognized stage.

#### Scenario: Some checks remain unverified
- **WHEN** only part of a stage's required checks are supported by submitted evidence
- **THEN** the skill SHALL report checked and unverified counts or lists

#### Scenario: No stage can be confirmed
- **WHEN** the construction stage cannot be identified with enough confidence
- **THEN** the skill SHALL avoid completeness scoring and request wider context
