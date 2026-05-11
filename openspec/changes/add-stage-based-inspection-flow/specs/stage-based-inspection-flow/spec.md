## ADDED Requirements

### Requirement: Construction stage recognition
The skill SHALL identify the likely construction stage before selecting standards or producing findings.

#### Scenario: Single clear stage
- **WHEN** the evidence clearly shows plumbing and electrical rough-in
- **THEN** the skill SHALL classify the stage as plumbing/electrical rough-in with confidence before checking issues

#### Scenario: Mixed stage evidence
- **WHEN** the evidence shows more than one stage such as waterproofing plus window installation
- **THEN** the skill SHALL identify each relevant stage or distinguish the dominant stage from secondary stages

#### Scenario: Ambiguous stage
- **WHEN** the evidence does not provide enough information to classify the stage reliably
- **THEN** the skill SHALL state the likely candidate stages and ask for specific stage context or wider evidence

### Requirement: Stage-specific standards retrieval
The skill SHALL use the recognized construction stage to prioritize applicable standards and benchmark sources.

#### Scenario: Waterproofing stage
- **WHEN** the stage is waterproofing
- **THEN** the skill SHALL prioritize waterproofing-related mandatory, national, or industry standards before enterprise benchmarks

#### Scenario: Plumbing and electrical rough-in stage
- **WHEN** the stage is plumbing/electrical rough-in
- **THEN** the skill SHALL prioritize electrical installation, water supply/drainage, and construction quality control sources before generic workmanship sources

#### Scenario: Window or door installation stage
- **WHEN** the stage is window/door installation or window edge finishing
- **THEN** the skill SHALL prioritize decoration quality, door/window installation, waterproof sealing, and design-node evidence

### Requirement: Stage common issue comparison
The skill SHALL compare observed evidence against the common issue patterns for the recognized stage.

#### Scenario: Evidence matches common issue
- **WHEN** visible evidence matches a stage-specific common issue pattern
- **THEN** the skill SHALL convert that match into a finding with the evidence reference and risk explanation

#### Scenario: Common issue lacks evidence
- **WHEN** a common stage issue is relevant but not visible or supported by text
- **THEN** the skill SHALL list it as an evidence gap or checklist item instead of a confirmed finding

### Requirement: Stage-aware evidence requests
The skill SHALL request supplemental evidence that is specific to the recognized stage and issue type.

#### Scenario: Rough-in evidence request
- **WHEN** the stage is plumbing/electrical rough-in and evidence is incomplete
- **THEN** the skill SHALL request pressure test records, drainage test video, conduit continuity checks, pipe crossing close-ups, and full-route photos as applicable

#### Scenario: Waterproofing evidence request
- **WHEN** the stage is waterproofing and evidence is incomplete
- **THEN** the skill SHALL request close-ups of corners, pipe roots, door thresholds, wall upturn height with a ruler, and water-retention or shower test records as applicable

#### Scenario: Window edge evidence request
- **WHEN** the stage is window/door installation or window finishing and evidence is incomplete
- **THEN** the skill SHALL request ruler-based gap photos, interior and exterior sealant views, frame fixing details, and water-spray or rain observation evidence as applicable

### Requirement: Stage context in output
The skill SHALL include stage context in its reasoning and user-facing output.

#### Scenario: Finding includes stage
- **WHEN** the skill returns a finding
- **THEN** the finding SHALL identify the relevant stage or stage category when the stage is known

#### Scenario: Summary includes stage
- **WHEN** the skill completes an inspection
- **THEN** the overall summary SHALL mention the identified stage and the most important stage-specific checks
