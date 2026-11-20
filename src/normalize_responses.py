"""Deterministic post-hoc normalization used for the integration check.

This does not alter the recorded raw response. It only removes one outer
Markdown code fence when a provider returns fenced JSON.
"""
from __future__ import annotations

import re


_FENCE = re.compile(r"^\s*```(?:json)?\s*\n(?P<body>.*)\n```\s*$", re.IGNORECASE | re.DOTALL)


def remove_outer_json_fence(text: str) -> str:
    """Return text with one outer ``` or ```json fence removed, if present."""
    match = _FENCE.match(text)
    return match.group("body") if match else text
