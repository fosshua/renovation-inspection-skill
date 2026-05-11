# Reference Image Strategy

Reference images improve visual comparison but do not create compliance obligations by themselves.

## Source Preference

1. Curated internal gallery with known provenance, trade category, construction stage, and source permission.
2. Publicly documented manufacturer, training, or enterprise施工标准 images with clear context.
3. External image search results only when provenance can be described and the result is used as a non-authoritative visual comparison.

## Required Metadata

Each reference image entry should include:
- `reference_id`
- `source_name`
- `source_url_or_location`
- `permission_status`
- `room_or_trade`
- `construction_stage`
- `observable_good_practice`
- `not_a_compliance_basis: true`

## Comparison Attributes

Compare observable attributes, including:
- Alignment and levelness cues.
- Gap consistency.
- Slope direction and drainage path.
- Waterproofing coverage, upturn, corner treatment, and pipe-root detail when visible.
- Pipe and conduit routing neatness, crossing, spacing, protection, and fixing.
- Socket box, switch box, drain, valve, inspection opening, and fixture positioning.
- Surface flatness cues, cracking, hollowing indicators, contamination, and finish consistency.
- Finished-product protection and construction sequencing.

## Output Rules

- Label reference-image support as `reference_image_comparison`.
- State which observable attribute differs from the reference example.
- Do not describe an image as a legal standard.
- Do not infer hidden-layer quality from a finished-surface reference image.
