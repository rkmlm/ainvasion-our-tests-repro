"""Validate and score the published Our Tests evidence.

Usage:
    python src/score_results.py
    python src/score_results.py --protocol evidence/protocol.json --results evidence/results.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from normalize_responses import remove_outer_json_fence


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=Path("evidence/protocol.json"))
    parser.add_argument("--results", type=Path, default=Path("evidence/results.json"))
    args = parser.parse_args()

    protocol_bytes = args.protocol.read_bytes()
    protocol = json.loads(protocol_bytes)
    results = json.loads(args.results.read_text(encoding="utf-8"))
    expected = {case["id"]: case for case in protocol["cases"]}
    assert hashlib.sha256(protocol_bytes).hexdigest() == results["protocol_sha256"], "protocol checksum mismatch"

    raw_pass = {}
    normalized_pass = {}
    for obs in results["observations"]:
        case = expected[obs["case_id"]]
        parsed = obs.get("parsed_response")
        raw_valid = isinstance(parsed, dict) and obs.get("passes_decision_and_amount") is True
        normalized = parsed
        if not raw_valid:
            try:
                normalized = json.loads(remove_outer_json_fence(obs.get("response_text", "")))
            except json.JSONDecodeError:
                normalized = None
        normalized_ok = (
            isinstance(normalized, dict)
            and normalized.get("decision") == case["expected_decision"]
            and normalized.get("amount_usd") == case["expected_amount_usd"]
        )
        model = obs["model_requested"]
        raw_pass[model] = raw_pass.get(model, 0) + int(raw_valid)
        normalized_pass[model] = normalized_pass.get(model, 0) + int(normalized_ok)

    print(json.dumps({
        "observations": len(results["observations"]),
        "raw_pass": raw_pass,
        "after_outer_fence_removal": normalized_pass,
        "protocol_sha256": results["protocol_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
