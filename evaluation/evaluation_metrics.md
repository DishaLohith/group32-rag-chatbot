# Evaluation Metrics — Group 32 GST Classification

This file defines how the 14-item test set (`test_set.md`) is scored. Each metric says what it tells you and how it is calculated.

## Core metrics (defined for the no-retrieval baseline)

1. **Classification accuracy** — did the system label the product GST-free or taxable correctly? Calculated as (correct classifications) / (14 total items).
2. **Attribution correctness** — did the system cite the correct governing provision or document (Schedule item, GSTD determination, or Act section)? Calculated as (correct citations) / (14 total items).
3. **Abstention behaviour** — on a case where the evidence is genuinely unclear, did the system decline to answer instead of guessing with false confidence? Scored yes/no per case.

Near-duplicate pairs (raw vs. hot chicken, plain vs. flavoured milk, raw vs. roasted almonds, still vs. sparkling water) test whether the system applies the retrieved rule or pattern-matches on product names.

## How these relate to the group's full evaluation

The group's later evaluation (Achyut's presentation and the written report) extends these with retrieval metrics (nDCG@1/3/5, Recall@k), macro-F1 alongside accuracy, and abstention measures (refusal rate, false abstention rate, risk-coverage). Retrieval numbers come from Aarya's pipeline and are not reproduced in this repo folder. The three metrics above are the ones used for the baseline in `baseline_results.md`.

## Note on abstention and GST14

The original GST14 (rice cakes) was the abstention case. The group revised GST14 to a narrower, answerable question (see the revision note in `test_set.md`), so the revised set has no built-in abstention item. Adding a genuinely ambiguous item was raised with the group and is not settled in this folder.

Status: Metrics defined; applied to the no-retrieval baseline (see `baseline_results.md`).
