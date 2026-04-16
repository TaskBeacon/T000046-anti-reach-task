# CHANGELOG

All notable development changes for `T000046-anti-reach-task` are documented here.

## [v0.1.0-dev] - 2026-04-16

### Changed
- Replaced the generic template controller and trial flow with a generalized anti-reach task built around eye/hand reference-frame manipulation.
- Added deterministic trial-spec generation in `src/utils.py` so cue side, goal side, and timing can be reproduced from the block seed and trial id.
- Rebuilt `src/run_trial.py` around `fixation -> context_cue -> memory_hold -> go_cue -> reach_response -> feedback -> iti` with explicit trial context on every participant-visible phase.
- Rewrote the human, QA, and sim configs to use the 16 anti-reach condition tokens, the published cue/memory/response timings, and the new trigger map.
- Added task-specific sampler responder behavior for simulation mode and kept the scripted sim path for smoke validation.
- Curated the reference bundle and manual mapping files to the anti-reach literature set.

### Fixed
- Removed the placeholder scaffold language from the README and assets documentation.
- Restored consistent UTF-8 participant-facing text, trigger naming, and summary screens for the anti-reach workflow.

## [0.1.0] - 2026-02-16

### Added
- Initial task scaffold generated from the PsyFlow template.
- Human/QA/sim mode entrypoint in `main.py`.
- Base configs under `config/` and trial logic under `src/`.
- Contract adoption metadata in `taskbeacon.yaml` (`contracts.psyflow_taps: v0.1.0`).
