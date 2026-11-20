# Reproducibility notes

## Original run

The published run used two proxy-visible model aliases, `gpt-6-luna` and `gemini-3.8-flash`, with one request per model and case. The protocol contains the system prompt, fictional policy, 12 cases, expected decisions, expected amounts, output limits, and scoring rule.

A result passed the predeclared strict check only when the raw response parsed as JSON and both `decision` and `amount_usd` exactly matched the answer key. The `reply` field was preserved but not separately graded.

## Post-hoc view

The published normalized view removes one outer Markdown code fence from responses that are otherwise JSON. This is a parser/integration repair, not a rerun and not a change to the raw evidence. `src/normalize_responses.py` implements only that deterministic transformation.

## Checksums

`results.json` records the SHA-256 digest of `protocol.json`. `src/score_results.py` recomputes and verifies it before scoring. The checksum identifies the archived bytes; it does not prove when the file was created, independently validate the model calls, or make a future replay identical.

## Fresh replays

`src/run_experiment.py` sends the same protocol to an OpenAI-compatible endpoint. It intentionally writes a separate output file and includes a warning that a replay may differ. Credentials are read from environment variables and are never written to the repository.

A replay should record at minimum the endpoint, requested model, returned model identifier, request time, response ID, finish reason, raw response text, usage metadata, and any error. Do not publish secrets, private customer data, or provider response headers that contain credentials.

## Interpretation

This is a small integration experiment, not a statistical benchmark. It does not establish a general ranking, reliability rate, safety guarantee, or suitability for production. The synthetic policy and cases are intentionally narrow. Readers should preserve the distinction between raw parsing, normalized parsing, policy-field accuracy, customer-facing prose quality, and authorization to perform a refund.
