# Task Logic Audit: Anti-Reach Task

## 1. Paradigm Intent

- Task: `anti-reach`
- Primary construct: context-dependent sensorimotor transformation in eye-centered and hand-centered reference frames, with anti-response inhibition over a prepotent reach direction
- Manipulated factors:
  - rule cue (`pro` vs `anti`)
  - reference-frame arrangement (`standard` same-side fixation vs `generalized` split eye/hand fixation)
  - cue side (`left` vs `right` relative to eye fixation)
  - fixation laterality (`left` vs `right`)
- Dependent measures:
  - response accuracy
  - response latency as a keyboard proxy for reach initiation
  - timeout rate
  - original paper outcomes also include movement time and endpoint variability, but those are not directly measurable in the local keyboard-only runtime
- Key citations:
  - `W2030000493` (Westendorff & Gail, 2010, Experimental Brain Research, supplemental context only)
  - `W2133917458` (Bernier & Grafton, 2010, Neuron)
  - `W2012315642` (Gail & Andersen, 2006, Journal of Neuroscience)
  - `W2128212281` (Chen et al., 2014, Journal of Neuroscience)
  - `W1986350479` (Brozzoli et al., 2012, Journal of Neuroscience)
  - `W2169124255` (Filimon, 2010, The Neuroscientist)

## 2. Block/Trial Workflow

### Block Structure

- Total blocks:
  - human: `4`
  - qa/sim: `1`
- Trials per block:
  - human: `32`
  - qa/sim: `16`
- Randomization/counterbalancing:
  - each block uses `BlockUnit.generate_conditions(...)`
  - the condition list contains 16 fully specified trial tokens covering the 2 × 2 × 2 × 2 design
  - conditions are evenly sampled and shuffled within each block
- Condition generation method:
  - built-in `BlockUnit.generate_conditions(...)`
  - a custom controller is not needed because the trial token itself carries the full state needed for deterministic trial synthesis
  - data shape passed into `run_trial.py` is a string condition token such as `std_ll_pro_L` or `gen_lr_anti_R`
- Runtime-generated trial values:
  - eye fixation side
  - hand fixation side
  - cue side relative to eye fixation
  - pro/anti rule
  - deterministic cue/memory/response durations sampled from configured ranges
  - correct key derived from rule and cue direction
  - all generated in `src/utils.py` from the block seed and trial id so the timeline is reproducible

### Trial State Machine

1. State name: `fixation`
   - Onset trigger: `fixation_onset`
   - Stimuli shown:
     - eye fixation spot
     - hand anchor/fixation spot
     - setup-specific left/right positions for eye and hand anchors
   - Valid keys: none
   - Timeout behavior: fixed display duration, then advance
   - Next state: `context_cue`

2. State name: `context_cue`
   - Onset trigger: `context_cue_onset`
   - Stimuli shown:
     - eye fixation spot
     - hand anchor/fixation spot
     - colored square frame around the eye fixation spot
     - green frame for `pro`, blue frame for `anti`
   - Valid keys: none
   - Timeout behavior: fixed display duration, then advance
   - Next state: `memory_hold`

3. State name: `memory_hold`
   - Onset trigger: `memory_hold_onset`
   - Stimuli shown:
     - eye fixation spot
     - hand anchor/fixation spot
     - no rule frame
   - Valid keys: none
   - Timeout behavior: fixed display duration, then advance
   - Next state: `go_cue`

4. State name: `go_cue`
   - Onset trigger: `go_cue_onset`
   - Stimuli shown:
     - eye fixation spot
     - hand anchor/fixation spot
     - brief white spatial cue at the cue location relative to eye fixation
   - Valid keys: none
   - Timeout behavior: fixed display duration, then advance
   - Next state: `reach_response`

5. State name: `reach_response`
   - Onset trigger: `response_window_onset`
   - Stimuli shown:
     - eye fixation spot
     - hand anchor/fixation spot
     - spatial cue remains visible for the response deadline
   - Valid keys: `left_key`, `right_key`
   - Timeout behavior: no response before deadline marks the trial as timeout
   - Next state: `feedback`

6. State name: `feedback`
   - Onset trigger: `feedback_hit_onset` or `feedback_miss_onset`
   - Stimuli shown:
     - correct goal marker at the expected reach location
     - positive or negative feedback label, depending on outcome
   - Valid keys: none
   - Timeout behavior: fixed display duration, then advance
   - Next state: `iti`

7. State name: `iti`
   - Onset trigger: `iti_onset`
   - Stimuli shown:
     - neutral fixation cross
   - Valid keys: none
   - Timeout behavior: fixed display duration, then advance
   - Next state: next logical trial or block summary

## 3. Condition Semantics

Condition token syntax used in `task.conditions`:

- `std_ll_pro_L`
- `std_ll_pro_R`
- `std_ll_anti_L`
- `std_ll_anti_R`
- `std_rr_pro_L`
- `std_rr_pro_R`
- `std_rr_anti_L`
- `std_rr_anti_R`
- `gen_lr_pro_L`
- `gen_lr_pro_R`
- `gen_lr_anti_L`
- `gen_lr_anti_R`
- `gen_rl_pro_L`
- `gen_rl_pro_R`
- `gen_rl_anti_L`
- `gen_rl_anti_R`

Interpretation shared across all tokens:

- `std` means eye fixation and hand fixation occupy the same horizontal side
- `gen` means eye fixation and hand fixation occupy opposite horizontal sides
- `ll` means left eye fixation / left hand fixation
- `rr` means right eye fixation / right hand fixation
- `lr` means eye left / hand right
- `rl` means eye right / hand left
- `pro` means reach in the same direction as the spatial cue relative to eye fixation
- `anti` means reach in the opposite direction as the spatial cue relative to eye fixation
- `L` or `R` means cue location left or right relative to eye fixation

Participant-facing meaning, concrete realization, and outcome rule:

- `std_ll_pro_L`
  - Meaning: standard setup with eye and hand both left; cue left of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor left of center, green cue-frame rule, white cue left of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `std_ll_pro_R`
  - Meaning: standard setup with eye and hand both left; cue right of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor left of center, green cue-frame rule, white cue right of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `std_ll_anti_L`
  - Meaning: standard setup with eye and hand both left; cue left of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor left of center, blue cue-frame rule, white cue left of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `std_ll_anti_R`
  - Meaning: standard setup with eye and hand both left; cue right of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor left of center, blue cue-frame rule, white cue right of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `std_rr_pro_L`
  - Meaning: standard setup with eye and hand both right; cue left of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor right of center, green cue-frame rule, white cue left of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `std_rr_pro_R`
  - Meaning: standard setup with eye and hand both right; cue right of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor right of center, green cue-frame rule, white cue right of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `std_rr_anti_L`
  - Meaning: standard setup with eye and hand both right; cue left of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor right of center, blue cue-frame rule, white cue left of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `std_rr_anti_R`
  - Meaning: standard setup with eye and hand both right; cue right of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor right of center, blue cue-frame rule, white cue right of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `gen_lr_pro_L`
  - Meaning: generalized setup with eye left / hand right; cue left of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor right of center, green cue-frame rule, white cue left of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `gen_lr_pro_R`
  - Meaning: generalized setup with eye left / hand right; cue right of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor right of center, green cue-frame rule, white cue right of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `gen_lr_anti_L`
  - Meaning: generalized setup with eye left / hand right; cue left of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor right of center, blue cue-frame rule, white cue left of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `gen_lr_anti_R`
  - Meaning: generalized setup with eye left / hand right; cue right of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation left of center, white hand anchor right of center, blue cue-frame rule, white cue right of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `gen_rl_pro_L`
  - Meaning: generalized setup with eye right / hand left; cue left of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor left of center, green cue-frame rule, white cue left of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct
- `gen_rl_pro_R`
  - Meaning: generalized setup with eye right / hand left; cue right of eye; reach same direction as cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor left of center, green cue-frame rule, white cue right of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `gen_rl_anti_L`
  - Meaning: generalized setup with eye right / hand left; cue left of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor left of center, blue cue-frame rule, white cue left of the eye anchor
  - Outcome rule: right-direction response relative to the hand anchor is correct
- `gen_rl_anti_R`
  - Meaning: generalized setup with eye right / hand left; cue right of eye; reach opposite the cue
  - Concrete stimulus realization: red eye fixation right of center, white hand anchor left of center, blue cue-frame rule, white cue right of the eye anchor
  - Outcome rule: left-direction response relative to the hand anchor is correct

Participant-facing text source:

- `config/config.yaml` stimuli for instructions, block summaries, and completion screens
- `src/run_trial.py` uses `StimBank.get_and_format(...)` only for summary text interpolation
- trial-stage labels and response logic stay in code, but the visible copy remains in YAML

Why this source is appropriate for auditability:

- all participant-facing copy is editable without changing runtime control flow
- the runtime only selects and positions predeclared stimuli
- the same YAML source can be translated to another language without code edits

Localization strategy:

- Chinese participant text is stored in `config/*.yaml`
- fonts use `SimHei` for Chinese glyph coverage
- non-Chinese deployments can swap only the stimulus strings and font family while preserving the trial logic

## 4. Response and Scoring Rules

- Response mapping:
  - `f -> left`
  - `j -> right`
- Response key source:
  - `task.left_key`, `task.right_key`, and `task.key_list` in config
- If code-defined, why config-driven mapping is not sufficient:
  - the displayed keyboard proxy is still config-driven
  - the response translation logic is coded because the rule depends on the sampled cue direction and setup token
- Missing-response policy:
  - no valid key before deadline marks the trial as timeout
  - timeouts are counted as incorrect
- Correctness logic:
  - `pro` trials: response direction matches the cue direction relative to eye fixation
  - `anti` trials: response direction is opposite the cue direction relative to eye fixation
  - in both cases, the keyboard key is interpreted as left/right relative to the hand anchor
- Reward/penalty updates:
  - none
- Running metrics:
  - accuracy = correct trials / all trials
  - mean RT = average response latency across correct trials only
  - timeout count = number of trials without a valid response

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: `fixation`
  - Stimulus IDs shown together: `eye_fixation`, `hand_anchor`
  - Layout anchors (`pos`): eye fixation centered on the upper row; hand anchor centered on the lower row; trial-specific left/right x positions set to roughly `±145 px`
  - Size/spacing (`height`, width, wrap): eye fixation spot small and high-contrast; hand anchor slightly larger and outlined to stay readable
  - Readability/overlap checks: vertical separation prevents the two anchors from collapsing into one marker in the standard same-side trials
  - Rationale: the paper’s eye and hand fixation points are represented with two visually separable markers

- Screen name: `context_cue`
  - Stimulus IDs shown together: `eye_fixation`, `hand_anchor`, `rule_pro` or `rule_anti`
  - Layout anchors (`pos`): colored frame centered on the eye fixation; hand anchor remains on the lower row
  - Size/spacing (`height`, width, wrap): rule frame encloses the eye fixation with enough margin to remain visually distinct
  - Readability/overlap checks: the frame must not cover the hand anchor or the cue position
  - Rationale: the color-coded context cue is the primary rule signal

- Screen name: `memory_hold`
  - Stimulus IDs shown together: `eye_fixation`, `hand_anchor`
  - Layout anchors (`pos`): same as fixation screen
  - Size/spacing (`height`, width, wrap): neutral low-clutter display
  - Readability/overlap checks: no rule frame during memory hold so the cue is visibly gone
  - Rationale: supports the cue-to-go delay described in the paper

- Screen name: `go_cue`
  - Stimulus IDs shown together: `eye_fixation`, `hand_anchor`, `spatial_cue`
  - Layout anchors (`pos`): spatial cue appears left or right of the eye fixation; eye/hand anchors remain on their respective rows
  - Size/spacing (`height`, width, wrap): white cue circle small enough to avoid overlap with the fixation frame
  - Readability/overlap checks: cue locations must remain within the 1024x768 viewport at the chosen eccentricity
  - Rationale: the cue defines the reference direction that is transformed by the pro/anti rule

- Screen name: `reach_response`
  - Stimulus IDs shown together: `eye_fixation`, `hand_anchor`, `spatial_cue`
  - Layout anchors (`pos`): same as go cue, but the response window remains open until timeout or response
  - Size/spacing (`height`, width, wrap): identical to `go_cue` so the response window matches the instructed geometry
  - Readability/overlap checks: the cue and anchors remain legible without occluding each other
  - Rationale: lets the keyboard proxy stand in for the reach direction decision

- Screen name: `feedback`
  - Stimulus IDs shown together: correct goal marker plus hit/miss label
  - Layout anchors (`pos`): goal marker at the computed correct reach location; label centered above the display
  - Size/spacing (`height`, width, wrap): feedback label uses larger text than the cue to avoid ambiguity
  - Readability/overlap checks: feedback goal should never overlap the label
  - Rationale: mirrors the paper’s endpoint feedback at the goal location

- Screen name: `block_break` / `good_bye`
  - Stimulus IDs shown together: config-defined summary text only
  - Layout anchors (`pos`): centered text block
  - Size/spacing (`height`, width, wrap): `wrapWidth` wide enough for multi-line Chinese copy
  - Readability/overlap checks: only a single text panel is shown
  - Rationale: keeps transitions readable and uncluttered

## 6. Trigger Plan

| Trigger | Code | Semantics |
|---|---:|---|
| `exp_onset` | 1 | experiment start |
| `exp_end` | 2 | experiment end |
| `block_onset` | 10 | block start |
| `block_end` | 11 | block end |
| `fixation_onset` | 20 | eye/hand fixation display begins |
| `context_cue_onset` | 21 | colored pro/anti context cue appears |
| `memory_hold_onset` | 22 | post-cue retention interval begins |
| `go_cue_onset` | 23 | spatial cue / response-go signal appears |
| `response_window_onset` | 24 | active response capture window begins |
| `feedback_hit_onset` | 40 | correct response feedback |
| `feedback_miss_onset` | 41 | incorrect or timeout feedback |
| `response_left` | 50 | left-direction response key |
| `response_right` | 51 | right-direction response key |
| `response_timeout` | 60 | no response before the deadline |
| `iti_onset` | 70 | inter-trial interval onset |

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: simple mode-aware flow with one block loop and block-level summaries
- `utils.py` used? yes
- If yes, exact purpose:
  - deterministic trial-spec generation
  - condition parsing
  - cue/goal coordinate derivation
  - block/overall summary metrics
- Custom controller used? no
- If yes, why PsyFlow-native path is insufficient: n/a
- Legacy/backward-compatibility fallback logic required? no
- If yes, scope and removal plan: n/a

## 8. Inference Log

- The exact anti-reach paper is low citation and therefore not included in the selected bundle, but it is used as supplemental protocol context for the state machine and timing.
- The local runtime does not expose touch-screen or eye-tracker responses, so keyboard left/right responses are used as a portable proxy for reach direction.
- The published paper reports 0.5–1.0 s, 0.5–1.5 s, 0.2 s, 0.17 s, and 0.3 s intervals; the implementation uses the same bounded durations with deterministic sampling from those ranges.
- The paper’s movement time and endpoint variability outcomes are not directly representable in this runtime, so the build records latency, correctness, and timeout instead.
- Vertical separation of the eye and hand markers is an implementation choice to keep the trial visually readable on a desktop display while preserving the horizontal reference-frame logic.

## Contract Note

- Participant-facing labels/instructions/options should be config-defined whenever possible.
- `src/run_trial.py` should not hardcode participant-facing text that would require code edits for localization.
