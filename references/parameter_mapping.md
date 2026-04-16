# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `conditions` | `task.conditions` | 16 tokens covering standard/generalized x pro/anti x cue left/right | `W2030000493; W2133917458; W2128212281` | Fig. 1-2 and Methods in the anti-reach paper; reference-frame results in Bernier & Grafton and Chen et al. | `adapted` | Each token carries the full trial state for the generalized pro/anti design. |
| `condition_weights` | `task.condition_weights` | `null` | `W2030000493` | The paper randomizes all condition factors; no explicit weighting scheme is reported. | `inferred` | Even weighting is appropriate for balanced block generation. |
| `total_blocks` | `task.total_blocks` | Human `4`; QA/sim `1` | `W2030000493` | The paper uses repeated trials per condition; the exact block count is not fixed by the protocol. | `inferred` | Human profile is shortened for practical desktop runs. |
| `trial_per_block` | `task.trial_per_block` | Human `32`; QA/sim `16` | `W2030000493` | About 20 correct trials per condition are reported in the paper; the local build uses a reduced but balanced sampling plan. | `adapted` | Human profile yields 2 trials per condition per block. |
| `total_trials` | `task.total_trials` | Human `128`; QA/sim `16` | `W2030000493` | Derived from block count and per-block trial count. | `inferred` | Useful for summary screens and data QA. |
| `overall_seed` | `task.overall_seed` | `2026` | `W2030000493` | Deterministic replay is a build-system decision, not a literature parameter. | `inferred` | Used to make trial-spec sampling reproducible. |
| `position_step_px` | `task.position_step_px` | `145` px | `W2030000493; W2128212281` | Methods describe 5 cm lateral spacing for fixation, cue, and goal locations; the desktop implementation converts that spacing to pixels. | `adapted` | Shared horizontal step for eye/hand positions and cue/goal offsets. |
| `eye_row_y_px` | `task.eye_row_y_px` | `120` px | `W2030000493` | Visual separation between eye fixation and hand fixation is an implementation choice to keep the desktop display readable. | `inferred` | Upper-row marker for the eye fixation point. |
| `hand_row_y_px` | `task.hand_row_y_px` | `-120` px | `W2030000493` | Visual separation between eye fixation and hand fixation is an implementation choice to keep the desktop display readable. | `inferred` | Lower-row marker for the hand anchor. |
| `cue_row_y_px` | `task.cue_row_y_px` | `120` px | `W2030000493` | The spatial cue is presented in the eye-fixation row in the published task. | `adapted` | Keeps the cue aligned with the eye-centered frame. |
| `goal_row_y_px` | `task.goal_row_y_px` | `-120` px | `W2030000493` | The reach goal is defined relative to the hand fixation position in the published task. | `adapted` | The feedback marker sits on the hand row. |
| `frame_size_px` | `task.frame_size_px` | `84` px | `W2030000493` | The context cue is a square frame around fixation; the exact on-screen pixel size is inferred from the reported ~3 deg edge length. | `adapted` | Frame must remain visibly distinct from the fixation spot. |
| `fixation_radius_px` | `task.fixation_radius_px` | `8` px | `W2030000493` | The paper uses a small fixation spot; the exact pixel radius is an implementation inference. | `inferred` | Red eye fixation dot. |
| `hand_radius_px` | `task.hand_radius_px` | `18` px | `W2030000493` | The hand target is a visible circle at the starting location; exact radius is an implementation inference. | `inferred` | White hand anchor circle. |
| `cue_radius_px` | `task.cue_radius_px` | `14` px | `W2030000493` | The spatial cue is a brief white circular patch; exact radius is an implementation inference. | `inferred` | White cue dot at the go signal. |
| `goal_radius_px` | `task.goal_radius_px` | `16` px | `W2030000493` | The feedback goal marker is a visible endpoint patch; exact radius is an implementation inference. | `inferred` | Used only on feedback screens. |
| `left_key` | `task.left_key` | `f` | `W2030000493` | The local runtime uses keyboard left/right as a portable proxy for reach direction. | `inferred` | Config keeps the response mapping explicit. |
| `right_key` | `task.right_key` | `j` | `W2030000493` | The local runtime uses keyboard left/right as a portable proxy for reach direction. | `inferred` | Config keeps the response mapping explicit. |
| `key_list` | `task.key_list` | `[f, j, space]` | `W2030000493` | The task requires two response keys plus a continue key for instructions and breaks. | `inferred` | `space` is used to advance non-response screens. |
| `fixation_duration` | `timing.fixation_duration` | Human `[0.5, 1.0]`; QA `[0.3, 0.4]`; Sim `[0.25, 0.35]` | `W2030000493` | The paper reports a 0.5-1.0 s fixation period before the context cue. | `adapted` | QA/sim are shortened for validation speed. |
| `context_cue_duration` | `timing.context_cue_duration` | Human `0.2`; QA `0.12`; Sim `0.10` | `W2030000493` | Methods report a 0.2 s context cue flash. | `direct` | Green or blue frame around eye fixation. |
| `memory_hold_duration` | `timing.memory_hold_duration` | Human `[0.5, 1.5]`; QA `[0.25, 0.45]`; Sim `[0.2, 0.4]` | `W2030000493` | Methods report a 0.5-1.5 s memory period. | `direct` | Cue is absent during this delay. |
| `go_cue_duration` | `timing.go_cue_duration` | Human `0.17`; QA `0.10`; Sim `0.08` | `W2030000493` | Methods report a 0.17 s spatial cue/go-signal flash. | `direct` | White spatial cue at the cue location. |
| `response_deadline` | `timing.response_deadline` | Human `1.0`; QA `0.8`; Sim `0.7` | `W2030000493` | Methods report a maximum 1.0 s movement period. | `direct` | Used as the active response window. |
| `feedback_duration` | `timing.feedback_duration` | Human `0.3`; QA `0.2`; Sim `0.15` | `W2030000493` | Methods report a 0.3 s feedback period. | `direct` | Visual feedback is shown at the goal location. |
| `iti_duration` | `timing.iti_duration` | Human `0.6`; QA `0.2`; Sim `0.12` | `W2030000493` | The paper does not fix a desktop ITI; the build uses a conservative inferred value. | `inferred` | Allows clean separation between trials. |
| `fixation_onset` | `triggers.map.fixation_onset` | `20` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Marks the start of the fixation display. |
| `context_cue_onset` | `triggers.map.context_cue_onset` | `21` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Marks the colored rule-frame flash. |
| `memory_hold_onset` | `triggers.map.memory_hold_onset` | `22` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Marks the post-cue retention interval. |
| `go_cue_onset` | `triggers.map.go_cue_onset` | `23` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Marks the spatial cue flash. |
| `response_window_onset` | `triggers.map.response_window_onset` | `24` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Marks the active response-capture window. |
| `feedback_hit_onset` | `triggers.map.feedback_hit_onset` | `40` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Correct-trial feedback onset. |
| `feedback_miss_onset` | `triggers.map.feedback_miss_onset` | `41` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Error/timeout feedback onset. |
| `response_left` | `triggers.map.response_left` | `50` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Left-direction response code. |
| `response_right` | `triggers.map.response_right` | `51` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Right-direction response code. |
| `response_timeout` | `triggers.map.response_timeout` | `60` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Used when no valid key is pressed before deadline. |
| `iti_onset` | `triggers.map.iti_onset` | `70` | `W2030000493` | Trigger numbering is a build-system implementation detail. | `inferred` | Marks the inter-trial interval onset. |
