from __future__ import annotations

from functools import partial
from typing import Any

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import ANTI_COLOR, HIT_COLOR, MISS_COLOR, PRO_COLOR, SIDE_LEFT, SIDE_RIGHT, build_antireach_trial_spec


def _make_unit(win, kb, trigger_runtime, label: str) -> StimUnit:
    return StimUnit(unit_label=label, win=win, kb=kb, runtime=trigger_runtime)


def _add_fixation_display(unit: StimUnit, stim_bank, spec: dict[str, Any]) -> StimUnit:
    unit.add_stim(stim_bank.rebuild("eye_fixation", pos=[spec["eye_x"], spec["eye_y"]]))
    unit.add_stim(stim_bank.rebuild("hand_anchor", pos=[spec["hand_x"], spec["hand_y"]]))
    return unit


def _rule_color(rule: str):
    return PRO_COLOR if str(rule).lower() == "pro" else ANTI_COLOR


def _cue_label(rule: str) -> str:
    return "pro" if str(rule).lower() == "pro" else "anti"


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
    block_seed=None,
):
    """Run one anti-reach trial."""
    trial_id = next_trial_id()
    spec = build_antireach_trial_spec(
        condition=condition,
        trial_id=trial_id,
        block_seed=block_seed,
        settings=settings,
    )

    block_label = str(block_id) if block_id is not None else "block_0"
    block_index = int(block_idx) if block_idx is not None else 0
    trial_label = spec["condition_id"]
    cue_color = _rule_color(spec["rule"])
    goal_color = HIT_COLOR
    miss_color = MISS_COLOR

    trial_data = {
        "trial_id": int(trial_id),
        "block_id": block_label,
        "block_idx": block_index,
        "condition": spec["condition"],
        "condition_id": trial_label,
        "setup": spec["setup"],
        "layout_kind": spec["layout_kind"],
        "layout_code": spec["layout_code"],
        "rule": spec["rule"],
        "cue_side": spec["cue_side"],
        "eye_side": spec["eye_side"],
        "hand_side": spec["hand_side"],
        "goal_side": spec["goal_side"],
        "correct_key": spec["correct_key"],
        "left_key": spec["left_key"],
        "right_key": spec["right_key"],
    }

    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    fixation = _add_fixation_display(make_unit(unit_label="fixation"), stim_bank, spec)
    set_trial_context(
        fixation,
        trial_id=trial_id,
        phase="fixation",
        deadline_s=spec["fixation_duration"],
        valid_keys=[],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "fixation",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "block_idx": block_index,
        },
        stim_id="eye_fixation+hand_anchor",
    )
    fixation.show(
        duration=spec["fixation_duration"],
        onset_trigger=settings.triggers.get("fixation_onset"),
    ).to_dict(trial_data)

    context_cue = _add_fixation_display(make_unit(unit_label="context_cue"), stim_bank, spec)
    context_cue.add_stim(
        stim_bank.rebuild(
            "context_frame",
            pos=[spec["eye_x"], spec["eye_y"]],
            width=spec["frame_size_px"],
            height=spec["frame_size_px"],
            lineColor=cue_color,
            fillColor=None,
        )
    )
    set_trial_context(
        context_cue,
        trial_id=trial_id,
        phase="context_cue",
        deadline_s=spec["context_cue_duration"],
        valid_keys=[],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "context_cue",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "block_idx": block_index,
        },
        stim_id=f"eye_fixation+hand_anchor+context_frame_{_cue_label(spec['rule'])}",
    )
    context_cue.show(
        duration=spec["context_cue_duration"],
        onset_trigger=settings.triggers.get("context_cue_onset"),
    ).to_dict(trial_data)

    memory_hold = _add_fixation_display(make_unit(unit_label="memory_hold"), stim_bank, spec)
    set_trial_context(
        memory_hold,
        trial_id=trial_id,
        phase="memory_hold",
        deadline_s=spec["memory_hold_duration"],
        valid_keys=[],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "memory_hold",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "block_idx": block_index,
        },
        stim_id="eye_fixation+hand_anchor",
    )
    memory_hold.show(
        duration=spec["memory_hold_duration"],
        onset_trigger=settings.triggers.get("memory_hold_onset"),
    ).to_dict(trial_data)

    go_cue = _add_fixation_display(make_unit(unit_label="go_cue"), stim_bank, spec)
    go_cue.add_stim(
        stim_bank.rebuild(
            "spatial_cue",
            pos=[spec["cue_x"], spec["cue_y"]],
            radius=spec.get("cue_radius_px", 14),
        )
    )
    set_trial_context(
        go_cue,
        trial_id=trial_id,
        phase="go_cue",
        deadline_s=spec["go_cue_duration"],
        valid_keys=[],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "go_cue",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "goal_side": spec["goal_side"],
            "block_idx": block_index,
        },
        stim_id="eye_fixation+hand_anchor+spatial_cue",
    )
    go_cue.show(
        duration=spec["go_cue_duration"],
        onset_trigger=settings.triggers.get("go_cue_onset"),
    ).to_dict(trial_data)

    reach_response = _add_fixation_display(make_unit(unit_label="reach_response"), stim_bank, spec)
    reach_response.add_stim(
        stim_bank.rebuild(
            "spatial_cue",
            pos=[spec["cue_x"], spec["cue_y"]],
            radius=spec.get("cue_radius_px", 14),
        )
    )
    set_trial_context(
        reach_response,
        trial_id=trial_id,
        phase="reach_response",
        deadline_s=spec["response_deadline"],
        valid_keys=[spec["left_key"], spec["right_key"]],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "reach_response",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "goal_side": spec["goal_side"],
            "correct_key": spec["correct_key"],
            "block_idx": block_index,
        },
        stim_id="eye_fixation+hand_anchor+spatial_cue",
    )
    reach_response.capture_response(
        keys=[spec["left_key"], spec["right_key"]],
        correct_keys=[spec["correct_key"]],
        duration=spec["response_deadline"],
        onset_trigger=settings.triggers.get("response_window_onset"),
        response_trigger={
            spec["left_key"]: settings.triggers.get("response_left"),
            spec["right_key"]: settings.triggers.get("response_right"),
        },
        timeout_trigger=settings.triggers.get("response_timeout"),
    ).to_dict(trial_data)

    response_key = str(reach_response.get_state("response", "")).strip().lower()
    responded = bool(response_key)
    hit = bool(reach_response.get_state("hit", False))
    rt = reach_response.get_state("rt", None)
    rt_s = float(rt) if isinstance(rt, (int, float)) else None

    trial_data.update(
        {
            "timed_out": not responded,
            "response_key": response_key,
            "response_rt": rt_s,
            "response_correct": bool(hit),
            "reach_response_response": response_key,
            "reach_response_rt": rt_s,
            "reach_response_hit": bool(hit),
        }
    )

    outcome = "hit" if hit else ("timeout" if not responded else "miss")
    feedback = make_unit(unit_label="feedback")
    if hit:
        feedback.add_stim(
            stim_bank.rebuild(
                "goal_marker",
                pos=[spec["goal_x"], spec["goal_y"]],
                lineColor=goal_color,
                fillColor=goal_color,
            )
        )
        feedback.add_stim(stim_bank.get_and_format("feedback_text", feedback_label="正确"))
        feedback_trigger = settings.triggers.get("feedback_hit_onset")
    else:
        feedback.add_stim(
            stim_bank.rebuild(
                "goal_marker",
                pos=[spec["goal_x"], spec["goal_y"]],
                lineColor=miss_color,
                fillColor=miss_color,
            )
        )
        feedback_label = "超时" if not responded else "错误"
        feedback.add_stim(stim_bank.get_and_format("feedback_text", feedback_label=feedback_label))
        feedback_trigger = settings.triggers.get("feedback_miss_onset")

    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=spec["feedback_duration"],
        valid_keys=[],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "feedback",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "goal_side": spec["goal_side"],
            "outcome": outcome,
            "block_idx": block_index,
        },
        stim_id="goal_marker+feedback_text",
    )
    feedback.show(
        duration=spec["feedback_duration"],
        onset_trigger=feedback_trigger,
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti")
    iti.add_stim(stim_bank.get("fixation_cross"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="iti",
        deadline_s=spec["iti_duration"],
        valid_keys=[],
        block_id=block_label,
        condition_id=trial_label,
        task_factors={
            "stage": "iti",
            "rule": spec["rule"],
            "setup": spec["setup"],
            "cue_side": spec["cue_side"],
            "eye_side": spec["eye_side"],
            "hand_side": spec["hand_side"],
            "block_idx": block_index,
        },
        stim_id="fixation_cross",
    )
    iti.show(
        duration=spec["iti_duration"],
        onset_trigger=settings.triggers.get("iti_onset"),
    ).to_dict(trial_data)

    return trial_data
