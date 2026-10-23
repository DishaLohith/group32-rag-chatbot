import pandas as pd


# =========================================================
# FILE PATHS
# =========================================================

RESULTS_FILE = "../../target/runs/gst-rag-classification-results.csv"
GROUNDTRUTH_FILE = "../../gst_data/walert_data/groundtruth.csv"

OUTPUT_FILE = "../../target/runs/gst-rag-error-analysis.csv"


# =========================================================
# LOAD DATA
# =========================================================

print("Loading classification results...")

results_df = pd.read_csv(RESULTS_FILE)

print("Results loaded:", len(results_df))


# =========================================================
# ANALYSE EACH QUESTION
# =========================================================

analysis_rows = []

for _, row in results_df.iterrows():

    query_id = row["query_id"]
    question = row["question"]
    expected = row["expected_label"]
    predicted = row["prediction"]

    retrieved = str(row["retrieved_passages"]).split(";")

    # Find gold relevant passages from groundtruth
    groundtruth_df = pd.read_csv(GROUNDTRUTH_FILE)

    gt_row = groundtruth_df[
        groundtruth_df["query_id"] == query_id
    ]

    gold_passages = []

    if len(gt_row) > 0:
        gold_passages = str(
            gt_row.iloc[0]["relevant_passages"]
        ).split(";")

    # Check whether any gold passage was retrieved
    gold_retrieved = any(
        passage in retrieved
        for passage in gold_passages
    )

    classification_correct = predicted == expected


    # =====================================================
    # DETERMINE ERROR TYPE
    # =====================================================

    if classification_correct:

        error_type = "Correct"

    elif not gold_retrieved:

        error_type = "Retrieval failure"

    else:

        error_type = "Generation failure"


    analysis_rows.append({
        "query_id": query_id,
        "question": question,
        "expected_label": expected,
        "predicted_label": predicted,
        "gold_passages": ";".join(gold_passages),
        "retrieved_passages": ";".join(retrieved),
        "gold_retrieved_top3": gold_retrieved,
        "classification_correct": classification_correct,
        "error_type": error_type
    })


# =========================================================
# CREATE DATAFRAME
# =========================================================

analysis_df = pd.DataFrame(analysis_rows)


# =========================================================
# SAVE CSV
# =========================================================

analysis_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# =========================================================
# PRINT RESULTS
# =========================================================

print("\n========================================")
print("GST RAG ERROR ANALYSIS")
print("========================================")

print(
    analysis_df[
        [
            "query_id",
            "expected_label",
            "predicted_label",
            "gold_retrieved_top3",
            "error_type"
        ]
    ].to_string(index=False)
)


print("\n========================================")
print("ERROR SUMMARY")
print("========================================")

print(analysis_df["error_type"].value_counts())


print("\nCSV saved successfully to:")
print(OUTPUT_FILE)