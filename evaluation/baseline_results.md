# Baseline Test — No-Retrieval LLM vs. GST Test Set

Tested a general-purpose LLM (no document retrieval, no grounding) against our 14-item test set to establish Condition 1 of our 3-way comparison (no-retrieval LLM vs. adapted Walert vs. our own system). The unedited prompt and response are in `baseline_raw_response.md`.

| # | Product | Expected Answer | Baseline Answer | Correct? | Cited Specific Source? |
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
| 12 | Still bottled water | GST-free | Taxable | Disagreement | No |
| 13 | Sparkling water | Taxable | Taxable | Yes | No |
| 14 | Rice cakes (contested) | Abstain | Hedged, no clean abstention | Partial | No |

**Key finding:** 12/14 correct classifications, but zero specific provision citations across all 14 responses, and one direct disagreement with our source material (bottled water). This demonstrates why classification accuracy alone is insufficient for this use case — a business needs traceable, verifiable answers, which requires retrieval grounding against real ATO documents rather than relying on general model knowledge.

**Note on item 14:** This baseline was run on the original GST14 wording ("Rice cakes", expected answer: abstain). The group later revised GST14 to "rice cakes made principally from compressed cereal" (expected GST-free); see the revision note in `test_set.md`. The results above are unchanged and describe the original item.
