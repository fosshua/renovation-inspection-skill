# Renovation Inspection Fixtures

Use these bundled image fixtures to validate the skill manually or in automated prompt tests. The fixture set is intentionally small: one normal/control case and two known issue cases. Video fixtures are intentionally not bundled.

## Image Assets

- `images/design-drawing-normal.jpg`: normal/control case. A design drawing photo, not a site construction defect photo.
- `images/window-bottom-gap.jpg`: issue case. Window bottom gap / edge finishing risk.
- `images/tile-haitang-angle-wide.jpg`: issue case. Oversized tile haitang angle / outside-corner workmanship risk.

## Case 1: Normal Control - Design Drawing

Input:
- `image_1`: `images/design-drawing-normal.jpg`

Expected:
- Treat the image as design/documentary evidence, not as a construction defect photo.
- Keep the answer short and say no confirmed site defect is visible.
- Do not invent construction-defect findings from the drawing alone.
- Suggest on-site checks for dimensions, water/electrical points, switch/socket/light positions, furniture clearances, and design changes.
- If stage is reported, mark construction-stage confidence as low or medium because the image is not site evidence.

## Case 2: Window Bottom Gap / Edge Finishing

Input:
- `image_1`: `images/window-bottom-gap.jpg`

Expected:
- Identify the primary stage as `window_door_installation`, with possible secondary stage `tiling_flooring`.
- Detect the visible oversized window frame bottom gap / edge finishing risk.
- Include `stage_id`, `stage_name`, evidence reference, evidence strength, severity, and stage-gate risk.
- Match `window_gap_hidden_by_thick_caulk` if the evidence suggests loose filler, thick caulk, or cover-up risk.
- Explain that final sealing, trim, or tile edge closure should pause until gap filling, inner/outer sealing, waterproofing, and drainage checks are verified.
- Ask for ruler-based gap close-up, wide photo, interior/exterior sealant views, and rain/water-spray evidence when applicable.

## Case 3: Oversized Tile Haitang Angle

Input:
- `image_1`: `images/tile-haitang-angle-wide.jpg`
- `text_1`: "海棠角宽度太大。"

Expected:
- Prefer `tiling_flooring` over `window_door_installation` because the user names 海棠角 and the image is a tile outside-corner detail.
- Detect oversized or inconsistent haitang-angle width as a tile outside-corner workmanship issue.
- Include shortcut pattern match `tile_haitang_angle_too_wide` when ruler evidence or user text supports it.
- Use `medium` severity by default; raise severity only if sharp edges, chipping, water exposure, or repeated broad failure is visible.
- Do not misclassify the image as a window gap only because a vertical dark edge is visible.
- Ask for a wide tile-corner location photo, perpendicular ruler close-up, side-angle photo showing both tile faces, and sample-board/design requirement if available.
