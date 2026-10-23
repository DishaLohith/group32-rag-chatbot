import pandas as pd

from GST_IMPROVED import (
    get_context_passages,
    classify_from_evidence
)


# =========================================================
# PATHS
# =========================================================

TEST_FILE = "../../gst_data/walert_data/gst_abstention_test.csv"

OUTPUT = "../../target/runs/gst-abstention-results.csv"


# =========================================================
# LOAD ABSTENTION TEST SET
# =========================================================

print("\nLoading GST abstention test set...")

df = pd.read_csv(TEST_FILE)

print("Questions loaded:", len(df))


# =========================================================
# RUN TESTS
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

    evidence_statuses = ";".join(
        item["status"]
        for item in result["evidence"]
    )

    correct = prediction == expected

    print("Expected:  ", expected)
    print("Predicted: ", prediction)
    print("Retrieved: ", retrieved_ids)
    print("Evidence:  ", evidence_ids)
    print("Statuses:  ", evidence_statuses)
    print("Reason:    ", result["reason"])
    print("Correct:   ", correct)

    results.append({
        "query_id": query_id,
        "question": question,
        "expected_label": expected,
        "prediction": prediction,
        "retrieved_passages": retrieved_ids,
        "evidence_used": evidence_ids,
        "evidence_statuses": evidence_statuses,
        "reason": result["reason"],
        "correct": correct
    })


# =========================================================
# SAVE RESULTS
# =========================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    OUTPUT,
    index=False
)


# =========================================================
# ABSTENTION PERFORMANCE
# =========================================================

correct_count = int(results_df["correct"].sum())
total = len(results_df)

accuracy = correct_count / total

abstain_count = (
    results_df["prediction"] == "Abstain"
).sum()

abstention_rate = abstain_count / total


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n========================================")
print("TIER-C ABSTENTION RESULTS")
print("========================================")

print(f"Correct abstentions: {correct_count}/{total}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy: {accuracy * 100:.2f}%")

print(
    f"Abstention rate: "
    f"{abstain_count}/{total} "
    f"({abstention_rate * 100:.2f}%)"
)

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