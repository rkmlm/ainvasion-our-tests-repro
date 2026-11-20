# AInvasion Our Tests: Customer-Support Policy Experiment

Reproducibility materials for [AInvasion’s Our Tests experiment](https://www.ainvasion.com/our-ai-tests/).

This repository contains the published protocol, fictional policy, answer key, 24 recorded responses, analysis output, calculator audit, and clean-room replay helpers. It is designed to let a reader inspect the original record and run a new replay without exposing API credentials.

## What the experiment tested

Two proxy-visible model endpoints received the same 12 fictional airline customer-support cases, one attempt per model and case. The predeclared score required a valid JSON object whose `decision` and `amount_usd` matched the answer key. The customer-facing `reply` was retained for inspection but was not scored separately.

The original record found that the GPT endpoint passed the strict raw-JSON check for all 12 cases. The Gemini endpoint returned all 12 responses inside Markdown code fences; after removing the outer fence, the decision and amount fields matched the answer key for all 12 cases. This is integration evidence from a small convenience sample, not a benchmark, safety certification, deployment recommendation, or general model ranking.

## Repository layout

```text
.
├── README.md
├── LICENSE-CODE
├── LICENSE-DATA.md
├── CITATION.cff
├── evidence/
│   ├── protocol.json          # policy, cases, answer key, scoring rules
│   ├── results.json           # original 24 raw observations and metadata
│   ├── analysis.json          # published aggregate analysis
│   ├── calculator-test.md     # calculator audit in plain text
│   └── calculator-test.html   # calculator audit with screenshots/formatting
├── src/
│   ├── normalize_responses.py # deterministic outer-fence normalization
│   ├── score_results.py       # checksum validation and scoring
│   └── run_experiment.py      # optional OpenAI-compatible replay helper
└── docs/
    └── REPRODUCIBILITY.md     # detailed method and interpretation notes
```

## Quick verification of the published record

No network access or API key is needed to verify the archived results:

```bash
python3 src/score_results.py
```

Expected output is equivalent to:

```json
{
  "after_outer_fence_removal": {
    "gemini-3.8-flash": 12,
    "gpt-6-luna": 12
  },
  "raw_pass": {
    "gemini-3.8-flash": 0,
    "gpt-6-luna": 12
  },
  "observations": 24
}
```

The verifier also checks that the SHA-256 digest of `evidence/protocol.json` matches the digest recorded in `evidence/results.json`.

## Run a fresh replay

The replay helper uses an OpenAI-compatible `/chat/completions` endpoint. It does not reproduce the original run exactly: provider revisions, proxy routing, defaults, availability, and response formatting may differ.

1. Create a virtual environment and install the only runtime dependency:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   pip install requests
   ```

2. Set credentials outside the repository:

   ```bash
   export OPENAI_API_KEY='REPLACE_WITH_A_KEY'
   export OPENAI_BASE_URL='https://your-authorized-endpoint.example/v1'
   ```

   Never put an API key in a source file, commit, issue, notebook, or README. The original experiment used a Manus proxy; access to that proxy is not implied by this repository.

3. Run the replay:

   ```bash
   python3 src/run_experiment.py \
     --protocol evidence/protocol.json \
     --out evidence/results_replay.json
   ```

4. Inspect the output. If you want to score a replay, preserve the original `evidence/results.json` and run the verifier against the replay only after adapting it to include parsed responses and the scoring fields. A replay is a new experiment, not a replacement for the archived original.

## Reproducibility and limitations

The protocol, answer key, raw responses, aggregate analysis, and calculator audit are public. The original run script and post-hoc normalization were archived but were not part of the public file set when the page was first published; this repository now provides a clean-room normalization and replay implementation. It is not represented as the byte-for-byte original execution script.

The model names in the original evidence are proxy-reported aliases. Provider model revisions and exact backend mappings were not independently verified. The original test used one attempt per case, 12 synthetic English-language cases, one fictional policy, and no immutable provider snapshots. It did not test consumer applications, browsing, retrieval, connected tools, real transactions, malicious documents, or a complete prompt-injection defense.

The experiment should not be used to select a production model by itself. For deployment decisions, build a larger private test set from the relevant workflow, separate format validity from business-rule correctness, keep authorization in deterministic code or human approval, and repeat the test after changes to the model, prompt, policy, or integration.

## Citation

See `CITATION.cff` for a machine-readable citation. Suggested citation:

> Morgan, Tom / AInvasion. *Our Tests: AI Customer-Support Policy Experiment and Reproducibility Materials*. 2026. https://www.ainvasion.com/our-ai-tests/

## License

Code in `src/` is offered under the MIT License in `LICENSE-CODE`. Evidence and documentation are offered under CC BY 4.0 in `LICENSE-DATA.md`, unless a source file states otherwise. Third-party material remains subject to its own terms.
