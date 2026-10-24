# Evaluation Metrics — Group 32 GST Classification

Main scores use test items 1–13. GST14 (rice cakes) is reported separately.

1. **Accuracy** — share of items where the label (GST-free or Taxable) is correct. An Abstain counts as wrong.
2. **Macro-F1** — F1 for GST-free and F1 for Taxable, averaged. An Abstain counts as a miss for the correct class.
3. **Attribution** — share of items where the system's evidence includes at least one gold passage from `quantitative_eval/gst_data/processed/groundtruth.csv`. A system that cites nothing scores 0.

Near-duplicate pairs (raw vs hot chicken, plain vs flavoured milk, raw vs roasted almonds, still vs sparkling water) check that the system follows the rule, not the product name.

All scores were calculated in `GST_results.xlsx`.
