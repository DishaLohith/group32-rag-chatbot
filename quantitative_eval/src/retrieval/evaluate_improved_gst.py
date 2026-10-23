import pandas as pd

from GST_IMPROVED import (
    get_context_passages,
    classify_from_evidence
)


# =========================================================
# PATHS
# =========================================================

GROUNDTRUTH = "../../gst_data/walert_data/groundtruth.csv"

OUTPUT = "../../target/runs/gst-improved-classification-results.csv"


# =========================================================
# LOAD GROUND TRUTH
# =========================================================

print("\nLoading GST ground truth...")

df = pd.read_csv(GROUNDTRUTH)

print("Questions loaded:", len(df))


# =========================================================
# RUN ALL QUESTIONS
# =========================================================

results = []

for _, row in df.iterrows():

    query_id = row["query_id"]
    question = row["query"]
    expected = row["expected_label"]

    print("\n========================================")
    print(f"{query_id}: {question}")
    print("========================================")

    contexts = get_context_passages(question)

    result = classify_from_evidence(contexts)

    prediction = result["classification"]

    retrieved_ids = ";".join(
        context["passage_id"]
        for context in contexts
    )

    evidence_ids = ";".join(
        item["passage_id"]
        for item in result["evidence"]
    )

    correct = prediction == expected

    print("Expected:  ", expected)
    print("Predicted: ", prediction)
    print("Retrieved: ", retrieved_ids)
    print("Evidence:  ", evidence_ids)
    print("Reason:    ", result["reason"])
    print("Correct:   ", correct)

    results.append({
        "query_id": query_id,
        "question": question,
        "expected_label": expected,
        "prediction": prediction,
        "retrieved_passages": retrieved_ids,
        "evidence_used": evidence_ids,
        "reason": result["reason"],
        "correct": correct
    })


# =========================================================
# CREATE RESULTS DATAFRAME
# =========================================================

results_df = pd.DataFrame(results)


# =========================================================
# SAVE RESULTS
# =========================================================

results_df.to_csv(
    OUTPUT,
    index=False
)


# =========================================================
# CALCULATE ACCURACY
# =========================================================

correct_count = int(results_df["correct"].sum())

total = len(results_df)

accuracy = correct_count / total


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n========================================")
print("IMPROVED GST SYSTEM RESULTS")
print("========================================")

print(f"Correct: {correct_count}/{total}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nPrediction counts:")
print(results_df["prediction"].value_counts())

print("\nQuestion-level results:")

print(
    results_df[
        [
            "query_id",
            "expected_label",
            "prediction",
            "correct"
        ]
    ].to_string(index=False)
)

print("\nResults saved to:")
print(OUTPUT)