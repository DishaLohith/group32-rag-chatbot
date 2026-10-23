from GST_IMPROVED import (
    get_context_passages,
    classify_from_evidence
)

import re


# =========================================================
# GST DOMAIN GATE
# =========================================================

GST_TERMS = [
    "gst",
    "taxable",
    "tax free",
    "tax-free",
    "gst free",
    "gst-free"
]

FOOD_QUESTION_PATTERNS = [
    r"\bis .* taxable\b",
    r"\bare .* taxable\b",
    r"\bis .* gst[- ]free\b",
    r"\bare .* gst[- ]free\b"
]


def is_gst_classification_question(question):

    text = question.lower().strip()

    # Explicit GST/tax terminology
    if any(term in text for term in GST_TERMS):
        return True

    # Classification-style wording
    for pattern in FOOD_QUESTION_PATTERNS:

        if re.search(pattern, text):
            return True

    return False


# =========================================================
# FINAL GST SYSTEM
# =========================================================

def classify_gst(question):

    # -----------------------------------------------------
    # Stage 1: Domain gate
    # -----------------------------------------------------

    if not is_gst_classification_question(question):

        return {
            "classification": "Abstain",
            "reason": (
                "The question does not appear to request an "
                "Australian GST food classification."
            ),
            "contexts": [],
            "evidence": []
        }


    # -----------------------------------------------------
    # Stage 2: Dense retrieval
    # -----------------------------------------------------

    contexts = get_context_passages(question)


    # -----------------------------------------------------
    # Stage 3: Evidence classification
    # -----------------------------------------------------

    result = classify_from_evidence(contexts)

    return {
        "classification": result["classification"],
        "reason": result["reason"],
        "contexts": contexts,
        "evidence": result["evidence"]
    }


# =========================================================
# SIMPLE TEST
# =========================================================

if __name__ == "__main__":

    questions = [

        "Is flavoured chocolate milk taxable?",

        "Are plain bread rolls GST-free?",

        "What is the capital of France?"

    ]

    for question in questions:

        print("\n========================================")
        print("Question:", question)
        print("========================================")

        result = classify_gst(question)

        print(
            "Classification:",
            result["classification"]
        )

        print(
            "Reason:",
            result["reason"]
        )

        if len(result["contexts"]) > 0:

            print("\nRetrieved:")

            for context in result["contexts"]:

                print(
                    context["passage_id"],
                    "->",
                    round(context["score"], 4)
                )