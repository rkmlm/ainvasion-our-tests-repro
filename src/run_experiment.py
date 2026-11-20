"""Replay the protocol through an OpenAI-compatible API.

This is a clean-room replay helper, not a claim that it reproduces the
original proxy run exactly. It never stores API keys in the repository.
"""
from __future__ import annotations

import argparse
import json
import os
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests


def call_model(base_url: str, api_key: str, model: str, system_prompt: str, policy: str, case: str, limit: int) -> dict:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt + "\n\n" + policy},
            {"role": "user", "content": case},
        ],
        "max_tokens": limit,
    }
    response = requests.post(url, headers={"Authorization": f"Bearer {api_key}"}, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", type=Path, default=Path("evidence/protocol.json"))
    parser.add_argument("--out", type=Path, default=Path("evidence/results_replay.json"))
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--api-key", default=os.environ.get("OPENAI_API_KEY"))
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()
    if not args.api_key:
        raise SystemExit("Set OPENAI_API_KEY (or pass --api-key); never commit it.")

    protocol_bytes = args.protocol.read_bytes()
    protocol = json.loads(protocol_bytes)
    observations = []
    for model in protocol["models"]:
        limit = protocol["output_limit"].get(model, {}).get("max_tokens", 2000)
        for case in protocol["cases"]:
            started = datetime.now(timezone.utc).isoformat()
            record = {"model_requested": model, "case_id": case["id"], "started_utc": started}
            try:
                raw = call_model(args.base_url, args.api_key, model, protocol["system_prompt"], protocol["policy"], case["case"], limit)
                choice = raw["choices"][0]
                record.update({
                    "response_id": raw.get("id", str(uuid.uuid4())),
                    "model_returned": raw.get("model"),
                    "finish_reason": choice.get("finish_reason"),
                    "response_text": choice["message"]["content"],
                    "usage": raw.get("usage"),
                })
            except Exception as exc:
                record["error"] = f"{type(exc).__name__}: {exc}"
            observations.append(record)
            if args.sleep:
                time.sleep(args.sleep)

    import hashlib
    output = {
        "experiment": protocol["title"],
        "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
        "execution_environment": f"OpenAI-compatible endpoint: {args.base_url}",
        "test_completed_utc": datetime.now(timezone.utc).isoformat(),
        "observations": observations,
        "note": "Replay output is separate from the original published run and may differ by provider revision, proxy routing, or defaults.",
    }
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
