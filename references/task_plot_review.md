# Task Plot Review

## Evidence Match

- Pass: title and construct match the Anti-Reach Task.
- Pass: rows collapse the 16 condition tokens into standard/generalized by pro/anti classes while preserving cue-side variation.
- Pass: phase order matches README and `src/run_trial.py`: Fixation -> Context cue -> Memory hold -> Go cue -> Reach response -> Feedback -> ITI.
- Pass: timing labels match config: 500-1000 ms fixation, 200 ms context cue, 500-1500 ms memory hold, 170 ms go cue, 1000 ms response, 300 ms feedback, 600 ms ITI.
- Pass: response mapping shows F=left and J=right.
- Pass: pro rows show same-direction response and anti rows show opposite-direction response.
- Pass: no reward or extra adaptive controller is shown.

## Visual Quality

- Pass: labels and timings are readable.
- Pass: generated timeline content stays below the header band.
- Pass: fixed title and Construct subtitle are centered.
- Pass: top-right TaskBeacon logo lockup is borderless and non-overlapping.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`; raw timeline is saved as `references/task_plot_timeline_raw.png`.
