from __future__ import annotations

import math
import random
from typing import Any, Callable

from psychopy import logging

RULE_PRO = "pro"
RULE_ANTI = "anti"
SIDE_LEFT = "left"
SIDE_RIGHT = "right"

SETUP_STD_LL = "std_ll"
SETUP_STD_RR = "std_rr"
SETUP_GEN_LR = "gen_lr"
SETUP_GEN_RL = "gen_rl"

DEFAULT_CONDITIONS = tuple(
    f"{setup}_{rule}_{cue}"
    for setup in (SETUP_STD_LL, SETUP_STD_RR, SETUP_GEN_LR, SETUP_GEN_RL)
    for rule in (RULE_PRO, RULE_ANTI)
    for cue in ("L", "R")
)

PAIR_TO_SIDES = {
    "ll": (SIDE_LEFT, SIDE_LEFT),
    "rr": (SIDE_RIGHT, SIDE_RIGHT),
    "lr": (SIDE_LEFT, SIDE_RIGHT),
    "rl": (SIDE_RIGHT, SIDE_LEFT),
}

PRO_COLOR = [0.25, 0.9, 0.25]
ANTI_COLOR = [0.95, 0.25, 0.25]
HIT_COLOR = [0.2, 0.85, 0.35]
MISS_COLOR = [0.98, 0.55, 0.15]


def _make_seeded_random(seed: int) -> Callable[[], float]:
    value = seed & 0xFFFFFFFF

    def rng() -> float:
        nonlocal value
        value = (value + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((value ^ (value >> 15)) * (1 | value)) & 0xFFFFFFFF
        t ^= (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0

    return rng


def _as_float(value: Any, fallback: float) -> float:
    try:
        parsed = float(value)
    except Exception:
        return float(fallback)
    if math.isnan(parsed) or math.isinf(parsed):
        return float(fallback)
    return parsed


def _trial_rng(*, block_seed: int | None, trial_id: int, condition: str) -> Callable[[], float]:
    base = int(block_seed) if block_seed is not None else 0
    cond_offset = sum(ord(ch) for ch in str(condition))
    mixed_seed = (base * 1000003 + int(trial_id) * 97 + cond_offset) & 0xFFFFFFFF
    return _make_seeded_random(mixed_seed)


def _sample_duration(value: Any, rng: Callable[[], float], fallback: float) -> float:
    if isinstance(value, (list, tuple)):
        if len(value) == 2:
            low = _as_float(value[0], fallback)
            high = _as_float(value[1], fallback)
            if high < low:
                low, high = high, low
            return low + (high - low) * rng()
        if len(value) == 1:
            return _as_float(value[0], fallback)
    return _as_float(value, fallback)


def parse_antireach_condition(condition: str) -> dict[str, str]:
    token = str(condition).strip().lower()
    parts = token.split("_")
    if len(parts) != 4:
        raise ValueError(f"Unsupported anti-reach condition token: {condition!r}")

    layout_kind, layout_code, rule_token, cue_token = parts
    if layout_kind not in {"std", "gen"}:
        raise ValueError(f"Unsupported anti-reach layout kind: {layout_kind!r}")
    if layout_code not in PAIR_TO_SIDES:
        raise ValueError(f"Unsupported anti-reach layout code: {layout_code!r}")
    if rule_token not in {RULE_PRO, RULE_ANTI}:
        raise ValueError(f"Unsupported anti-reach rule: {rule_token!r}")
    if cue_token not in {"l", "r", "left", "right"}:
        raise ValueError(f"Unsupported anti-reach cue side: {cue_token!r}")

    eye_side, hand_side = PAIR_TO_SIDES[layout_code]
    cue_side = SIDE_LEFT if cue_token.startswith("l") else SIDE_RIGHT
    setup = f"{layout_kind}_{layout_code}"

    return {
        "condition": token,
        "condition_id": token,
        "setup": setup,
        "layout_kind": layout_kind,
        "layout_code": layout_code,
        "rule": rule_token,
        "cue_side": cue_side,
        "eye_side": eye_side,
        "hand_side": hand_side,
    }


def _side_to_sign(side: str) -> int:
    return -1 if str(side).strip().lower() == SIDE_LEFT else 1


def _sign_to_side(sign: int) -> str:
    return SIDE_LEFT if sign < 0 else SIDE_RIGHT


def build_antireach_trial_spec(
    *,
    condition: str,
    trial_id: int,
    block_seed: int | None = None,
    settings: Any,
) -> dict[str, Any]:
    parsed = parse_antireach_condition(condition)
    rng = _trial_rng(block_seed=block_seed, trial_id=trial_id, condition=parsed["condition_id"])

    left_key = str(getattr(settings, "left_key", "f")).strip().lower()
    right_key = str(getattr(settings, "right_key", "j")).strip().lower()

    position_step_px = _as_float(getattr(settings, "position_step_px", 145), 145.0)
    eye_row_y_px = _as_float(getattr(settings, "eye_row_y_px", 120), 120.0)
    hand_row_y_px = _as_float(getattr(settings, "hand_row_y_px", -120), -120.0)
    cue_row_y_px = _as_float(getattr(settings, "cue_row_y_px", eye_row_y_px), eye_row_y_px)
    goal_row_y_px = _as_float(getattr(settings, "goal_row_y_px", hand_row_y_px), hand_row_y_px)
    frame_size_px = _as_float(getattr(settings, "frame_size_px", 84), 84.0)

    eye_x = _side_to_sign(parsed["eye_side"]) * position_step_px
    hand_x = _side_to_sign(parsed["hand_side"]) * position_step_px
    cue_x = eye_x + (_side_to_sign(parsed["cue_side"]) * position_step_px)
    cue_side = parsed["cue_side"]
    goal_side = cue_side if parsed["rule"] == RULE_PRO else (SIDE_RIGHT if cue_side == SIDE_LEFT else SIDE_LEFT)
    goal_x = hand_x + (_side_to_sign(goal_side) * position_step_px)

    fixation_duration = _sample_duration(getattr(settings, "fixation_duration", 0.6), rng, 0.6)
    context_cue_duration = _sample_duration(getattr(settings, "context_cue_duration", 0.2), rng, 0.2)
    memory_hold_duration = _sample_duration(getattr(settings, "memory_hold_duration", 0.9), rng, 0.9)
    go_cue_duration = _sample_duration(getattr(settings, "go_cue_duration", 0.17), rng, 0.17)
    response_deadline = _sample_duration(getattr(settings, "response_deadline", 1.0), rng, 1.0)
    feedback_duration = _sample_duration(getattr(settings, "feedback_duration", 0.3), rng, 0.3)
    iti_duration = _sample_duration(getattr(settings, "iti_duration", 0.6), rng, 0.6)

    correct_key = left_key if goal_side == SIDE_LEFT else right_key

    if bool(getattr(settings, "enable_logging", True)):
        logging.data(
            f"[AntiReach] condition={parsed['condition_id']} trial_id={trial_id} "
            f"rule={parsed['rule']} cue_side={parsed['cue_side']} correct_key={correct_key}"
        )

    return {
        **parsed,
        "goal_side": goal_side,
        "correct_key": correct_key,
        "left_key": left_key,
        "right_key": right_key,
        "position_step_px": position_step_px,
        "eye_row_y_px": eye_row_y_px,
        "hand_row_y_px": hand_row_y_px,
        "cue_row_y_px": cue_row_y_px,
        "goal_row_y_px": goal_row_y_px,
        "frame_size_px": frame_size_px,
        "eye_x": eye_x,
        "eye_y": eye_row_y_px,
        "hand_x": hand_x,
        "hand_y": hand_row_y_px,
        "cue_x": cue_x,
        "cue_y": cue_row_y_px,
        "goal_x": goal_x,
        "goal_y": goal_row_y_px,
        "fixation_duration": fixation_duration,
        "context_cue_duration": context_cue_duration,
        "memory_hold_duration": memory_hold_duration,
        "go_cue_duration": go_cue_duration,
        "response_deadline": response_deadline,
        "feedback_duration": feedback_duration,
        "iti_duration": iti_duration,
    }


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    token = str(value if value is not None else "").strip().lower()
    return token in {"1", "true", "yes", "y"}


def _summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "accuracy": 0.0,
            "mean_rt_ms": 0.0,
            "timeout_count": 0,
            "total_trials": 0,
        }

    correct = 0
    timeout_count = 0
    rt_sum = 0.0
    rt_count = 0
    for row in rows:
        if _as_bool(row.get("response_correct", False)):
            correct += 1
            rt = row.get("response_rt", None)
            if isinstance(rt, (int, float)):
                rt_sum += float(rt)
                rt_count += 1
        if _as_bool(row.get("timed_out", False)):
            timeout_count += 1

    accuracy = correct / len(rows)
    mean_rt_ms = (rt_sum / rt_count) * 1000.0 if rt_count > 0 else 0.0
    return {
        "accuracy": accuracy,
        "mean_rt_ms": mean_rt_ms,
        "timeout_count": timeout_count,
        "total_trials": len(rows),
    }


def summarizeBlock(reducedRows: list[dict[str, Any]], blockId: str) -> dict[str, Any]:
    rows = [row for row in reducedRows if str(row.get("block_id", "")) == blockId]
    return _summarize(rows)


def summarizeOverall(reducedRows: list[dict[str, Any]]) -> dict[str, Any]:
    return _summarize(list(reducedRows))
