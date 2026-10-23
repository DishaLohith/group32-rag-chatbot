from pyserini.search.faiss import FaissSearcher
import pandas as pd
import re


# =========================================================
# HELD-OUT CONFIGURATION
# =========================================================

DATA_DIR = "../../gst_data/walert_data/heldout"

COLLECTION = DATA_DIR + "/collection_heldout.csv"

INDEX = "../../target/indexes/gst-heldout-tct_colbert-v2-hnp-msmarco-faiss"

QUERY_ENCODER = "castorini/tct_colbert-v2-hnp-msmarco"

TOP_K = 3


# =========================================================
# LOAD HELD-OUT COLLECTION
# =========================================================

print("Loading held-out GST collection...")

collection_df = pd.read_csv(COLLECTION)

print("Held-out GST passages loaded:", len(collection_df))


# =========================================================
# LOAD DENSE RETRIEVER
# =========================================================

print("Loading held-out GST Dense FAISS retriever...")

searcher = FaissSearcher(
    INDEX,
    QUERY_ENCODER
)

print("Held-out retriever loaded.")


# =========================================================
# RETRIEVE EVIDENCE
# =========================================================

def get_context_passages(question, top_k=TOP_K):

    hits = searcher.search(question, 10)

    contexts = []

    for hit in hits[:top_k]:

        row = collection_df[
            collection_df["passage_id"] == hit.docid
        ]

        if len(row) == 0:
            continue

        passage = str(row.iloc[0]["passage"])

        contexts.append({
            "passage_id": hit.docid,
            "score": float(hit.score),
            "passage": passage
        })

    return contexts


# =========================================================
# EXTRACT EXPLICIT GST STATUS
# =========================================================

def extract_status(passage):

    text = passage.lower()

    if re.search(r"gst status:\s*gst[- ]free", text):
        return "GST-free"

    if re.search(r"gst status:\s*taxable", text):
        return "Taxable"

    if "supply of *food is gst-free" in text:
        return "GST-free"

    if "supply of food is gst-free" in text:
        return "GST-free"

    return None


# =========================================================
# EVIDENCE-BASED CLASSIFIER
# =========================================================

def classify_from_evidence(contexts):

    evidence = []

    for context in contexts:

        status = extract_status(
            context["passage"]
        )

        if status is not None:

            evidence.append({
                "passage_id": context["passage_id"],
                "score": context["score"],
                "status": status
            })


    # No explicit status evidence
    if len(evidence) == 0:

        return {
            "classification": "Abstain",
            "reason": (
                "No retrieved passage contained an explicit "
                "GST classification."
            ),
            "evidence": []
        }


    taxable = [
        item for item in evidence
        if item["status"] == "Taxable"
    ]

    gst_free = [
        item for item in evidence
        if item["status"] == "GST-free"
    ]


    # All explicit evidence says Taxable
    if len(taxable) > 0 and len(gst_free) == 0:

        return {
            "classification": "Taxable",
            "reason": (
                "The retrieved passages containing explicit GST "
                "status information consistently classify the "
                "related products as taxable."
            ),
            "evidence": taxable
        }


    # All explicit evidence says GST-free
    if len(gst_free) > 0 and len(taxable) == 0:

        return {
            "classification": "GST-free",
            "reason": (
                "The retrieved passages containing explicit GST "
                "status information consistently classify the "
                "related products as GST-free."
            ),
            "evidence": gst_free
        }


    # Conflicting evidence
    return {
        "classification": "Abstain",
        "reason": (
            "The retrieved passages contain conflicting explicit "
            "GST classifications, so the system abstains."
        ),
        "evidence": evidence
    }


# =========================================================
# TEST ONE QUESTION
# =========================================================

if __name__ == "__main__":

    question = "Is flavoured chocolate milk taxable?"

    print("\nQuestion:")
    print(question)

    contexts = get_context_passages(question)

    print("\n========================================")
    print("HELD-OUT TOP 3 PASSAGES")
    print("========================================")

    for i, context in enumerate(contexts, start=1):

        print(f"\n--- Document {i} ---")
        print("Passage ID:", context["passage_id"])
        print("Score:", context["score"])
        print(context["passage"])

        status = extract_status(
            context["passage"]
        )

        print("Extracted status:", status)


    result = classify_from_evidence(contexts)


    print("\n========================================")
    print("IMPROVED HELD-OUT CLASSIFICATION")
    print("========================================")

    print("Classification:", result["classification"])
    print("Reason:", result["reason"])

    print("\nEvidence used:")

    if len(result["evidence"]) == 0:

        print("None")

    else:

        for item in result["evidence"]:

            print(
                item["passage_id"],
                "->",
                item["status"]
            )