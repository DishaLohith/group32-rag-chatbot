# Baseline Test — No-Retrieval LLM vs. GST Test Set

A general-purpose LLM (no document retrieval) was asked all 14 test questions to establish Condition 1 of the three-way comparison. The unedited prompt and response are in `baseline_raw_response.md`.

| # | Product | Expected (at time of run) | Baseline Answer | Correct? | Cited Specific Source? |
|---|---|---|---|---|---|
| 1 | Bread rolls (supermarket) | GST-free | GST-free | Yes | No |
| 2 | Bread rolls (restaurant) | Taxable | Taxable | Yes | No |
| 3 | Plain milk | GST-free | GST-free | Yes | No |
| 4 | Flavoured milk | Taxable | Taxable | Yes | No |
| 5 | Raw chicken | GST-free | GST-free | Yes | No |
| 6 | Hot roast chicken | Taxable | Taxable | Yes | No |
| 7 | Confectionery | Taxable | Taxable | Yes | No |
| 8 | Soft drink | Taxable | Taxable | Yes | No |
| 9 | Fruit juice ≥90% | GST-free | GST-free | Yes | No |
| 10 | Raw almonds | GST-free | GST-free | Yes | No |
| 11 | Roasted salted almonds | Taxable | Taxable | Yes | No |
| 12 | Still bottled water | GST-free | Taxable | No | No |
| 13 | Sparkling water | Taxable | Taxable | Yes | No |
| 14 | Rice cakes | Abstain | Hedged | Partial | No |

## Results on items 1–13 (all three conditions)

| Metric | Baseline (no retrieval) | Adapted Walert | Our system |
|---|---|---|---|
| Accuracy | 12/13 (92.3%) | 6/13 (46.2%) | 12/13 (92.3%) |
| Macro-F1 | 0.921 | 0.353 | 0.962 |
| Attribution | 0% | 0% | 11/13 (84.6%) |

GST14 separately: baseline hedged (wrong), Walert correct, our system correct.

The baseline was as accurate as our system but cited no specific provision. Retrieval's main gain is traceability.

The table above was scored when GST14's expected answer was Abstain. GST14 is now GST-free (see `test_set.md`).
