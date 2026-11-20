# AI API cost calculator: browser test evidence

**Tested:** November 19, 2026, approximately 14:29–14:31 UTC, in the Manus sandbox browser (Chrome/156.0.0.0 on Linux). **Product:** [AInvasion Monthly API cost calculator](https://www.ainvasion.com/ai-cost-calculator/). The page says it was originally published September 16, 2026 and rebuilt/re-verified October 8, 2026; it labels its rate card as read on October 8, 2026. These are the page's claims, not independent vendor-price validation. [1]

**Result:** All 66 displayed amounts across the six recorded input states are consistent with the page's arithmetic and the observed display rounding, subject to the stated January cache-rate interpretation below. The examples establish neither that the rates are current nor that they match any provider's bill. The calculator's summary names only one cheapest and one priciest model in the default state, although the costs are tied.

## Formula and rates used for independent calculation

The page states: “cost = fresh input × input rate + cached input × cache-read rate + output × output rate.” Inputs are **millions of tokens per month**, and rates are **USD per million tokens**. For input I, output O, and cache proportion h, fresh input is I × (1 − h) and cached input is I × h. [1]

The page says Batch halves every rate **except Gemini 3.1 Pro Preview's cache rate**. The residency checkbox says “+10%, Anthropic and OpenAI”; the calculations multiply the applicable resulting cost by 1.1. The January checkbox says “Gemini Flash doubles”; the rate-card note explicitly changes Gemini 3.8 Flash input/output to $1.50/$7.50. For case 6, the expected amount additionally interprets “doubles” as doubling its $0.075 cache-read rate to $0.15. The visible note does not independently specify the future cache-read rate, so this part is an interpretation, not a verified future price. No January adjustment was applied to Flash-Lite.

The page's standard text rates, in the order **input / output / cache read**, are: [1]

- Anthropic: Claude Haiku 5.5 = $0.10 / $0.50 / $0.01; Claude Sonnet 5.5 = $2 / $10 / $0.10; Claude Opus 5.5 = $4 / $20 / $0.20; Claude Fable 5.1 = $10 / $50 / $0.25.
- OpenAI: GPT-6 Luna = $0.10 / $0.50 / $0.01; GPT-6.1 Sol = $2 / $10 / $0.10; GPT-6 Astra = $10 / $50 / $1; GPT-5.6 Sol **promotional tier** = $4 / $20 / $0.40.
- Google: Gemini 3.5 Flash-Lite = $0.30 / $2.50 / $0.03; Gemini 3.8 Flash = $0.75 / $3.75 / $0.075; Gemini 3.1 Pro Preview = $2 / $12 / $0.20.

Exact expectations below were independently computed with Python `decimal.Decimal`, not obtained from the calculator's implementation. In these cases, amounts under $10 displayed two decimal places and amounts of $10 or more displayed whole dollars. Each item is **exact expected USD → observed browser display**, so differences caused by this rounding are visible rather than hidden. This is an observed pattern for these examples, not a claim about every rounding boundary.

## Six recorded browser states

### 1. Default Chatbot state

Inputs: **50** million input, **10** million output; cache **0%**; Batch **off**; US residency **off**; January 2027 **off**. Initial page load, with the Chatbot preset selected. [Screenshot](calculator-screenshots/ainvasion_2026-11-19_14-29-39_1341.webp)

- Anthropic: Claude Haiku 5.5 **10 → $10**; Claude Sonnet 5.5 **200 → $200**; Claude Opus 5.5 **400 → $400**; Claude Fable 5.1 **1000 → $1,000**.
- OpenAI: GPT-6 Luna **10 → $10**; GPT-6.1 Sol **200 → $200**; GPT-6 Astra **1000 → $1,000**; GPT-5.6 Sol (promo) **400 → $400**.
- Google: Gemini 3.5 Flash-Lite **40 → $40**; Gemini 3.8 Flash **75 → $75**; Gemini 3.1 Pro Preview **220 → $220**.

The summary displayed “Cheapest: Claude Haiku 5.5 at $10. Priciest: GPT-6 Astra at $1,000. That is a 100.0x spread for the same token volume.” GPT-6 Luna also tied for cheapest, and Claude Fable 5.1 also tied for priciest; the summary did not mention those ties. The ratio is correct for this case.

### 2. Light preset

Action: click **Light**. Inputs: **5** million input, **1** million output; cache **0%**; Batch **off**; residency **off**; January **off**. [Screenshot](calculator-screenshots/ainvasion_2026-11-19_14-29-50_6599.webp)

- Anthropic: Claude Haiku 5.5 **1 → $1.00**; Claude Sonnet 5.5 **20 → $20**; Claude Opus 5.5 **40 → $40**; Claude Fable 5.1 **100 → $100**.
- OpenAI: GPT-6 Luna **1 → $1.00**; GPT-6.1 Sol **20 → $20**; GPT-6 Astra **100 → $100**; GPT-5.6 Sol (promo) **40 → $40**.
- Google: Gemini 3.5 Flash-Lite **4 → $4.00**; Gemini 3.8 Flash **7.5 → $7.50**; Gemini 3.1 Pro Preview **22 → $22**.

### 3. Zero-usage boundary

Action: enter **0** in each token field. Inputs: **0** million input, **0** million output; cache **0%**; Batch **off**; residency **off**; January **off**. [Screenshot](calculator-screenshots/ainvasion_2026-11-19_14-30-01_7338.webp)

- Anthropic: Claude Haiku 5.5 **0 → $0.00**; Claude Sonnet 5.5 **0 → $0.00**; Claude Opus 5.5 **0 → $0.00**; Claude Fable 5.1 **0 → $0.00**.
- OpenAI: GPT-6 Luna **0 → $0.00**; GPT-6.1 Sol **0 → $0.00**; GPT-6 Astra **0 → $0.00**; GPT-5.6 Sol (promo) **0 → $0.00**.
- Google: Gemini 3.5 Flash-Lite **0 → $0.00**; Gemini 3.8 Flash **0 → $0.00**; Gemini 3.1 Pro Preview **0 → $0.00**.

The summary changed to “Enter token volumes above to see costs.” No zero-denominator ratio was shown.

### 4. Mixed fresh and cached input

Actions: enter **100** input and **20** output, then click the middle of the cache slider. Inputs: **100** million input, **20** million output; cache **45%**; Batch **off**; residency **off**; January **off**. This is 55 million fresh and 45 million cached input tokens. [Screenshot](calculator-screenshots/ainvasion_2026-11-19_14-30-20_4673.webp)

- Anthropic: Claude Haiku 5.5 **15.95 → $16**; Claude Sonnet 5.5 **314.5 → $315**; Claude Opus 5.5 **629 → $629**; Claude Fable 5.1 **1561.25 → $1,561**.
- OpenAI: GPT-6 Luna **15.95 → $16**; GPT-6.1 Sol **314.5 → $315**; GPT-6 Astra **1595 → $1,595**; GPT-5.6 Sol (promo) **638 → $638**.
- Google: Gemini 3.5 Flash-Lite **67.85 → $68**; Gemini 3.8 Flash **119.625 → $120**; Gemini 3.1 Pro Preview **359 → $359**.

Example: Claude Sonnet 5.5 is `55 × 2 + 45 × 0.1 + 20 × 10 = $314.50`, shown as **$315**. The summary displayed a **100.0x** spread; the exact expected amounts $1,595 and $15.95 have that ratio, while the rounded display values $1,595 and $16 do not produce exactly 100.0x.

### 5. Maximum cache plus Batch

Actions: focus the cache slider and press **End** to reach its maximum, then enable **Batch API**. Inputs: **100** million input, **20** million output; cache **90%**; Batch **on**; residency **off**; January **off**. [Screenshot](calculator-screenshots/ainvasion_2026-11-19_14-30-35_6606.webp)

- Anthropic: Claude Haiku 5.5 **5.95 → $5.95**; Claude Sonnet 5.5 **114.5 → $115**; Claude Opus 5.5 **229 → $229**; Claude Fable 5.1 **561.25 → $561**.
- OpenAI: GPT-6 Luna **5.95 → $5.95**; GPT-6.1 Sol **114.5 → $115**; GPT-6 Astra **595 → $595**; GPT-5.6 Sol (promo) **238 → $238**.
- Google: Gemini 3.5 Flash-Lite **27.85 → $28**; Gemini 3.8 Flash **44.625 → $45**; Gemini 3.1 Pro Preview **148 → $148**.

Example for the stated Batch exception: Gemini 3.1 Pro Preview is `10 × (2 / 2) + 90 × 0.2 + 20 × (12 / 2) = $148`, matching the display. Halving its cache-read rate too would instead produce $139.

### 6. Maximum cache, Batch, US residency and January scenario

Actions: retain case 5, then enable **US-only data residency** and **Price as of Jan 1, 2027**. Inputs: **100** million input, **20** million output; cache **90%**; Batch **on**; residency **on**; January **on**. The three checked states were also read from the live browser DOM. [Screenshot](calculator-screenshots/ainvasion_2026-11-19_14-30-51_3882.webp)

- Anthropic: Claude Haiku 5.5 **6.545 → $6.55**; Claude Sonnet 5.5 **125.95 → $126**; Claude Opus 5.5 **251.9 → $252**; Claude Fable 5.1 **617.375 → $617**.
- OpenAI: GPT-6 Luna **6.545 → $6.55**; GPT-6.1 Sol **125.95 → $126**; GPT-6 Astra **654.5 → $655**; GPT-5.6 Sol (promo) **261.8 → $262**.
- Google: Gemini 3.5 Flash-Lite **27.85 → $28**; Gemini 3.8 Flash **89.25 → $89**; Gemini 3.1 Pro Preview **148 → $148**.

For Gemini 3.8 Flash, the case-6 expectation assumes all three Flash rates double, giving `10 × (1.50 / 2) + 90 × (0.15 / 2) + 20 × (7.50 / 2) = $89.25`, shown as **$89**. If the cache-read rate were unchanged at $0.075, the analogous expectation would be **$85.875**; the page does not explicitly state that future cache rate in its rate-card note. For Haiku, the unrounded case-5 $5.95 × 1.1 = $6.545, shown as **$6.55**. Google costs are not increased by the residency toggle in this test.

## Limits and reproducibility

The token fields declare minimum 0 and step `any`; the cache slider declares minimum 0%, maximum 90%, and 5-percentage-point steps. Thus 100% cache is not selectable with the observed slider. Negative and fractional token inputs, other combinations, long-context cliffs, and non-browser devices were not tested. The page itself says its calculation excludes cache-write charges, Google's hourly cache-storage fees, long-context surcharges, and tool fees. It also describes context thresholds separately. These tests evaluate the calculator against its **own stated simplified model**, not actual invoices or current vendor rate cards. [1]

The screenshots capture the browser viewport and may not show the entire result table; all 11 row values above were read from the rendered browser table. Rates, interface, and observed outputs may change after the test date.

## References

[1]: https://www.ainvasion.com/ai-cost-calculator/ "AInvasion AI API cost calculator and rate card"
