# Evaluation Metrics — Group 32 GST Classification

The main scores use GST01–GST13. GST14 (rice cakes) is reported separately.

- **Accuracy** is the percentage of questions answered correctly. An Abstain counts as incorrect.
- **Macro-F1** is the average of the F1 score for GST-free and the F1 score for Taxable. This gives both labels equal weight. An Abstain counts as a miss for the correct label.
- **Attribution** measures whether the system's evidence includes at least one passage listed as relevant in the ground truth. A system that cites nothing scores 0.

The test includes similar products with different GST outcomes, such as raw and hot chicken, plain and flavoured milk, raw and roasted almonds, and still and sparkling water. These pairs help show whether a system follows the GST rule for each case, rather than relying on the product name alone.

All scores were calculated in `GST_results.xlsx`.
