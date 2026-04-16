# Task Plot Audit

- generated_at: 2026-04-16T01:10:35Z
- mode: existing
- task_path: E:\Taskbeacon\T000046-anti-reach-task

## 1. Inputs and provenance

- E:\Taskbeacon\T000046-anti-reach-task\README.md
- E:\Taskbeacon\T000046-anti-reach-task\config\config.yaml
- E:\Taskbeacon\T000046-anti-reach-task\src\run_trial.py

## 2. Evidence extracted from README

- Fixation shows the eye fixation spot and hand anchor on separate rows.
- Context cue uses a green pro frame or a blue anti frame.
- Memory hold removes the frame while fixation continues.
- Go cue and response present a white spatial cue and capture the left/right proxy response.
- Feedback shows a goal marker plus an outcome label.
- ITI shows a neutral fixation cross.

## 3. Evidence extracted from config/source

- 16 condition tokens grouped into pro and anti families.
- Fixation duration range: 500-1000 ms.
- Context cue duration: 200 ms.
- Memory hold duration range: 500-1500 ms.
- Go cue duration: 170 ms.
- Response window duration: 1000 ms.
- Feedback duration: 300 ms.
- ITI duration: 600 ms.

## 4. Mapping to task_plot_spec

- Timeline collection: one representative timeline per rule family.
- Standard/generalized cue-side variants are collapsed into pro and anti.
- Row subtitles encode the canonical layout used in the figure.
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Two-timeline overview selected for legibility.
- Black cards with colored cues preserve the task's visual language.
- Phase labels and timing labels remain readable at publication scale.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 2
- screens_per_timeline: 7
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- qa_mode: local
- layout_pass_1: row subtitles shortened; anti row moved upward; no overlap in phase cards
- layout_pass_2: final figure checked visually for spacing and scale

## 7. Output files and checksums

- E:\Taskbeacon\T000046-anti-reach-task\references\task_plot_spec.yaml: sha256=9E3DA0D8820EC6B2E2BB9AF65D824C08772840A078376163FA2185FE8DDD8280
- E:\Taskbeacon\T000046-anti-reach-task\references\task_plot_spec.json: sha256=E16504B930CAFE22253FC546F9028FDADE09732D14472C02353F6670929289DD
- E:\Taskbeacon\T000046-anti-reach-task\references\task_plot_source_excerpt.md: sha256=9F15D2CCC52D89CE4061555301B721FB2D1CF0EA331C602216487FF35E5CC508
- E:\Taskbeacon\T000046-anti-reach-task\task_flow.png: sha256=2730B862DF362E3598354B3FABD21A58CF630CC7EBF5B1A45C8123CD39F5F57A

## 8. Inferred/uncertain items

- Standard versus generalized layouts are collapsed into the representative pro and anti rows.
- Cue side and correct response follow the final condition token suffix and the rule frame color.
