import pandas as pd

from RAG_GST import (
    get_context_passages,
    build_prompt,
    generate_answer
)


# =========================================================
# FILES
# =========================================================

GROUNDTRUTH = "../../gst_data/walert_data/groundtruth.csv"

OUTPUT = "../../target/runs/gst-rag-classification-results.csv"


# =========================================================
# LOAD TEST QUESTIONS
# =========================================================

print("\nLoading GST ground truth...")

df = pd.read_csv(GROUNDTRUTH)

print("Questions loaded:", len(df))


# =========================================================
# NORMALISE MODEL OUTPUT
# =========================================================

def normalise_prediction(answer):

    answer = str(answer).strip().lower()

    if answer == "taxable":
        return "Taxable"

    if answer in ["gst-free", "gst free"]:
        return "GST-free"

    if answer == "abstain":
        return "Abstain"

    return "Invalid"


# =========================================================
# RUN ALL GST QUESTIONS
# =========================================================

results = []

for index, row in df.iterrows():

    query_id = row["query_id"]
    question = row["query"]
    expected = row["expected_label"]

    print("\n========================================")
    print(f"{query_id}: {question}")
    print("========================================")

    contexts = get_context_passages(question)

    prompt = build_prompt(
        question,
        contexts
    )

    raw_answer = generate_answer(prompt)

    prediction = normalise_prediction(raw_answer)

    retrieved_ids = ";".join(
        context["passage_id"]
        for context in contexts
    )

    correct = prediction == expected

    print("Expected: ", expected)
    print("Predicted:", prediction)
    print("Raw output:", raw_answer)
    print("Evidence: ", retrieved_ids)
    print("Correct:  ", correct)

    results.append({
        "query_id": query_id,
        "question": question,
        "expected_label": expected,
        "prediction": prediction,
        "raw_output": raw_answer,
        "retrieved_passages": retrieved_ids,
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
# CALCULATE ACCURACY
# =========================================================

correct_count = results_df["correct"].sum()

total = len(results_df)

accuracy = correct_count / total


print("\n========================================")
print("GST RAG CLASSIFICATION RESULTS")
print("========================================")

print(f"Correct: {correct_count}/{total}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nPrediction counts:")
print(results_df["prediction"].value_counts())

print("\nResults saved to:")
print(OUTPUT)