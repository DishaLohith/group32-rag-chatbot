import pandas as pd

from GST_FINAL import classify_gst


# =========================================================
# PATHS
# =========================================================

GST_TEST = "../../gst_data/walert_data/groundtruth.csv"

ABSTENTION_TEST = "../../gst_data/walert_data/gst_abstention_test.csv"

OUTPUT = "../../target/runs/gst-final-system-results.csv"


# =========================================================
# EVALUATION FUNCTION
# =========================================================

def evaluate_dataset(df, test_type):

    results = []

    for _, row in df.iterrows():

        query_id = row["query_id"]
        question = row["query"]
        expected = row["expected_label"]

        result = classify_gst(question)

        prediction = result["classification"]

        correct = prediction == expected

        retrieved_ids = ";".join(
            context["passage_id"]
            for context in result["contexts"]
        )

        evidence_ids = ";".join(
            item["passage_id"]
            for item in result["evidence"]
        )

        print("\n========================================")
        print(f"{query_id}: {question}")
        print("========================================")

        print("Type:      ", test_type)
        print("Expected:  ", expected)
        print("Predicted: ", prediction)
        print("Retrieved: ", retrieved_ids)
        print("Evidence:  ", evidence_ids)
        print("Correct:   ", correct)

        results.append({
            "query_id": query_id,
            "test_type": test_type,
            "question": question,
            "expected_label": expected,
            "prediction": prediction,
            "retrieved_passages": retrieved_ids,
            "evidence_used": evidence_ids,
            "reason": result["reason"],
            "correct": correct
        })

    return results


# =========================================================
# LOAD DATASETS
# =========================================================

print("\nLoading GST classification test set...")

gst_df = pd.read_csv(GST_TEST)

print("GST questions:", len(gst_df))


print("\nLoading Tier-C abstention test set...")

abstain_df = pd.read_csv(ABSTENTION_TEST)

print("Abstention questions:", len(abstain_df))


# =========================================================
# RUN BOTH TEST SETS
# =========================================================

all_results = []

all_results.extend(
    evaluate_dataset(
        gst_df,
        "GST classification"
    )
)

all_results.extend(
    evaluate_dataset(
        abstain_df,
        "Tier-C abstention"
    )
)


# =========================================================
# RESULTS DATAFRAME
# =========================================================

results_df = pd.DataFrame(all_results)

results_df.to_csv(
    OUTPUT,
    index=False
)


# =========================================================
# GST CLASSIFICATION PERFORMANCE
# =========================================================

gst_results = results_df[
    results_df["test_type"] == "GST classification"
]

gst_correct = int(
    gst_results["correct"].sum()
)

gst_total = len(gst_results)

gst_accuracy = gst_correct / gst_total


# =========================================================
# ABSTENTION PERFORMANCE
# =========================================================

abstention_results = results_df[
    results_df["test_type"] == "Tier-C abstention"
]

abstention_correct = int(
    abstention_results["correct"].sum()
)

abstention_total = len(abstention_results)

abstention_accuracy = (
    abstention_correct / abstention_total
)


# =========================================================
# OVERALL PERFORMANCE
# =========================================================

overall_correct = int(
    results_df["correct"].sum()
)

overall_total = len(results_df)

overall_accuracy = (
    overall_correct / overall_total
)


# =========================================================
# PRINT FINAL RESULTS
# =========================================================

print("\n========================================")
print("FINAL GST SYSTEM RESULTS")
print("========================================")

print(
    f"GST classification: "
    f"{gst_correct}/{gst_total} "
    f"({gst_accuracy * 100:.2f}%)"
)

print(
    f"Tier-C abstention: "
    f"{abstention_correct}/{abstention_total} "
    f"({abstention_accuracy * 100:.2f}%)"
)

print(
    f"Overall: "
    f"{overall_correct}/{overall_total} "
    f"({overall_accuracy * 100:.2f}%)"
)


print("\nPrediction counts:")

print(
    results_df["prediction"].value_counts()
)


print("\nQuestion-level results:")

print(
    results_df[
        [
            "query_id",
            "test_type",
            "expected_label",
            "prediction",
            "correct"
        ]
    ].to_string(index=False)
)


print("\nResults saved to:")
print(OUTPUT)