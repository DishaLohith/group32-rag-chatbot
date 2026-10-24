# GST Classification Test Set — Group 32

14-item test set covering clear-cut GST-free items, clear-cut taxable items, and one contested case, including near-duplicate pairs to test whether classification is driven by actual retrieved rules rather than surface similarity between product names.

| # | Product | Correct Answer | Supporting Source |
|---|---|---|---|
| 1 | Plain bread rolls | GST-free | GST Act s 38-2 |
| 2 | Bread rolls (served in restaurant) | Taxable | s 38-3 |
| 3 | Plain milk | GST-free | Schedule 2, item 1 |
| 4 | Flavoured (chocolate) milk | Taxable | Detailed Food List |
| 5 | Raw chicken | GST-free | s 38-2 |
| 6 | Hot roast chicken, ready to eat | Taxable | Detailed Food List |
| 7 | Chocolate / confectionery | Taxable | Schedule 1 |
| 8 | Carbonated soft drink | Taxable | s 38-3(1)(d), not listed in Schedule 2 |
| 9 | Fruit juice, ≥90% juice | GST-free | GSTD 2002/2 |
| 10 | Plain unsalted raw almonds | GST-free | Detailed Food List |
| 11 | Roasted salted almonds | Taxable | Detailed Food List |
| 12 | Still bottled water, unflavoured | GST-free | Schedule 2, item 14 |
| 13 | Sparkling mineral water | Taxable | s 38-3(1)(d), not listed in Schedule 2 (optional, same logic as soft drink) |
| 14 | Rice cakes (DFL entry 656, under review) | Abstain — contested | Detailed Food List |

## Revision note (GST14)

The table above is the original test set, as it was when the no-retrieval baseline was run (see `baseline_results.md`).

The group later revised GST14 to "Are rice cakes made principally from compressed cereal GST-free?", expected label **GST-free**. The reason: ATO Detailed Food List entry 656 lists all rice cakes as GST-free, but the ATO's separate guidance (Issue 26) says only rice cakes made principally from compressed cereal are GST-free, and the ATO has said it is reviewing entry 656. The original wording was therefore too broad to have a single correct answer. Rows 1–13 are unchanged.

Status: Test set used as the basis for the group's evaluation (groundtruth GST01–GST14). GST14 revised as described above.
